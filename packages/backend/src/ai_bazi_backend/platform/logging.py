import json
import logging
import re
from datetime import UTC, datetime
from typing import Any, Final

from ai_bazi_backend.platform.config import RuntimeSettings
from ai_bazi_backend.platform.observability import current_trace_context

SENSITIVE_PATTERNS: Final = (
    re.compile(r"(?i)(authorization|token|password|secret|api[_-]?key)=([^\s&]+)"),
    re.compile(r"(?i)(postgres(?:ql)?|redis)://[^\s/@:]+:[^\s/@]+@"),
    re.compile(r"(?i)bearer\s+[A-Za-z0-9._~+/=-]+"),
)


def redact_text(value: str) -> str:
    redacted = value
    for pattern in SENSITIVE_PATTERNS:
        if "bearer" in pattern.pattern.lower():
            redacted = pattern.sub("Bearer [REDACTED]", redacted)
        elif "postgres" in pattern.pattern.lower():
            redacted = pattern.sub(r"\1://[REDACTED]@", redacted)
        else:
            redacted = pattern.sub(r"\1=[REDACTED]", redacted)
    return redacted


class JsonFormatter(logging.Formatter):
    def __init__(self, settings: RuntimeSettings) -> None:
        super().__init__()
        self._settings = settings

    def format(self, record: logging.LogRecord) -> str:
        context = current_trace_context()
        payload: dict[str, Any] = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "service": self._settings.app_name,
            "environment": self._settings.environment.value,
            "release": self._settings.release,
            "logger": record.name,
            "event_name": getattr(record, "event_name", record.getMessage()),
            "message": redact_text(record.getMessage()),
        }
        if context is not None:
            payload.update(
                request_id=context.request_id,
                correlation_id=context.correlation_id,
            )
            if context.trace_id is not None:
                payload["trace_id"] = context.trace_id
        for field in ("result", "error_code", "duration_ms", "dependency"):
            value = getattr(record, field, None)
            if value is not None:
                payload[field] = value
        if record.exc_info:
            exception_type = record.exc_info[0]
            payload["exception_type"] = (
                exception_type.__name__ if exception_type is not None else "UnknownError"
            )
        return json.dumps(payload, ensure_ascii=False, separators=(",", ":"))


def configure_logging(settings: RuntimeSettings) -> None:
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter(settings))
    logging.basicConfig(
        level=settings.log_level,
        handlers=[handler],
        force=True,
    )


__all__ = ["JsonFormatter", "configure_logging", "redact_text"]
