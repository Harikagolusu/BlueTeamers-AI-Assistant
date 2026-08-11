from typing import Dict, Any, Optional
import logging

from app.observability.interfaces.metrics import BaseMetricsService
from app.observability.registry import MetricsRegistry

logger = logging.getLogger("app.observability.metrics")

class PrometheusMetricsAdapter(BaseMetricsService):
    def __init__(self, registry: MetricsRegistry):
        self.registry = registry

    def _get_metric(self, name: str):
        return getattr(self.registry, name, None)

    def increment_counter(self, name: str, value: float = 1.0, labels: Optional[Dict[str, str]] = None) -> None:
        metric = self._get_metric(name)
        if metric:
            try:
                if labels:
                    metric.labels(**labels).inc(value)
                else:
                    metric.inc(value)
            except Exception as e:
                logger.warning(f"Failed to increment counter {name}: {str(e)}")

    def set_gauge(self, name: str, value: float, labels: Optional[Dict[str, str]] = None) -> None:
        metric = self._get_metric(name)
        if metric:
            try:
                if labels:
                    metric.labels(**labels).set(value)
                else:
                    metric.set(value)
            except Exception as e:
                logger.warning(f"Failed to set gauge {name}: {str(e)}")

    def increment_gauge(self, name: str, value: float = 1.0, labels: Optional[Dict[str, str]] = None) -> None:
        metric = self._get_metric(name)
        if metric:
            try:
                if labels:
                    metric.labels(**labels).inc(value)
                else:
                    metric.inc(value)
            except Exception as e:
                logger.warning(f"Failed to increment gauge {name}: {str(e)}")

    def decrement_gauge(self, name: str, value: float = 1.0, labels: Optional[Dict[str, str]] = None) -> None:
        metric = self._get_metric(name)
        if metric:
            try:
                if labels:
                    metric.labels(**labels).dec(value)
                else:
                    metric.dec(value)
            except Exception as e:
                logger.warning(f"Failed to decrement gauge {name}: {str(e)}")

    def observe_histogram(self, name: str, value: float, labels: Optional[Dict[str, str]] = None) -> None:
        metric = self._get_metric(name)
        if metric:
            try:
                if labels:
                    metric.labels(**labels).observe(value)
                else:
                    metric.observe(value)
            except Exception as e:
                logger.warning(f"Failed to observe histogram {name}: {str(e)}")

    def get_registered_metrics_count(self) -> int:
        return self.registry.get_registered_count()
