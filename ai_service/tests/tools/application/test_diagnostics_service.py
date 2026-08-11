import pytest
from app.tools.application.diagnostics.diagnostics_application_service import DiagnosticsApplicationService
from app.tools.domain.schemas.health_schema import HealthSchema
from app.tools.domain.schemas.connectivity_schema import ConnectivitySchema

@pytest.mark.asyncio
async def test_health_check():
    service = DiagnosticsApplicationService()
    await service.initialize()
    schema = HealthSchema(component="all")
    result = await service.check_health(schema)
    assert result.status == "healthy"

@pytest.mark.asyncio
async def test_connectivity():
    service = DiagnosticsApplicationService()
    await service.initialize()
    schema = ConnectivitySchema(host="127.0.0.1", port=80)
    result = await service.check_connectivity(schema)
    assert isinstance(result.reachable, bool)
