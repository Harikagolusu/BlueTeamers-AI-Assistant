from typing import Dict, Any
from app.agents.interfaces.i_analytics import IMetricsCollector
from app.agents.analytics.usage_tracker import UsageTracker

class MetricsCollector(IMetricsCollector):
    def __init__(self, usage_tracker: UsageTracker):
        self._usage_tracker = usage_tracker
        
    def collect_metrics(self) -> Dict[str, Any]:
        return {
            "usage": self._usage_tracker.get_raw_usage(),
            # In future, collect memory footprint, token rates, etc.
        }
