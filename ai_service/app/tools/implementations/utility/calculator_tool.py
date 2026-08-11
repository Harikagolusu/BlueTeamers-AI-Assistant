from app.tools.discovery.decorators.tool_decorator import tool
from app.tools.discovery.metadata.enums import ToolCategory
from app.tools.domain.base_tool import BaseTool
from app.tools.models.tool_request import ToolRequest
from app.tools.models.tool_response import ToolResponse
from app.tools.infrastructure.response.response_builder import ResponseBuilder
from app.tools.infrastructure.validation.validation_service import ValidationService
from app.tools.domain.schemas.calculator_schema import CalculatorSchema
from app.tools.application.interfaces.i_utility_service import IUtilityService

@tool(
    name="calculator",
    description="Evaluates a mathematical expression",
    category=ToolCategory.UTILITY
)
class CalculatorTool(BaseTool):
    def __init__(self, utility_service: IUtilityService):
        super().__init__()
        self._service = utility_service
        
    async def execute(self, request: ToolRequest) -> ToolResponse:
        try:
            schema = ValidationService.validate_schema(CalculatorSchema, request.arguments)
            result = await self._service.calculate(schema)
            return ResponseBuilder.success(result)
        except ValueError as e:
            return ResponseBuilder.validation_error(str(e))
        except Exception as e:
            return ResponseBuilder.system_error(str(e))
