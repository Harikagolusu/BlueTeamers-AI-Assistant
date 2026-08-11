import time
import asyncio
from typing import Dict, Any

class PlatformHealthMonitor:
    def __init__(self):
        self.metrics = {
            "platform_uptime": 0.0,
            "workflow_latency_avg": 0.0,
            "agent_latency_avg": 0.0,
            "queue_depth": 0,
            "active_executions": 0,
            "failure_rate": 0.0,
            "retry_count": 0
        }
        
    def record_latency(self, component: str, latency_ms: float):
        key = f"{component}_latency_avg"
        if key in self.metrics:
            # Exponential moving average for simplicity
            self.metrics[key] = (self.metrics[key] * 0.9) + (latency_ms * 0.1)
            
    def get_health_report(self) -> Dict[str, Any]:
        return self.metrics
