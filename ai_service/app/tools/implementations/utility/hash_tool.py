from app.tools.discovery.decorators.tool_decorator import tool
from app.tools.discovery.metadata.enums import ToolCategory
from app.tools.domain.base_tool import BaseTool
from app.tools.models.tool_request import ToolRequest
from app.tools.models.tool_response import ToolResponse
from app.tools.infrastructure.response.response_builder import ResponseBuilder
from app.tools.infrastructure.validation.validation_service import ValidationService
from app.tools.domain.schemas.hash_schema import HashSchema
from app.tools.application.interfaces.i_utility_service import IUtilityService

@tool(
    name="hash",
    description="Hashes data using specified algorithm",
    category=ToolCategory.UTILITY
)
class HashTool(BaseTool):
    def __init__(self, utility_service: IUtilityService):
        super().__init__()
        self._service = utility_service
        
    async def execute(self, request: ToolRequest) -> ToolResponse:
        try:
            schema = ValidationService.validate_schema(HashSchema, request.arguments)
            result = await self._service.hash_data(schema)
            return ResponseBuilder.success(result)
        except ValueError as e:
            return ResponseBuilder.validation_error(str(e))
        except Exception as e:
            return ResponseBuilder.system_error(str(e))
