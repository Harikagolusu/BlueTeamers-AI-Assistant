from functools import lru_cache

from app.observability.service import ObservabilityService
from app.observability.registry import MetricsRegistry
from app.observability.adapters.prometheus_adapter import PrometheusMetricsAdapter
from app.observability.adapters.tracing_adapter import NativeTracingAdapter

@lru_cache()
def get_observability_service() -> ObservabilityService:
    """
    Dependency provider for the ObservabilityService facade.
    Returns a singleton instance to ensure metrics registries are not duplicated.
    """
    registry = MetricsRegistry()
    metrics = PrometheusMetricsAdapter(registry)
    tracing = NativeTracingAdapter()
    
    return ObservabilityService(metrics=metrics, tracing=tracing)

from app.observability.service_health import ObservabilityHealthService

def get_observability_health_service() -> ObservabilityHealthService:
    return ObservabilityHealthService(get_observability_service())
