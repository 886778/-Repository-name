import asyncio
from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol


class HealthStatus(StrEnum):
    UP = "up"
    DOWN = "down"


class HealthDependency(Protocol):
    name: str

    async def ping(self) -> bool: ...


@dataclass(frozen=True, slots=True)
class HealthCheck:
    dependency: HealthDependency
    critical: bool


@dataclass(frozen=True, slots=True)
class HealthResult:
    status: HealthStatus
    checks: dict[str, HealthStatus]

    @property
    def ready(self) -> bool:
        return self.status is HealthStatus.UP


class HealthRegistry:
    def __init__(self) -> None:
        self._checks: list[HealthCheck] = []

    def register(self, dependency: HealthDependency, *, critical: bool) -> None:
        if any(item.dependency.name == dependency.name for item in self._checks):
            raise ValueError("health dependency name must be unique")
        self._checks.append(HealthCheck(dependency=dependency, critical=critical))

    async def readiness(self) -> HealthResult:
        if not self._checks:
            return HealthResult(status=HealthStatus.UP, checks={})
        states = await asyncio.gather(*(item.dependency.ping() for item in self._checks))
        checks = {
            item.dependency.name: HealthStatus.UP if state else HealthStatus.DOWN
            for item, state in zip(self._checks, states, strict=True)
        }
        critical_failure = any(
            item.critical and checks[item.dependency.name] is HealthStatus.DOWN
            for item in self._checks
        )
        return HealthResult(
            status=HealthStatus.DOWN if critical_failure else HealthStatus.UP,
            checks=checks,
        )


__all__ = ["HealthRegistry", "HealthResult", "HealthStatus"]
