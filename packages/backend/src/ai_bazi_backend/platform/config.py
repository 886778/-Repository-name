import os
from dataclasses import dataclass
from typing import Final

DEFAULT_ENVIRONMENT: Final = "local"
DEFAULT_LOG_LEVEL: Final = "INFO"


@dataclass(frozen=True, slots=True)
class RuntimeSettings:
    app_name: str
    environment: str
    log_level: str

    @classmethod
    def from_environment(cls, *, app_name: str) -> RuntimeSettings:
        return cls(
            app_name=app_name,
            environment=os.getenv("APP_ENV", DEFAULT_ENVIRONMENT),
            log_level=os.getenv("LOG_LEVEL", DEFAULT_LOG_LEVEL).upper(),
        )
