import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Protocol, cast

import asyncpg

from ai_bazi_backend.platform.config import DatabaseSettings
from ai_bazi_backend.platform.errors import DependencyUnavailableError


class DatabaseTransaction(Protocol):
    async def execute(self, statement: str, *parameters: object) -> str: ...

    async def fetch_value(self, statement: str, *parameters: object) -> object: ...


class _AsyncpgTransaction:
    def __init__(self, connection: asyncpg.Connection) -> None:
        self._connection = connection

    async def execute(self, statement: str, *parameters: object) -> str:
        return cast(str, await self._connection.execute(statement, *parameters))

    async def fetch_value(self, statement: str, *parameters: object) -> object:
        return await self._connection.fetchval(statement, *parameters)


class PostgresDatabase:
    """PostgreSQL runtime adapter; it owns no schema or repository mapping."""

    name = "postgresql"

    def __init__(self, settings: DatabaseSettings) -> None:
        if settings.url is None:
            raise ValueError("PostgreSQL adapter requires an enabled database configuration")
        self._settings = settings
        self._pool: asyncpg.Pool | None = None

    async def startup(self) -> None:
        if self._pool is not None:
            return
        try:
            self._pool = await asyncpg.create_pool(
                dsn=self._settings.url,
                min_size=1,
                max_size=self._settings.pool_size,
                timeout=self._settings.timeout_seconds,
                command_timeout=self._settings.timeout_seconds,
            )
        except (OSError, asyncpg.PostgresError, TimeoutError) as exc:
            raise DependencyUnavailableError(cause=exc) from exc

    async def shutdown(self) -> None:
        pool, self._pool = self._pool, None
        if pool is not None:
            await pool.close()

    async def ping(self) -> bool:
        if self._pool is None:
            return False
        try:
            result = cast(
                object,
                await asyncio.wait_for(
                    self._pool.fetchval("SELECT 1"),
                    timeout=self._settings.timeout_seconds,
                ),
            )
        except (OSError, asyncpg.PostgresError, TimeoutError):
            return False
        return result == 1

    @asynccontextmanager
    async def transaction(self) -> AsyncIterator[DatabaseTransaction]:
        if self._pool is None:
            raise DependencyUnavailableError()
        try:
            async with self._pool.acquire() as connection, connection.transaction():
                yield _AsyncpgTransaction(connection)
        except (OSError, asyncpg.PostgresError, TimeoutError) as exc:
            raise DependencyUnavailableError(cause=exc) from exc


__all__ = ["DatabaseTransaction", "PostgresDatabase"]
