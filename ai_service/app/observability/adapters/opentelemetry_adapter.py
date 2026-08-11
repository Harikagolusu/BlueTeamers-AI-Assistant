import logging
from typing import Dict, Any, Optional
from app.observability.interfaces.metrics import BaseMetricsService
from app.observability.interfaces.tracing import BaseTracingService

logger = logging.getLogger("app.observability.adapters.opentelemetry")

class OpenTelemetryMetricsAdapter(BaseMetricsService):
    """
    OpenTelemetry implementation of BaseMetricsService.
    Currently a safe no-op placeholder until the full OTEL collector is integrated.
    """
    def __init__(self):
        logger.warning("OpenTelemetryMetricsAdapter initialized as a no-op placeholder.")

    def increment_counter(self, name: str, value: float = 1.0, labels: Optional[Dict[str, str]] = None) -> None:
        pass

    def observe_histogram(self, name: str, value: float, labels: Optional[Dict[str, str]] = None) -> None:
        pass

    def set_gauge(self, name: str, value: float, labels: Optional[Dict[str, str]] = None) -> None:
        pass

    def increment_gauge(self, name: str, value: float = 1.0, labels: Optional[Dict[str, str]] = None) -> None:
        pass

    def decrement_gauge(self, name: str, value: float = 1.0, labels: Optional[Dict[str, str]] = None) -> None:
        pass

    def get_registered_metrics_count(self) -> int:
        return 0


class OpenTelemetryTracingAdapter(BaseTracingService):
    """
    OpenTelemetry implementation of BaseTracingService.
    Currently a safe no-op placeholder until the full OTEL collector is integrated.
    """
    def __init__(self):
        logger.warning("OpenTelemetryTracingAdapter initialized as a no-op placeholder.")

    def generate_trace_id(self) -> str:
        # Fallback to random hex if we need a string format
        import uuid
        return uuid.uuid4().hex

    def generate_span_id(self) -> str:
        import uuid
        return uuid.uuid4().hex[:16]

    def set_trace_context(self, trace_id: str, span_id: str) -> None:
        pass

    def get_current_trace_id(self) -> Optional[str]:
        return None

    def get_current_span_id(self) -> Optional[str]:
        return None
