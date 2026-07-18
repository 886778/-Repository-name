from dataclasses import dataclass

import pytest
from ai_bazi_backend.platform.health import HealthRegistry, HealthStatus


@dataclass
class FakeDependency:
    name: str
    available: bool

    async def ping(self) -> bool:
        return self.available


@pytest.mark.asyncio
async def test_critical_dependency_controls_readiness() -> None:
    registry = HealthRegistry()
    registry.register(FakeDependency("postgresql", False), critical=True)
    registry.register(FakeDependency("redis", False), critical=False)

    result = await registry.readiness()

    assert result.status is HealthStatus.DOWN
    assert not result.ready
    assert result.checks == {
        "postgresql": HealthStatus.DOWN,
        "redis": HealthStatus.DOWN,
    }


@pytest.mark.asyncio
async def test_optional_dependency_degrades_without_failing_readiness() -> None:
    registry = HealthRegistry()
    registry.register(FakeDependency("redis", False), critical=False)

    result = await registry.readiness()

    assert result.ready
