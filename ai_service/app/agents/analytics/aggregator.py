from typing import Dict, Any
from app.agents.interfaces.i_analytics import IAnalyticsAggregator

class AnalyticsAggregator(IAnalyticsAggregator):
    def aggregate_usage(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        aggregated = {
            "total_executions": 0,
            "total_tokens": 0,
            "total_failures": 0,
            "components_used": 0
        }
        
        usage = metrics.get("usage", {})
        for comp_id, stats in usage.items():
            aggregated["components_used"] += 1
            aggregated["total_executions"] += stats.get("executions", 0)
            aggregated["total_tokens"] += stats.get("tokens", 0)
            aggregated["total_failures"] += stats.get("failures", 0)
            
        return aggregated
