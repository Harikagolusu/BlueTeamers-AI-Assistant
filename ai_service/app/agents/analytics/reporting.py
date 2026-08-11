from typing import Dict, Any
from app.agents.interfaces.i_analytics import IMetricsCollector, IAnalyticsAggregator

class ReportingService:
    def __init__(self, collector: IMetricsCollector, aggregator: IAnalyticsAggregator):
        self._collector = collector
        self._aggregator = aggregator

    def generate_report(self) -> Dict[str, Any]:
        metrics = self._collector.collect_metrics()
        aggregated = self._aggregator.aggregate_usage(metrics)
        return {
            "raw": metrics,
            "summary": aggregated
        }
