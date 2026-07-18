import asyncio
import re
from typing import Protocol

from redis.asyncio import Redis
from redis.exceptions import RedisError

from ai_bazi_backend.platform.config import CacheSettings
from ai_bazi_backend.platform.errors import DependencyUnavailableError

CACHE_KEY_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9:._-]{0,249}$")


class Cache(Protocol):
    async def get(self, key: str) -> bytes | None: ...

    async def set(self, key: str, value: bytes, *, ttl_seconds: int) -> None: ...

    async def delete(self, key: str) -> None: ...


def validate_cache_key(key: str) -> str:
    if not CACHE_KEY_PATTERN.fullmatch(key):
        raise ValueError("cache key must be opaque, bounded, and namespaced")
    return key


class NullCache:
    name = "cache-disabled"

    async def startup(self) -> None:
        return None

    async def shutdown(self) -> None:
        return None

    async def ping(self) -> bool:
        return False

    async def get(self, key: str) -> bytes | None:
        validate_cache_key(key)
        return None

    async def set(self, key: str, value: bytes, *, ttl_seconds: int) -> None:
        validate_cache_key(key)
        if ttl_seconds <= 0:
            raise ValueError("cache TTL must be positive")
        del value

    async def delete(self, key: str) -> None:
        validate_cache_key(key)


class RedisCache:
    """Redis cache-aside adapter. Redis is never a source of truth."""

    name = "redis"

    def __init__(self, settings: CacheSettings) -> None:
        url = settings.url
        if url is None:
            raise ValueError("Redis adapter requires an enabled cache configuration")
        self._settings = settings
        self._url = url
        self._client: Redis | None = None

    async def startup(self) -> None:
        if self._client is None:
            self._client = Redis.from_url(
                self._url,
                decode_responses=False,
                socket_connect_timeout=self._settings.timeout_seconds,
                socket_timeout=self._settings.timeout_seconds,
            )

    async def shutdown(self) -> None:
        client, self._client = self._client, None
        if client is not None:
            await client.aclose()

    async def ping(self) -> bool:
        if self._client is None:
            return False
        try:
            return bool(
                await asyncio.wait_for(
                    self._client.ping(),
                    timeout=self._settings.timeout_seconds,
                )
            )
        except (OSError, RedisError, TimeoutError):
            return False

    async def get(self, key: str) -> bytes | None:
        client = self._require_client()
        try:
            value = await client.get(self._namespaced(key))
        except (OSError, RedisError, TimeoutError) as exc:
            raise DependencyUnavailableError(cause=exc) from exc
        if value is None or isinstance(value, bytes):
            return value
        raise TypeError("cache adapter must return bytes")

    async def set(self, key: str, value: bytes, *, ttl_seconds: int) -> None:
        if ttl_seconds <= 0:
            raise ValueError("cache TTL must be positive")
        client = self._require_client()
        try:
            await client.set(self._namespaced(key), value, ex=ttl_seconds)
        except (OSError, RedisError, TimeoutError) as exc:
            raise DependencyUnavailableError(cause=exc) from exc

    async def delete(self, key: str) -> None:
        client = self._require_client()
        try:
            await client.delete(self._namespaced(key))
        except (OSError, RedisError, TimeoutError) as exc:
            raise DependencyUnavailableError(cause=exc) from exc

    def _namespaced(self, key: str) -> str:
        return f"{self._settings.key_prefix}:{validate_cache_key(key)}"

    def _require_client(self) -> Redis:
        if self._client is None:
            raise RuntimeError("cache adapter is not started")
        return self._client


__all__ = ["Cache", "NullCache", "RedisCache", "validate_cache_key"]
