from abc import ABC, abstractmethod
from typing import Dict, Any

class IUsageTracker(ABC):
    @abstractmethod
    def track_execution(self, component_id: str, tokens: int, duration_ms: float, success: bool) -> None: pass

class IMetricsCollector(ABC):
    @abstractmethod
    def collect_metrics(self) -> Dict[str, Any]: pass

class IAnalyticsAggregator(ABC):
    @abstractmethod
    def aggregate_usage(self, metrics: Dict[str, Any]) -> Dict[str, Any]: pass
