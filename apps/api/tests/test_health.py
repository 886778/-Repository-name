from typing import cast

import pytest
from ai_bazi_api.main import app, create_app
from ai_bazi_backend.bootstrap import PlatformRuntime
from ai_bazi_backend.platform.errors import DependencyUnavailableError
from ai_bazi_backend.platform.observability import InMemoryMetricsRecorder
from httpx import ASGITransport, AsyncClient


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("path", "expected_status"),
    [
        ("/health/live", "live"),
        ("/health/ready", "ready"),
    ],
)
async def test_health_endpoint(path: str, expected_status: str) -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get(path)

    assert response.status_code == 200
    assert response.json() == {"status": expected_status}


@pytest.mark.asyncio
@pytest.mark.parametrize("path", ["/docs", "/redoc", "/openapi.json"])
async def test_framework_documentation_endpoints_are_disabled(path: str) -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get(path)

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_request_and_correlation_ids_are_validated_and_returned() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get(
            "/health/live",
            headers={"X-Request-Id": "request-1", "X-Correlation-Id": "invalid value"},
        )

    assert response.headers["X-Request-Id"] == "request-1"
    assert response.headers["X-Correlation-Id"] != "invalid value"
    assert response.headers["Cache-Control"] == "no-store"


@pytest.mark.asyncio
async def test_http_errors_use_safe_problem_details() -> None:
    application = create_app(environ={"APP_ENV": "test", "APP_RELEASE": "test"})
    transport = ASGITransport(app=application)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/missing")

    body = response.json()
    assert response.status_code == 404
    assert response.headers["content-type"] == "application/problem+json"
    assert body["code"] == "SYSTEM-HTTP-404"
    assert body["requestId"] == response.headers["X-Request-Id"]


@pytest.mark.asyncio
async def test_platform_errors_are_safe_and_correlated() -> None:
    application = create_app(environ={"APP_ENV": "test", "APP_RELEASE": "test"})

    async def fail() -> None:
        raise DependencyUnavailableError(cause=RuntimeError("internal-only detail"))

    application.add_api_route("/_test/fail", fail, include_in_schema=False)
    transport = ASGITransport(app=application)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/_test/fail")

    assert response.status_code == 503
    assert response.json()["code"] == "SYSTEM-DEPENDENCY-001"
    assert "internal-only" not in response.text


@pytest.mark.asyncio
async def test_api_records_bounded_technical_metrics() -> None:
    metrics = InMemoryMetricsRecorder()
    application = create_app(
        environ={"APP_ENV": "test", "APP_RELEASE": "test"},
        metrics=metrics,
    )
    transport = ASGITransport(app=application)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health/live")

    assert response.status_code == 200
    assert sum(metrics.counters.values()) == 1
    assert sum(len(values) for values in metrics.observations.values()) == 1


@pytest.mark.asyncio
async def test_critical_dependency_failure_makes_api_not_ready() -> None:
    application = create_app(environ={"APP_ENV": "test", "APP_RELEASE": "test"})
    runtime = cast(PlatformRuntime, application.state.runtime)

    class DownDependency:
        name = "postgresql-test"

        async def ping(self) -> bool:
            return False

    runtime.health.register(DownDependency(), critical=True)
    transport = ASGITransport(app=application)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health/ready")

    assert response.status_code == 503
    assert response.json() == {"status": "not_ready"}
