from typing import Final

import uvicorn
from ai_bazi_backend.bootstrap import configure_runtime
from fastapi import FastAPI

APP_NAME: Final = "ai-bazi-api"


def create_app() -> FastAPI:
    configure_runtime(APP_NAME)
    application = FastAPI(
        title="AI Bazi Platform Health API",
        version="0.0.0",
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
    )

    @application.get("/health/live", tags=["health"])
    async def live() -> dict[str, str]:
        return {"status": "live"}

    @application.get("/health/ready", tags=["health"])
    async def ready() -> dict[str, str]:
        return {"status": "ready"}

    return application


app = create_app()


def run() -> None:
    uvicorn.run("ai_bazi_api.main:app", host="127.0.0.1", port=8000)
