import time
import socket
from app.tools.application.interfaces.i_diagnostics_service import IDiagnosticsService
from app.tools.infrastructure.base.base_service import BaseService
from app.tools.domain.schemas.health_schema import HealthSchema
from app.tools.domain.results.health_result import HealthResult
from app.tools.domain.schemas.connectivity_schema import ConnectivitySchema
from app.tools.domain.results.connectivity_result import ConnectivityResult

# Only loopback / local-network diagnostics hosts are ever reachable. Arbitrary
# user-supplied host:port connectivity checks would create an SSRF / network-
# scan primitive, so everything else is rejected.
_ALLOWED_HOSTS = {"127.0.0.1", "localhost", "::1"}
_ALLOWED_PORTS = {8000, 8001, 5173}

class DiagnosticsApplicationService(BaseService, IDiagnosticsService):
    async def _on_initialize(self) -> None:
        self._logger.info("Initializing DiagnosticsApplicationService")

    async def check_health(self, schema: HealthSchema) -> HealthResult:
        components = {"database": "healthy", "cache": "healthy"}
        if schema.component != "all" and schema.component in components:
            return HealthResult(status=components[schema.component], components={schema.component: components[schema.component]})
        return HealthResult(status="healthy", components=components)

    async def check_connectivity(self, schema: ConnectivitySchema) -> ConnectivityResult:
        if schema.host not in _ALLOWED_HOSTS or schema.port not in _ALLOWED_PORTS:
            return ConnectivityResult(reachable=False, latency_ms=0.0)
        start = time.perf_counter()
        reachable = False
        try:
            with socket.create_connection((schema.host, schema.port), timeout=2):
                reachable = True
        except Exception:
            pass
        latency = (time.perf_counter() - start) * 1000
        return ConnectivityResult(reachable=reachable, latency_ms=latency if reachable else 0.0)
