import asyncio
import logging
import signal
from collections.abc import Callable

from ai_bazi_backend.bootstrap import configure_runtime

LOGGER = logging.getLogger("ai_bazi.worker")


async def run_worker(stop_event: asyncio.Event | None = None) -> None:
    configure_runtime("ai-bazi-worker")
    event = stop_event or asyncio.Event()
    loop = asyncio.get_running_loop()

    if stop_event is None:
        stop: Callable[[], None] = event.set
        for signal_name in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(signal_name, stop)

    LOGGER.info("worker_started")
    await event.wait()
    LOGGER.info("worker_stopped")


def main() -> None:
    asyncio.run(run_worker())
