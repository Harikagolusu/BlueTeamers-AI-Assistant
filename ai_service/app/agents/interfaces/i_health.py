from abc import ABC, abstractmethod
from typing import Dict, Any

class IHeartbeatMonitor(ABC):
    @abstractmethod
    def ping(self, component_id: str) -> bool: pass

class ILatencyMonitor(ABC):
    @abstractmethod
    def record_latency(self, component_id: str, latency_ms: float) -> None: pass
    @abstractmethod
    def get_average_latency(self, component_id: str) -> float: pass

class IAvailabilityMonitor(ABC):
    @abstractmethod
    def report_status(self, component_id: str, is_available: bool) -> None: pass
    @abstractmethod
    def get_availability(self, component_id: str) -> float: pass

class IFailureMonitor(ABC):
    @abstractmethod
    def record_failure(self, component_id: str, error: str) -> None: pass
    @abstractmethod
    def get_failure_rate(self, component_id: str) -> float: pass

class IHealthMonitor(ABC):
    @abstractmethod
    def get_component_health(self, component_id: str) -> Dict[str, Any]: pass

class IHealthChecker(ABC):
    @abstractmethod
    def check_all(self) -> Dict[str, Any]: pass
