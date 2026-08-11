import logging
import logging.config
import json
import sys
from pathlib import Path
from typing import Any, Dict
from contextvars import ContextVar

from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.config import settings

# Ensure logs directory exists
LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)

# Context variable to store correlation ID for the current request
request_id_var: ContextVar[str] = ContextVar("request_id", default="-")

# Observability context variables from adapter
from app.observability.adapters.tracing_adapter import trace_id_var, span_id_var

class JSONFormatter(logging.Formatter):
    """
    Custom formatter that outputs JSON strings for structured logging.
    Includes correlation ID and specific log record attributes.
    """
    def format(self, record: logging.LogRecord) -> str:
        log_obj: Dict[str, Any] = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "module": record.module,
            "function": record.funcName,
            "line_number": record.lineno,
            "request_id": request_id_var.get(),
            "trace_id": trace_id_var.get() or "-",
            "span_id": span_id_var.get() or "-",
            "environment": settings.APP_ENV,
            "deployment_mode": "development" if settings.is_development
                               else "production",
            "message": record.getMessage(),
        }

        # Add extra variables if provided dynamically via extra=kwargs
        if hasattr(record, "execution_time_ms"):
            log_obj["execution_time_ms"] = record.execution_time_ms
        if hasattr(record, "status_code"):
            log_obj["status_code"] = record.status_code
        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_obj)

def setup_logging() -> None:
    """
    Configure the root logger and specific application loggers using dictConfig.
    Sets up both console logging (human-readable) and rotating file logging (JSON).

    Level is resolved from the deployment mode in app/core/config.py:
    development -> DEBUG, production -> INFO (see LOG_LEVEL).
    """
    log_level = settings.LOG_LEVEL.upper()

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "console": {
                "format": "%(asctime)s %(levelname)s %(module)s %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "json": {
                "()": JSONFormatter,
                "datefmt": "%Y-%m-%dT%H:%M:%S%z",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "console",
                "stream": sys.stdout,
                "level": log_level,
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": str(LOGS_DIR / "app.log"),
                "maxBytes": 10 * 1024 * 1024,  # 10 MB
                "backupCount": 5,
                "formatter": "json",
                "level": log_level,
            },
        },
        "loggers": {
            "app": {
                "handlers": ["console", "file"],
                "level": log_level,
                "propagate": False,
            },
            "uvicorn": {
                "handlers": ["console", "file"],
                "level": "INFO",
                "propagate": False,
            },
            "uvicorn.access": {
                "handlers": ["console", "file"],
                "level": "INFO",
                "propagate": False,
            }
        },
        "root": {
            "handlers": ["console", "file"],
            "level": log_level,
        }
    }
    
    logging.config.dictConfig(logging_config)

logger = logging.getLogger("app")

def log_unhandled_exception(exc: Exception) -> None:
    """Helper method to log unexpected, unhandled exceptions."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=exc)

def log_validation_error(exc: RequestValidationError) -> None:
    """Helper method to log Pydantic validation errors."""
    logger.warning(f"Validation error: {exc.errors()}")

def log_http_exception(exc: StarletteHTTPException) -> None:
    """Helper method to log standard HTTP exceptions."""
    logger.warning(f"HTTP Exception: {exc.status_code} - {exc.detail}")
