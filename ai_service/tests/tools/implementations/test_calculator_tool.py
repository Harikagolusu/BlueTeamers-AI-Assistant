import pytest
from app.tools.implementations.utility.calculator_tool import CalculatorTool
from app.tools.application.utility.utility_application_service import UtilityApplicationService
from app.tools.models.tool_request import ToolRequest
from app.tools.models.execution_context import ExecutionContext

@pytest.mark.asyncio
async def test_calculator_tool_execute():
    service = UtilityApplicationService()
    await service.initialize()
    tool = CalculatorTool(utility_service=service)
    
    req = ToolRequest(
        tool_name="calculator",
        arguments={"expression": "10 / 2"},
        context=ExecutionContext()
    )
    resp = await tool.execute(req)
    assert resp.success is True
    assert resp.result["result"] == 5.0
