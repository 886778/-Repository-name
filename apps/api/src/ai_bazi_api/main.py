import logging
from collections.abc import AsyncIterator, Awaitable, Callable, Mapping
from contextlib import asynccontextmanager
from typing import Final

import uvicorn
from ai_bazi_backend.bootstrap import PlatformRuntime, build_runtime
from ai_bazi_backend.platform.errors import PlatformError
from ai_bazi_backend.platform.observability import (
    MetricsRecorder,
    Timer,
    TraceContext,
    accepted_identifier,
    bind_trace_context,
    current_trace_context,
    trace_id_from_traceparent,
)
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import Response

APP_NAME: Final = "ai-bazi-api"
LOGGER = logging.getLogger("ai_bazi.api")


def create_app(
    *,
    environ: Mapping[str, str] | None = None,
    metrics: MetricsRecorder | None = None,
) -> FastAPI:
    runtime = build_runtime(APP_NAME, environ=environ, metrics=metrics)

    @asynccontextmanager
    async def lifespan(application: FastAPI) -> AsyncIterator[None]:
        await runtime.startup()
        application.state.runtime = runtime
        try:
            yield
        finally:
            await runtime.shutdown()

    application = FastAPI(
        title="AI Bazi Platform API",
        version="0.1.0",
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
        lifespan=lifespan,
    )
    application.state.runtime = runtime
    _install_middleware(application, runtime)
    _install_error_handlers(application)
    _install_health_routes(application, runtime)
    return application


def _install_middleware(application: FastAPI, runtime: PlatformRuntime) -> None:
    @application.middleware("http")
    async def request_context(
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        request_id = accepted_identifier(request.headers.get("X-Request-Id"))
        correlation_id = accepted_identifier(request.headers.get("X-Correlation-Id"))
        context = TraceContext(
            request_id=request_id,
            correlation_id=correlation_id,
            trace_id=trace_id_from_traceparent(request.headers.get("traceparent")),
        )
        timer = Timer()
        status_code = 500
        with bind_trace_context(context):
            try:
                response = await call_next(request)
                status_code = response.status_code
            finally:
                duration = timer.elapsed_seconds
                labels = {
                    "method": request.method,
                    "route_class": _route_class(request.url.path),
                    "status_family": f"{status_code // 100}xx",
                }
                runtime.metrics.increment("api.requests", labels=labels)
                runtime.metrics.observe("api.duration_seconds", duration, labels=labels)
                LOGGER.info(
                    "request_completed",
                    extra={
                        "event_name": "api.request.completed",
                        "result": "success" if status_code < 500 else "failure",
                        "duration_ms": round(duration * 1000, 3),
                    },
                )
            response.headers["X-Request-Id"] = request_id
            response.headers["X-Correlation-Id"] = correlation_id
            response.headers["X-Content-Type-Options"] = "nosniff"
            response.headers["Cache-Control"] = "no-store"
            return response


def _install_error_handlers(application: FastAPI) -> None:
    @application.exception_handler(PlatformError)
    async def platform_error_handler(request: Request, error: PlatformError) -> JSONResponse:
        del request
        LOGGER.warning(
            "platform_request_error",
            extra={
                "event_name": "api.request.platform_error",
                "error_code": error.descriptor.code,
                "result": "failure",
            },
        )
        return _problem_response(error, status_code=503)

    @application.exception_handler(StarletteHTTPException)
    async def http_error_handler(request: Request, error: StarletteHTTPException) -> JSONResponse:
        del request
        body = _problem_body(
            code=f"SYSTEM-HTTP-{error.status_code}",
            title="请求无法处理",
            detail="请求的资源或操作不可用。",
            status_code=error.status_code,
            retryable=False,
        )
        return JSONResponse(
            body, status_code=error.status_code, media_type="application/problem+json"
        )

    @application.exception_handler(Exception)
    async def unhandled_error_handler(request: Request, error: Exception) -> JSONResponse:
        del request
        LOGGER.exception(
            "unhandled_request_error",
            exc_info=error,
            extra={"event_name": "api.request.unhandled_error", "error_code": "SYSTEM-001"},
        )
        return _problem_response(PlatformError(cause=error), status_code=500)


def _install_health_routes(application: FastAPI, runtime: PlatformRuntime) -> None:
    @application.get("/health/live", tags=["health"])
    async def live() -> dict[str, str]:
        return {"status": "live"}

    @application.get("/health/ready", tags=["health"])
    async def ready() -> JSONResponse:
        result = await runtime.health.readiness()
        status_code = 200 if result.ready else 503
        status = "ready" if result.ready else "not_ready"
        return JSONResponse({"status": status}, status_code=status_code)


def _problem_response(error: PlatformError, *, status_code: int) -> JSONResponse:
    descriptor = error.descriptor
    return JSONResponse(
        _problem_body(
            code=descriptor.code,
            title=descriptor.title,
            detail=descriptor.detail,
            status_code=status_code,
            retryable=descriptor.retryable,
        ),
        status_code=status_code,
        media_type="application/problem+json",
    )


def _problem_body(
    *,
    code: str,
    title: str,
    detail: str,
    status_code: int,
    retryable: bool,
) -> dict[str, object]:
    context = current_trace_context()
    request_id = context.request_id if context else accepted_identifier(None)
    correlation_id = context.correlation_id if context else accepted_identifier(None)
    return {
        "type": f"urn:ai-bazi:problem:{code.lower()}",
        "title": title,
        "status": status_code,
        "detail": detail,
        "instance": f"urn:ai-bazi:request:{request_id}",
        "code": code,
        "requestId": request_id,
        "correlationId": correlation_id,
        "retryable": retryable,
    }


def _route_class(path: str) -> str:
    if path.startswith("/health/"):
        return "health"
    return "unmatched"


app = create_app()


def run() -> None:
    uvicorn.run(
        "ai_bazi_api.main:app",
        host="127.0.0.1",
        port=8000,
        log_config=None,
        access_log=False,
    )
