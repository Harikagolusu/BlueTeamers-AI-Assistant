from app.tools.base import BaseTool, ToolMetadata
from app.tools.context import ToolContext
from app.platform.platform_agent_orchestrator.models import OrchestratorContext
from typing import Any

class ContextManagementTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="context_management",
            metadata=ToolMetadata(
                input_schema={"action": "str", "payload": "dict", "orchestrator_context": "OrchestratorContext"},
                output_schema={"updated_context": "OrchestratorContext"},
                tags=["orchestration", "context"]
            )
        )

    async def execute(self, context: ToolContext, **kwargs) -> Any:
        action = kwargs.get("action")
        payload = kwargs.get("payload", {})
        orch_context: OrchestratorContext = kwargs.get("orchestrator_context")
        
        if action == "UPDATE_SHARED_MEMORY":
            orch_context.execution.shared_memory.memory.update(payload)
            
        return orch_context
