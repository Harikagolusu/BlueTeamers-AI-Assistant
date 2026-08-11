from app.tools.base import BaseTool, ToolMetadata
from app.tools.context import ToolContext
from app.platform.platform_agent_orchestrator.services.execution_planner import ExecutionPlannerService
from typing import Any

class ExecutionPlanningTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="execution_planning",
            metadata=ToolMetadata(
                input_schema={"intent": "UserIntent", "resolved_capabilities": "dict", "payload": "dict"},
                output_schema={"execution_plan": "ExecutionPlan"},
                tags=["orchestration", "planning"]
            )
        )
        self.planner_service = ExecutionPlannerService()

    async def execute(self, context: ToolContext, **kwargs) -> Any:
        intent = kwargs.get("intent")
        resolved_capabilities = kwargs.get("resolved_capabilities")
        payload = kwargs.get("payload")
        
        return self.planner_service.generate_plan(intent, resolved_capabilities, payload)
