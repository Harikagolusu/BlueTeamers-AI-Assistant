import logging
from typing import Dict, Optional, Any

from app.observability.interfaces.metrics import BaseMetricsService
from app.observability.interfaces.tracing import BaseTracingService
from app.core.config import settings

logger = logging.getLogger("app.observability")

class ObservabilityService:
    """
    Facade for all observability operations.
    Combines metrics, tracing, and logging to simplify dependency injection.
    """
    def __init__(self, metrics: BaseMetricsService, tracing: BaseTracingService):
        self.metrics = metrics
        self.tracing = tracing
        self.enabled = settings.OBSERVABILITY_ENABLED
        self.metrics_enabled = settings.METRICS_ENABLED
        self.tracing_enabled = settings.TRACING_ENABLED

    # --- Tracing ---
    def set_trace_context(self, trace_id: str, span_id: str) -> None:
        if self.tracing_enabled:
            self.tracing.set_trace_context(trace_id, span_id)

    def get_trace_context(self) -> Dict[str, Optional[str]]:
        if self.tracing_enabled:
            return self.tracing.get_trace_context()
        return {"trace_id": None, "span_id": None}

    def generate_trace_id(self) -> str:
        return self.tracing.generate_trace_id()

    def generate_span_id(self) -> str:
        return self.tracing.generate_span_id()

    # --- Metrics ---
    def increment_counter(self, name: str, value: float = 1.0, labels: Optional[Dict[str, str]] = None) -> None:
        if self.metrics_enabled:
            self.metrics.increment_counter(name, value, labels)

    def set_gauge(self, name: str, value: float, labels: Optional[Dict[str, str]] = None) -> None:
        if self.metrics_enabled:
            self.metrics.set_gauge(name, value, labels)

    def increment_gauge(self, name: str, value: float = 1.0, labels: Optional[Dict[str, str]] = None) -> None:
        if self.metrics_enabled:
            self.metrics.increment_gauge(name, value, labels)

    def decrement_gauge(self, name: str, value: float = 1.0, labels: Optional[Dict[str, str]] = None) -> None:
        if self.metrics_enabled:
            self.metrics.decrement_gauge(name, value, labels)

    def observe_histogram(self, name: str, value: float, labels: Optional[Dict[str, str]] = None) -> None:
        if self.metrics_enabled:
            self.metrics.observe_histogram(name, value, labels)

    def get_registered_metrics_count(self) -> int:
        return self.metrics.get_registered_metrics_count()

    # --- Logging ---
    def log_info(self, message: str, **kwargs: Any) -> None:
        """Log an info message with trace context automatically appended by the JSON formatter."""
        if self.enabled:
            logger.info(message, extra=kwargs)

    def log_warning(self, message: str, **kwargs: Any) -> None:
        """Log a warning message with trace context automatically appended."""
        if self.enabled:
            logger.warning(message, extra=kwargs)

    def log_error(self, message: str, exc: Optional[Exception] = None, **kwargs: Any) -> None:
        if self.enabled:
            logger.error(message, exc_info=exc, extra=kwargs)
