from typing import Dict
from app.observability.interfaces.i_metrics import IMetricsCollector, IMetricsRegistry
from app.observability.models.metrics import MetricRecord

class InMemoryMetricsCollector(IMetricsCollector):
    def __init__(self, registry: IMetricsRegistry):
        self._registry = registry

    def increment_counter(self, name: str, value: int = 1, tags: Dict[str, str] = None) -> None:
        record = MetricRecord(name=name, type="counter", value=value, tags=tags or {})
        self._registry.register(record)

    def set_gauge(self, name: str, value: float, tags: Dict[str, str] = None) -> None:
        record = MetricRecord(name=name, type="gauge", value=value, tags=tags or {})
        self._registry.register(record)

    def record_histogram(self, name: str, value: float, tags: Dict[str, str] = None) -> None:
        record = MetricRecord(name=name, type="histogram", value=value, tags=tags or {})
        self._registry.register(record)
