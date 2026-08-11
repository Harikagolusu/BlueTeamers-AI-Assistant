from typing import Dict, Any
from app.observability.interfaces.i_observability import IObservabilityService

class RuntimeTelemetryService:
    """
    Facade wrapping the existing app.observability module.
    Ensures that observability doesn't get duplicated while providing a unified
    runtime interface for telemetry, tracing, and metrics.
    """
    def __init__(self, observability: IObservabilityService):
        self.observability = observability
        
    async def start_trace(self, name: str, attributes: Dict[str, Any] = None) -> Any:
        return self.observability.start_trace(name, attributes)
        
    async def end_trace(self, trace_id: Any) -> None:
        self.observability.end_trace(trace_id)
        
    async def record_metric(self, name: str, value: float, tags: Dict[str, str] = None) -> None:
        self.observability.record_metric(name, value, tags)
