import logging
from dataclasses import dataclass, field

import pytest
from ai_bazi_backend.platform.worker import WorkerFramework


@dataclass
class FakeComponent:
    name: str
    events: list[str] = field(default_factory=list)
    fail_startup: bool = False

    async def startup(self) -> None:
        self.events.append(f"{self.name}:start")
        if self.fail_startup:
            raise RuntimeError("startup failed")

    async def shutdown(self) -> None:
        self.events.append(f"{self.name}:stop")


@pytest.mark.asyncio
async def test_worker_components_stop_in_reverse_order() -> None:
    events: list[str] = []
    first = FakeComponent("first", events)
    second = FakeComponent("second", events)
    framework = WorkerFramework([first, second], logger=logging.getLogger("test"))

    await framework.startup()
    await framework.shutdown()

    assert events == ["first:start", "second:start", "second:stop", "first:stop"]


@pytest.mark.asyncio
async def test_worker_cleans_up_started_components_after_startup_failure() -> None:
    events: list[str] = []
    first = FakeComponent("first", events)
    second = FakeComponent("second", events, fail_startup=True)
    framework = WorkerFramework([first, second], logger=logging.getLogger("test"))

    with pytest.raises(RuntimeError, match="startup failed"):
        await framework.startup()

    assert events == ["first:start", "second:start", "first:stop"]
