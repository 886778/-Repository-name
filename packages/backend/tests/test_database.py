from types import TracebackType

import pytest
from ai_bazi_backend.platform.config import DatabaseSettings
from ai_bazi_backend.platform.database import PostgresDatabase
from ai_bazi_backend.platform.errors import DependencyUnavailableError


class FakeTransactionContext:
    async def __aenter__(self) -> None:
        return None

    async def __aexit__(
        self,
        exception_type: type[BaseException] | None,
        exception: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        del exception_type, exception, traceback


class FakeConnection:
    def transaction(self) -> FakeTransactionContext:
        return FakeTransactionContext()

    async def execute(self, statement: str, *parameters: object) -> str:
        del statement, parameters
        return "OK"

    async def fetchval(self, statement: str, *parameters: object) -> object:
        del statement, parameters
        return 1


class FakeAcquireContext:
    def __init__(self, connection: FakeConnection) -> None:
        self._connection = connection

    async def __aenter__(self) -> FakeConnection:
        return self._connection

    async def __aexit__(
        self,
        exception_type: type[BaseException] | None,
        exception: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        del exception_type, exception, traceback


class FakePool:
    def __init__(self) -> None:
        self.connection = FakeConnection()
        self.closed = False

    async def fetchval(self, statement: str) -> object:
        del statement
        return 1

    def acquire(self) -> FakeAcquireContext:
        return FakeAcquireContext(self.connection)

    async def close(self) -> None:
        self.closed = True


@pytest.mark.asyncio
async def test_postgres_runtime_lifecycle_and_transaction(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    pool = FakePool()

    async def create_pool(**options: object) -> FakePool:
        assert options["max_size"] == 2
        return pool

    monkeypatch.setattr("ai_bazi_backend.platform.database.asyncpg.create_pool", create_pool)
    database = PostgresDatabase(
        DatabaseSettings(url="postgresql://localhost/platform", pool_size=2)
    )

    await database.startup()
    assert await database.ping()
    async with database.transaction() as transaction:
        assert await transaction.execute("SELECT 1") == "OK"
        assert await transaction.fetch_value("SELECT 1") == 1
    await database.shutdown()

    assert pool.closed


@pytest.mark.asyncio
async def test_transaction_fails_safely_before_startup() -> None:
    database = PostgresDatabase(DatabaseSettings(url="postgresql://localhost/platform"))

    with pytest.raises(DependencyUnavailableError):
        async with database.transaction():
            pytest.fail("transaction should not start")
