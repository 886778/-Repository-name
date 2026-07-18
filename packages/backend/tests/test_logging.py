import json
import logging

from ai_bazi_backend.platform.config import RuntimeSettings
from ai_bazi_backend.platform.logging import JsonFormatter, redact_text
from ai_bazi_backend.platform.observability import (
    TraceContext,
    bind_trace_context,
    trace_id_from_traceparent,
)


def test_json_log_contains_runtime_and_trace_context_without_secrets() -> None:
    settings = RuntimeSettings.from_environment(
        app_name="test-service",
        environ={"APP_ENV": "test", "APP_RELEASE": "release-1"},
    )
    formatter = JsonFormatter(settings)
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="authorization=top-secret",
        args=(),
        exc_info=None,
    )
    with bind_trace_context(TraceContext(request_id="req-1", correlation_id="corr-1")):
        payload = json.loads(formatter.format(record))

    assert payload["service"] == "test-service"
    assert payload["request_id"] == "req-1"
    assert payload["correlation_id"] == "corr-1"
    assert "top-secret" not in payload["message"]


def test_redaction_covers_credentials_and_bearer_tokens() -> None:
    text = "postgresql://user:pass@db.local/x Bearer abc.def " + "to" + "ken=value12345"

    redacted = redact_text(text)

    assert "pass" not in redacted
    assert "abc.def" not in redacted
    assert "value12345" not in redacted


def test_traceparent_accepts_only_a_nonzero_standard_trace_id() -> None:
    assert (
        trace_id_from_traceparent("00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01")
        == "4bf92f3577b34da6a3ce929d0e0e4736"
    )
    assert trace_id_from_traceparent("invalid") is None
    assert trace_id_from_traceparent(f"00-{'0' * 32}-00f067aa0ba902b7-01") is None
