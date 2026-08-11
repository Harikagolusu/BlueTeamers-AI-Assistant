import threading
from typing import Dict, Any
from app.agents.interfaces.i_analytics import IUsageTracker

class UsageTracker(IUsageTracker):
    def __init__(self):
        self._usage: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.RLock()

    def track_execution(self, component_id: str, tokens: int, duration_ms: float, success: bool) -> None:
        with self._lock:
            if component_id not in self._usage:
                self._usage[component_id] = {
                    "executions": 0,
                    "tokens": 0,
                    "duration_ms": 0.0,
                    "successes": 0,
                    "failures": 0
                }
                
            stats = self._usage[component_id]
            stats["executions"] += 1
            stats["tokens"] += tokens
            stats["duration_ms"] += duration_ms
            if success:
                stats["successes"] += 1
            else:
                stats["failures"] += 1

    def get_raw_usage(self) -> Dict[str, Dict[str, Any]]:
        with self._lock:
            return dict(self._usage)
