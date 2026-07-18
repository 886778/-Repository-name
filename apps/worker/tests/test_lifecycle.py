import asyncio

import pytest
from ai_bazi_worker.main import run_worker


@pytest.mark.asyncio
async def test_worker_starts_and_stops_without_broker() -> None:
    stop_event = asyncio.Event()
    stop_event.set()

    await run_worker(stop_event)
