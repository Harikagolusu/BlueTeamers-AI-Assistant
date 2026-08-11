from abc import ABC, abstractmethod
from app.tools.domain.schemas.health_schema import HealthSchema
from app.tools.domain.results.health_result import HealthResult
from app.tools.domain.schemas.connectivity_schema import ConnectivitySchema
from app.tools.domain.results.connectivity_result import ConnectivityResult

class IDiagnosticsService(ABC):
    @abstractmethod
    async def check_health(self, schema: HealthSchema) -> HealthResult:
        pass

    @abstractmethod
    async def check_connectivity(self, schema: ConnectivitySchema) -> ConnectivityResult:
        pass
