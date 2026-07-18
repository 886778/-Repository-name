import json
import logging
from datetime import UTC, datetime
from typing import Any

from ai_bazi_backend.platform.config import RuntimeSettings


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        return json.dumps(payload, ensure_ascii=False)


def configure_logging(settings: RuntimeSettings) -> None:
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    logging.basicConfig(
        level=settings.log_level,
        handlers=[handler],
        force=True,
    )
