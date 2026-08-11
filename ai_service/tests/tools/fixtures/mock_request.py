from typing import Any
from app.tools.models.tool_request import ToolRequest
from app.tools.models.execution_context import ExecutionContext

def create_mock_request(tool_name: str, arguments: dict = None) -> ToolRequest:
    return ToolRequest(
        tool_name=tool_name,
        arguments=arguments or {},
        context=ExecutionContext()
    )
