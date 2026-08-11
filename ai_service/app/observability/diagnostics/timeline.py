from typing import Dict, Any, List
from app.observability.interfaces.i_diagnostics import IExecutionTimeline

class ExecutionTimeline(IExecutionTimeline):
    def __init__(self):
        self._events: List[Dict[str, Any]] = []

    def add_event(self, timestamp: str, event_type: str, details: Dict[str, Any]) -> None:
        self._events.append({
            "timestamp": timestamp,
            "type": event_type,
            "details": details
        })

    def generate(self) -> list:
        # Sort by timestamp
        return sorted(self._events, key=lambda x: x["timestamp"])
