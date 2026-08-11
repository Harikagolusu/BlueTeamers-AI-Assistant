import threading
from typing import Dict, Any, List
from app.agents.interfaces.i_health import IHeartbeatMonitor, ILatencyMonitor, IAvailabilityMonitor, IFailureMonitor

class BaseMonitor:
    def __init__(self):
        self._lock = threading.RLock()
        self._data: Dict[str, Any] = {}

class HeartbeatMonitor(BaseMonitor, IHeartbeatMonitor):
    def ping(self, component_id: str) -> bool:
        with self._lock:
            self._data[component_id] = True
            return True

class LatencyMonitor(BaseMonitor, ILatencyMonitor):
    def __init__(self):
        super().__init__()
        self._latencies: Dict[str, List[float]] = {}
        
    def record_latency(self, component_id: str, latency_ms: float) -> None:
        with self._lock:
            if component_id not in self._latencies:
                self._latencies[component_id] = []
            self._latencies[component_id].append(latency_ms)

    def get_average_latency(self, component_id: str) -> float:
        with self._lock:
            lst = self._latencies.get(component_id, [])
            return sum(lst) / len(lst) if lst else 0.0

class AvailabilityMonitor(BaseMonitor, IAvailabilityMonitor):
    def report_status(self, component_id: str, is_available: bool) -> None:
        with self._lock:
            self._data[component_id] = is_available

    def get_availability(self, component_id: str) -> float:
        with self._lock:
            # Simplified boolean to float
            return 1.0 if self._data.get(component_id, False) else 0.0

class FailureMonitor(BaseMonitor, IFailureMonitor):
    def __init__(self):
        super().__init__()
        self._failures: Dict[str, int] = {}
        
    def record_failure(self, component_id: str, error: str) -> None:
        with self._lock:
            self._failures[component_id] = self._failures.get(component_id, 0) + 1

    def get_failure_rate(self, component_id: str) -> float:
        with self._lock:
            return float(self._failures.get(component_id, 0))
