import asyncio
import logging
import signal
from collections.abc import Callable, Mapping

from ai_bazi_backend.bootstrap import build_runtime
from ai_bazi_backend.platform.worker import WorkerFramework

LOGGER = logging.getLogger("ai_bazi.worker")


async def run_worker(
    stop_event: asyncio.Event | None = None,
    *,
    environ: Mapping[str, str] | None = None,
) -> None:
    platform_runtime = build_runtime("ai-bazi-worker", environ=environ)
    framework = WorkerFramework([platform_runtime], logger=LOGGER)
    event = stop_event or asyncio.Event()
    loop = asyncio.get_running_loop()

    if stop_event is None:
        stop: Callable[[], None] = event.set
        for signal_name in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(signal_name, stop)

    await framework.startup()
    try:
        await event.wait()
    finally:
        await framework.shutdown()


def main() -> None:
    asyncio.run(run_worker())
