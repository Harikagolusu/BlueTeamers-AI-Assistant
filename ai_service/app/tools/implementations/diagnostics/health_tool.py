from app.tools.discovery.decorators.tool_decorator import tool
from app.tools.discovery.metadata.enums import ToolCategory
from app.tools.domain.base_tool import BaseTool
from app.tools.models.tool_request import ToolRequest
from app.tools.models.tool_response import ToolResponse
from app.tools.infrastructure.response.response_builder import ResponseBuilder
from app.tools.infrastructure.validation.validation_service import ValidationService
from app.tools.domain.schemas.health_schema import HealthSchema
from app.tools.application.interfaces.i_diagnostics_service import IDiagnosticsService

@tool(
    name="system_health",
    description="Checks the health of the system and its components",
    category=ToolCategory.SYSTEM
)
class HealthTool(BaseTool):
    def __init__(self, diagnostics_service: IDiagnosticsService):
        super().__init__()
        self._service = diagnostics_service
        
    async def execute(self, request: ToolRequest) -> ToolResponse:
        try:
            schema = ValidationService.validate_schema(HealthSchema, request.arguments)
            result = await self._service.check_health(schema)
            return ResponseBuilder.success(result)
        except ValueError as e:
            return ResponseBuilder.validation_error(str(e))
        except Exception as e:
            return ResponseBuilder.system_error(str(e))
