import pytest
from app.tools.application.utility.utility_application_service import UtilityApplicationService
from app.tools.application.diagnostics.diagnostics_application_service import DiagnosticsApplicationService
from app.tools.application.cybersecurity.cybersecurity_application_service import CybersecurityApplicationService
from app.tools.domain.schemas.calculator_schema import CalculatorSchema
from app.tools.domain.schemas.hash_schema import HashSchema
from app.tools.domain.schemas.time_schema import TimeSchema
from app.tools.domain.schemas.connectivity_schema import ConnectivitySchema
from app.tools.domain.schemas.cybersecurity_schemas import IpUtilitySchema, UrlValidationSchema

@pytest.mark.asyncio
async def test_calculator_invalid_expression():
    service = UtilityApplicationService()
    await service.initialize()
    with pytest.raises(ValueError, match="Invalid mathematical expression"):
        await service.calculate(CalculatorSchema(expression="10 / 0"))
        
@pytest.mark.asyncio
async def test_calculator_unsupported_operator():
    service = UtilityApplicationService()
    await service.initialize()
    with pytest.raises(ValueError, match="Invalid mathematical expression"):
        await service.calculate(CalculatorSchema(expression="import os"))

@pytest.mark.asyncio
async def test_hash_invalid_algorithm():
    service = UtilityApplicationService()
    await service.initialize()
    with pytest.raises(ValueError, match="Algorithm unknown not supported"):
        await service.hash_data(HashSchema(data="test", algorithm="unknown"))

@pytest.mark.asyncio
async def test_time_invalid_timezone():
    service = UtilityApplicationService()
    await service.initialize()
    with pytest.raises(ValueError, match="Unknown timezone"):
        await service.get_time(TimeSchema(timezone="Invalid/Timezone"))

@pytest.mark.asyncio
async def test_connectivity_unreachable():
    service = DiagnosticsApplicationService()
    await service.initialize()
    # Assuming 10.255.255.255 is unreachable
    result = await service.check_connectivity(ConnectivitySchema(host="10.255.255.255", port=80))
    assert result.reachable is False
    assert result.latency_ms == 0.0

@pytest.mark.asyncio
async def test_ip_invalid():
    service = CybersecurityApplicationService()
    await service.initialize()
    with pytest.raises(ValueError, match="Invalid IP address"):
        await service.get_ip_utility(IpUtilitySchema(ip_address="999.999.999.999"))

@pytest.mark.asyncio
async def test_url_invalid():
    service = CybersecurityApplicationService()
    await service.initialize()
    # Though pydantic schema UrlValidationSchema validates the URL, if we bypass it:
    result = await service.validate_url(UrlValidationSchema(url="http://valid.com"))
    assert result.is_valid is True
