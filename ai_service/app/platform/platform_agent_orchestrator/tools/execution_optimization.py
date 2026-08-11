from app.tools.base import BaseTool, ToolMetadata
from app.tools.context import ToolContext
from app.platform.platform_agent_orchestrator.services.execution_optimizer import ExecutionOptimizerService
from typing import Any

class ExecutionOptimizationTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="execution_optimization",
            metadata=ToolMetadata(
                input_schema={"execution_plan": "ExecutionPlan"},
                output_schema={"optimized_plan": "ExecutionPlan"},
                tags=["orchestration", "optimization"]
            )
        )
        self.optimizer_service = ExecutionOptimizerService()

    async def execute(self, context: ToolContext, **kwargs) -> Any:
        plan = kwargs.get("execution_plan")
        return self.optimizer_service.optimize(plan)
