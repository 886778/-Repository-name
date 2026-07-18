from ai_bazi_backend.platform.config import RuntimeSettings
from ai_bazi_backend.platform.logging import configure_logging


def configure_runtime(app_name: str) -> RuntimeSettings:
    settings = RuntimeSettings.from_environment(app_name=app_name)
    configure_logging(settings)
    return settings


__all__ = ["configure_runtime"]
