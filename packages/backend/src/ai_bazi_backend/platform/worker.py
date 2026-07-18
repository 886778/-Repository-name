import logging
from collections.abc import Sequence
from typing import Protocol


class LifecycleComponent(Protocol):
    name: str

    async def startup(self) -> None: ...

    async def shutdown(self) -> None: ...


class WorkerFramework:
    """Lifecycle foundation only; no broker or business task dispatch."""

    def __init__(
        self,
        components: Sequence[LifecycleComponent],
        *,
        logger: logging.Logger,
    ) -> None:
        self._components = tuple(components)
        self._started: list[LifecycleComponent] = []
        self._logger = logger

    async def startup(self) -> None:
        try:
            for component in self._components:
                await component.startup()
                self._started.append(component)
        except Exception:
            await self.shutdown()
            raise
        self._logger.info("worker_framework_started", extra={"event_name": "worker.started"})

    async def shutdown(self) -> None:
        while self._started:
            component = self._started.pop()
            try:
                await component.shutdown()
            except Exception:
                self._logger.exception(
                    "worker_component_shutdown_failed",
                    extra={
                        "event_name": "worker.component.shutdown_failed",
                        "dependency": component.name,
                        "result": "failure",
                    },
                )
        self._logger.info("worker_framework_stopped", extra={"event_name": "worker.stopped"})


__all__ = ["LifecycleComponent", "WorkerFramework"]
