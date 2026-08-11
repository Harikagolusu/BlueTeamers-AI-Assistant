import threading
from typing import List, Any
from app.observability.interfaces.i_metrics import IMetricsRegistry, IMetricsAggregator
from app.agents.events.event_bus import agent_event_bus
from app.agents.events.agent_events import AgentEvent

class MetricCollectedEvent(AgentEvent):
    type: str = "MetricCollected"
    metric_name: str
    value: float

class InMemoryMetricsRegistry(IMetricsRegistry):
    def __init__(self, aggregator: IMetricsAggregator):
        self._metrics: List[Any] = []
        self._aggregator = aggregator
        self._lock = threading.RLock()

    def register(self, metric: Any) -> None:
        with self._lock:
            self._metrics.append(metric)
            
        agent_event_bus.publish(MetricCollectedEvent(
            session_id="sys",
            metric_name=metric.name,
            value=metric.value
        ))

    def get_metrics(self) -> list:
        with self._lock:
            snapshot = self._metrics[:]
            self._metrics.clear()
            return self._aggregator.aggregate(snapshot)
