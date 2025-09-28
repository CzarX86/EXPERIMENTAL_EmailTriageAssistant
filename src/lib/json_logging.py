from __future__ import annotations

import json
import logging
import os
import sys
from datetime import datetime, timezone
from typing import Any


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:  # type: ignore[override]
        payload: dict[str, Any] = {
            "ts": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }
        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)
        # Extra fields passed via Logger.bind-like usage (using record.__dict__)
        for k, v in record.__dict__.items():
            if k in (
                "msg",
                "args",
                "levelname",
                "levelno",
                "pathname",
                "filename",
                "module",
                "exc_info",
                "exc_text",
                "stack_info",
                "lineno",
                "funcName",
                "created",
                "msecs",
                "relativeCreated",
                "thread",
                "threadName",
                "processName",
                "process",
                "name",
            ):
                continue
            try:
                json.dumps(v)
                payload[k] = v
            except Exception:
                payload[k] = repr(v)
        return json.dumps(payload, ensure_ascii=False)


def configure_json_logging(level: str | None = None) -> None:
    """Configure root logger to output structured JSON to stdout.

    - Level picked from env LOG_LEVEL (default INFO) unless explicitly provided.
    - Disables existing handlers to avoid duplicate logs in tests.
    """
    level_name = (level or os.getenv("LOG_LEVEL") or "INFO").upper()
    numeric_level = getattr(logging, level_name, logging.INFO)

    root = logging.getLogger()
    # Avoid duplicate handlers if called multiple times (tests/CLI/API)
    for h in list(root.handlers):
        root.removeHandler(h)

    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(JsonFormatter())

    root.setLevel(numeric_level)
    root.addHandler(handler)


__all__ = ["configure_json_logging", "JsonFormatter"]
