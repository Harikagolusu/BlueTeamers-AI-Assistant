from typing import Dict, Any, Optional
from app.observability.interfaces.i_logging import ILogger
from app.observability.interfaces.i_tracing import ITracer, ISpan
from app.observability.interfaces.i_metrics import IMetricsCollector
from app.observability.interfaces.i_profiling import IProfiler
from app.observability.interfaces.i_health import IHealthMonitor

class InstrumentationFacade:
    def __init__(
        self,
        logger: ILogger,
        tracer: ITracer,
        metrics: IMetricsCollector,
        profiler: IProfiler,
        health: IHealthMonitor
    ):
        self.logger = logger
        self.tracer = tracer
        self.metrics = metrics
        self.profiler = profiler
        self.health = health

    def start_span(self, name: str, parent_id: Optional[str] = None) -> ISpan:
        return self.tracer.start_span(name, parent_id)

    def log_info(self, message: str, **kwargs) -> None:
        self.logger.info(message, **kwargs)
        
    def log_error(self, message: str, **kwargs) -> None:
        self.logger.error(message, **kwargs)

    def record_latency(self, name: str, latency: float, tags: Dict[str, str] = None) -> None:
        self.metrics.record_histogram(name, latency, tags)
        
    def increment_counter(self, name: str, value: int = 1, tags: Dict[str, str] = None) -> None:
        self.metrics.increment_counter(name, value, tags)
