from app.tools.base import BaseTool, ToolMetadata
from app.tools.context import ToolContext
from app.platform.platform_agent_orchestrator.services.capability_resolver import CapabilityResolverService
from typing import Any

class CapabilityResolutionTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="capability_resolution",
            metadata=ToolMetadata(
                input_schema={"capabilities": "list"},
                output_schema={"resolved_capabilities": "dict"},
                tags=["orchestration", "capability"]
            )
        )
        self.resolver_service = CapabilityResolverService()

    async def execute(self, context: ToolContext, **kwargs) -> Any:
        capabilities = kwargs.get("capabilities", [])
        return self.resolver_service.resolve_capabilities(capabilities)
