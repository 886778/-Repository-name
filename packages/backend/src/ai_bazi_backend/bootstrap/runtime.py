from collections.abc import Mapping
from dataclasses import dataclass

from ai_bazi_backend.platform.cache import Cache, NullCache, RedisCache
from ai_bazi_backend.platform.config import RuntimeSettings
from ai_bazi_backend.platform.database import PostgresDatabase
from ai_bazi_backend.platform.health import HealthRegistry
from ai_bazi_backend.platform.logging import configure_logging
from ai_bazi_backend.platform.observability import MetricsRecorder, NullMetricsRecorder
from ai_bazi_backend.platform.worker import LifecycleComponent


@dataclass(slots=True)
class PlatformRuntime:
    name = "platform-runtime"

    settings: RuntimeSettings
    health: HealthRegistry
    metrics: MetricsRecorder
    cache: Cache
    database: PostgresDatabase | None
    _components: tuple[LifecycleComponent, ...]
    _started: bool = False

    async def startup(self) -> None:
        if self._started:
            return
        started: list[LifecycleComponent] = []
        try:
            for component in self._components:
                await component.startup()
                started.append(component)
        except Exception:
            for component in reversed(started):
                await component.shutdown()
            raise
        self._started = True

    async def shutdown(self) -> None:
        if not self._started:
            return
        first_error: Exception | None = None
        for component in reversed(self._components):
            try:
                await component.shutdown()
            except Exception as exc:
                if first_error is None:
                    first_error = exc
        self._started = False
        if first_error is not None:
            raise first_error


def configure_runtime(
    app_name: str,
    *,
    environ: Mapping[str, str] | None = None,
) -> RuntimeSettings:
    settings = RuntimeSettings.from_environment(app_name=app_name, environ=environ)
    configure_logging(settings)
    return settings


def build_runtime(
    app_name: str,
    *,
    environ: Mapping[str, str] | None = None,
    metrics: MetricsRecorder | None = None,
) -> PlatformRuntime:
    settings = configure_runtime(app_name, environ=environ)
    health = HealthRegistry()
    components: list[LifecycleComponent] = []

    database: PostgresDatabase | None = None
    if settings.database.enabled:
        database = PostgresDatabase(settings.database)
        components.append(database)
        health.register(database, critical=True)

    cache: Cache
    if settings.cache.enabled:
        redis_cache = RedisCache(settings.cache)
        cache = redis_cache
        components.append(redis_cache)
        health.register(redis_cache, critical=False)
    else:
        cache = NullCache()

    return PlatformRuntime(
        settings=settings,
        health=health,
        metrics=metrics or NullMetricsRecorder(),
        cache=cache,
        database=database,
        _components=tuple(components),
    )
