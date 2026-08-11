from abc import ABC, abstractmethod
from typing import Dict, Any

class IMetricsCollector(ABC):
    @abstractmethod
    def increment_counter(self, name: str, value: int = 1, tags: Dict[str, str] = None) -> None: pass
    @abstractmethod
    def set_gauge(self, name: str, value: float, tags: Dict[str, str] = None) -> None: pass
    @abstractmethod
    def record_histogram(self, name: str, value: float, tags: Dict[str, str] = None) -> None: pass

class IMetricsAggregator(ABC):
    @abstractmethod
    def aggregate(self, metrics_batch: list) -> list: pass

class IMetricsRegistry(ABC):
    @abstractmethod
    def register(self, metric: Any) -> None: pass
    @abstractmethod
    def get_metrics(self) -> list: pass
