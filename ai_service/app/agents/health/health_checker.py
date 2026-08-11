from typing import Dict, Any
from app.agents.interfaces.i_health import IHealthChecker, IHealthMonitor, IHeartbeatMonitor, ILatencyMonitor, IAvailabilityMonitor, IFailureMonitor

class HealthChecker(IHealthChecker, IHealthMonitor):
    def __init__(
        self,
        heartbeat: IHeartbeatMonitor,
        latency: ILatencyMonitor,
        availability: IAvailabilityMonitor,
        failures: IFailureMonitor
    ):
        self._heartbeat = heartbeat
        self._latency = latency
        self._availability = availability
        self._failures = failures
        self._registered_components = set()

    def register_component(self, component_id: str):
        self._registered_components.add(component_id)

    def get_component_health(self, component_id: str) -> Dict[str, Any]:
        return {
            "component_id": component_id,
            "alive": self._heartbeat.ping(component_id),
            "latency_ms": self._latency.get_average_latency(component_id),
            "availability": self._availability.get_availability(component_id),
            "failure_count": self._failures.get_failure_rate(component_id)
        }

    def check_all(self) -> Dict[str, Any]:
        report = {}
        for comp in self._registered_components:
            report[comp] = self.get_component_health(comp)
        return report
