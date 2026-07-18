import logging
import os
import re
from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Final
from urllib.parse import urlsplit

from ai_bazi_backend.platform.errors import ConfigurationError

DEFAULT_ENVIRONMENT: Final = "local"
DEFAULT_LOG_LEVEL: Final = "INFO"
DEFAULT_RELEASE: Final = "development"
DEFAULT_DATABASE_POOL_SIZE: Final = 5
DEFAULT_DEPENDENCY_TIMEOUT_SECONDS: Final = 2.0
SUPPORTED_LOG_LEVELS: Final = frozenset(logging.getLevelNamesMapping())
CACHE_PREFIX_PATTERN: Final = re.compile(r"^[A-Za-z0-9][A-Za-z0-9:._-]{0,63}$")


class Environment(StrEnum):
    LOCAL = "local"
    TEST = "test"
    STAGING = "staging"
    PRODUCTION = "production"


@dataclass(frozen=True, slots=True)
class DatabaseSettings:
    url: str | None = field(default=None, repr=False)
    pool_size: int = DEFAULT_DATABASE_POOL_SIZE
    timeout_seconds: float = DEFAULT_DEPENDENCY_TIMEOUT_SECONDS

    @property
    def enabled(self) -> bool:
        return self.url is not None


@dataclass(frozen=True, slots=True)
class CacheSettings:
    url: str | None = field(default=None, repr=False)
    key_prefix: str = "ai-bazi"
    timeout_seconds: float = DEFAULT_DEPENDENCY_TIMEOUT_SECONDS

    @property
    def enabled(self) -> bool:
        return self.url is not None


@dataclass(frozen=True, slots=True)
class RuntimeSettings:
    app_name: str
    environment: Environment
    release: str
    log_level: str
    database: DatabaseSettings
    cache: CacheSettings

    @classmethod
    def from_environment(
        cls,
        *,
        app_name: str,
        environ: Mapping[str, str] | None = None,
    ) -> RuntimeSettings:
        source = os.environ if environ is None else environ
        try:
            settings = cls(
                app_name=_required_text(app_name),
                environment=Environment(source.get("APP_ENV", DEFAULT_ENVIRONMENT).lower()),
                release=_required_text(source.get("APP_RELEASE", DEFAULT_RELEASE)),
                log_level=_log_level(source.get("LOG_LEVEL", DEFAULT_LOG_LEVEL)),
                database=DatabaseSettings(
                    url=_optional_url(source.get("DATABASE_URL"), {"postgres", "postgresql"}),
                    pool_size=_positive_int(
                        source.get("DATABASE_POOL_SIZE"), DEFAULT_DATABASE_POOL_SIZE
                    ),
                    timeout_seconds=_positive_float(
                        source.get("DATABASE_TIMEOUT_SECONDS"),
                        DEFAULT_DEPENDENCY_TIMEOUT_SECONDS,
                    ),
                ),
                cache=CacheSettings(
                    url=_optional_url(source.get("REDIS_URL"), {"redis", "rediss"}),
                    key_prefix=_cache_prefix(source.get("CACHE_KEY_PREFIX", "ai-bazi")),
                    timeout_seconds=_positive_float(
                        source.get("CACHE_TIMEOUT_SECONDS"),
                        DEFAULT_DEPENDENCY_TIMEOUT_SECONDS,
                    ),
                ),
            )
        except (TypeError, ValueError) as exc:
            raise ConfigurationError(cause=exc) from exc
        settings._validate_environment_requirements()
        return settings

    def _validate_environment_requirements(self) -> None:
        if self.environment in {Environment.STAGING, Environment.PRODUCTION}:
            if not self.database.enabled:
                raise ConfigurationError()
            if self.release == DEFAULT_RELEASE:
                raise ConfigurationError()


def _required_text(value: str) -> str:
    normalized = value.strip()
    if not normalized or len(normalized) > 128:
        raise ValueError("text setting is empty or too long")
    return normalized


def _log_level(value: str) -> str:
    normalized = value.upper()
    if normalized not in SUPPORTED_LOG_LEVELS:
        raise ValueError("unsupported log level")
    return normalized


def _optional_url(value: str | None, schemes: set[str]) -> str | None:
    if value is None or not value.strip():
        return None
    normalized = value.strip()
    parsed = urlsplit(normalized)
    if parsed.scheme not in schemes or not parsed.hostname:
        raise ValueError("invalid dependency URL")
    return normalized


def _positive_int(value: str | None, default: int) -> int:
    result = default if value is None else int(value)
    if result <= 0:
        raise ValueError("value must be positive")
    return result


def _cache_prefix(value: str) -> str:
    normalized = value.strip()
    if not CACHE_PREFIX_PATTERN.fullmatch(normalized):
        raise ValueError("invalid cache key prefix")
    return normalized


def _positive_float(value: str | None, default: float) -> float:
    result = default if value is None else float(value)
    if result <= 0:
        raise ValueError("value must be positive")
    return result


__all__ = [
    "CacheSettings",
    "DatabaseSettings",
    "Environment",
    "RuntimeSettings",
]
