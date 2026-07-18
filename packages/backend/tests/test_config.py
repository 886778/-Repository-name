import pytest
from ai_bazi_backend.platform.config import Environment, RuntimeSettings
from ai_bazi_backend.platform.errors import ConfigurationError


def test_runtime_settings_are_typed_and_hide_connection_secrets() -> None:
    settings = RuntimeSettings.from_environment(
        app_name="test-service",
        environ={
            "APP_ENV": "test",
            "APP_RELEASE": "test-release",
            "DATABASE_URL": "postgresql://user:secret@localhost/platform",
            "REDIS_URL": "redis://:secret@localhost/0",
            "DATABASE_POOL_SIZE": "3",
        },
    )

    assert settings.environment is Environment.TEST
    assert settings.database.enabled
    assert settings.database.pool_size == 3
    assert settings.cache.enabled
    assert "secret" not in repr(settings)


@pytest.mark.parametrize(
    "environ",
    [
        {"APP_ENV": "invalid"},
        {"LOG_LEVEL": "verbose"},
        {"DATABASE_URL": "mysql://localhost/platform"},
        {"REDIS_URL": "https://localhost/cache"},
        {"DATABASE_POOL_SIZE": "0"},
        {"CACHE_KEY_PREFIX": "contains space"},
        {"APP_ENV": "production", "APP_RELEASE": "release-1"},
    ],
)
def test_invalid_or_unsafe_configuration_fails_closed(environ: dict[str, str]) -> None:
    with pytest.raises(ConfigurationError):
        RuntimeSettings.from_environment(app_name="test-service", environ=environ)
