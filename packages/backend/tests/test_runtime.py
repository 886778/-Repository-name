from dataclasses import dataclass, field

import pytest
from ai_bazi_backend.bootstrap import PlatformRuntime
from ai_bazi_backend.platform.cache import NullCache
from ai_bazi_backend.platform.config import RuntimeSettings
from ai_bazi_backend.platform.health import HealthRegistry
from ai_bazi_backend.platform.observability import NullMetricsRecorder


@dataclass
class FakeComponent:
    name: str
    events: list[str] = field(default_factory=list)
    fail_shutdown: bool = False

    async def startup(self) -> None:
        self.events.append(f"{self.name}:start")

    async def shutdown(self) -> None:
        self.events.append(f"{self.name}:stop")
        if self.fail_shutdown:
            raise RuntimeError(self.name)


@pytest.mark.asyncio
async def test_runtime_attempts_all_shutdowns_when_one_component_fails() -> None:
    events: list[str] = []
    first = FakeComponent("first", events)
    second = FakeComponent("second", events, fail_shutdown=True)
    settings = RuntimeSettings.from_environment(
        app_name="test-runtime",
        environ={"APP_ENV": "test", "APP_RELEASE": "test"},
    )
    runtime = PlatformRuntime(
        settings=settings,
        health=HealthRegistry(),
        metrics=NullMetricsRecorder(),
        cache=NullCache(),
        database=None,
        _components=(first, second),
    )

    await runtime.startup()
    with pytest.raises(RuntimeError, match="second"):
        await runtime.shutdown()

    assert events == ["first:start", "second:start", "second:stop", "first:stop"]
