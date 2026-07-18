import pytest
from ai_bazi_backend.platform.cache import NullCache, validate_cache_key


@pytest.mark.asyncio
async def test_disabled_cache_is_always_a_safe_miss() -> None:
    cache = NullCache()

    assert await cache.get("context:resource:version") is None
    await cache.set("context:resource:version", b"value", ttl_seconds=10)
    await cache.delete("context:resource:version")

    with pytest.raises(ValueError, match="TTL"):
        await cache.set("context:resource:version", b"value", ttl_seconds=0)


@pytest.mark.parametrize("key", ["", "contains space", "birth=1990-01-01", "x" * 251])
def test_cache_keys_must_be_opaque_and_bounded(key: str) -> None:
    with pytest.raises(ValueError):
        validate_cache_key(key)
