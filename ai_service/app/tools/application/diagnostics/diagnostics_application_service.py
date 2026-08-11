import time
import socket
from app.tools.application.interfaces.i_diagnostics_service import IDiagnosticsService
from app.tools.infrastructure.base.base_service import BaseService
from app.tools.domain.schemas.health_schema import HealthSchema
from app.tools.domain.results.health_result import HealthResult
from app.tools.domain.schemas.connectivity_schema import ConnectivitySchema
from app.tools.domain.results.connectivity_result import ConnectivityResult

class DiagnosticsApplicationService(BaseService, IDiagnosticsService):
    async def _on_initialize(self) -> None:
        self._logger.info("Initializing DiagnosticsApplicationService")

    async def check_health(self, schema: HealthSchema) -> HealthResult:
        components = {"database": "healthy", "cache": "healthy"}
        if schema.component != "all" and schema.component in components:
            return HealthResult(status=components[schema.component], components={schema.component: components[schema.component]})
        return HealthResult(status="healthy", components=components)

    async def check_connectivity(self, schema: ConnectivitySchema) -> ConnectivityResult:
        start = time.perf_counter()
        reachable = False
        try:
            with socket.create_connection((schema.host, schema.port), timeout=2):
                reachable = True
        except Exception:
            pass
        latency = (time.perf_counter() - start) * 1000
        return ConnectivityResult(reachable=reachable, latency_ms=latency if reachable else 0.0)
