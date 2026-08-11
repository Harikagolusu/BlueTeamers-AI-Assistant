import time
from typing import Dict, Any

from app.observability.service import ObservabilityService
from app.core.config import settings

START_TIME = time.time()

class ObservabilityHealthService:
    def __init__(self, observability_service: ObservabilityService):
        self.obs = observability_service

    async def get_health_status(self) -> Dict[str, Any]:
        """
        Return the health and status of the Observability components.
        """
        metrics_healthy = "healthy" if self.obs.metrics_enabled else "disabled"
        tracing_healthy = "healthy" if self.obs.tracing_enabled else "disabled"
        logging_healthy = "healthy" if self.obs.enabled else "disabled"
        
        return {
            "service": settings.SERVICE_NAME,
            "version": settings.SERVICE_VERSION,
            "environment": settings.ENVIRONMENT,
            "uptime_seconds": int(time.time() - START_TIME),
            "metrics": metrics_healthy,
            "tracing": tracing_healthy,
            "logging": logging_healthy,
            "metrics_provider": settings.METRICS_PROVIDER,
            "tracing_provider": settings.TRACING_PROVIDER,
            "registered_metrics": self.obs.get_registered_metrics_count()
        }
