from typing import Any
from app.tools.models.tool_response import ToolResponse

def create_mock_response(success: bool, result: Any = None, error: str = None) -> ToolResponse:
    return ToolResponse(
        success=success,
        result=result,
        error=error,
        metadata={}
    )
