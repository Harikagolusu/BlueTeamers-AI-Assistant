import pytest
from app.tools.application.utility.utility_application_service import UtilityApplicationService
from app.tools.domain.schemas.calculator_schema import CalculatorSchema
from app.tools.domain.schemas.hash_schema import HashSchema
from app.tools.domain.schemas.time_schema import TimeSchema

@pytest.mark.asyncio
async def test_calculator():
    service = UtilityApplicationService()
    await service.initialize()
    schema = CalculatorSchema(expression="2 + 2 * 3")
    result = await service.calculate(schema)
    assert result.result == 8.0

@pytest.mark.asyncio
async def test_hash_data():
    service = UtilityApplicationService()
    await service.initialize()
    schema = HashSchema(data="test", algorithm="sha256")
    result = await service.hash_data(schema)
    assert result.hash_value == "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08"

@pytest.mark.asyncio
async def test_get_time():
    service = UtilityApplicationService()
    await service.initialize()
    schema = TimeSchema(timezone="UTC")
    result = await service.get_time(schema)
    assert result.timezone == "UTC"
    assert "T" in result.current_time
