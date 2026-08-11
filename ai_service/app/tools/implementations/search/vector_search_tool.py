from app.tools.discovery.decorators.tool_decorator import tool
from app.tools.discovery.metadata.enums import ToolCategory
from app.tools.domain.base_tool import BaseTool
from app.tools.models.tool_request import ToolRequest
from app.tools.models.tool_response import ToolResponse
from app.tools.infrastructure.response.response_builder import ResponseBuilder
from app.tools.infrastructure.validation.validation_service import ValidationService
from app.tools.domain.schemas.search_schemas import VectorSearchSchema

@tool(
    name="vector_search",
    description="Vector search documents",
    category=ToolCategory.SEARCH
)
class VectorSearchTool(BaseTool):
    def __init__(self, service):
        super().__init__()
        self._service = service
        
    async def execute(self, request: ToolRequest) -> ToolResponse:
        try:
            schema = ValidationService.validate_schema(VectorSearchSchema, request.arguments)
            result = await self._service.vector_search(schema)
            return ResponseBuilder.success(result)
        except ValueError as e:
            return ResponseBuilder.validation_error(str(e))
        except Exception as e:
            return ResponseBuilder.system_error(str(e))
