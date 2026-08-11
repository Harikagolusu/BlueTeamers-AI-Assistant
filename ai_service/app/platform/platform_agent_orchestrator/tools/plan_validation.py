from app.tools.base import BaseTool, ToolMetadata
from app.tools.context import ToolContext
from app.platform.platform_agent_orchestrator.services.plan_validator import PlanValidatorService
from typing import Any

class PlanValidationTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="plan_validation",
            metadata=ToolMetadata(
                input_schema={"execution_plan": "ExecutionPlan"},
                output_schema={"is_valid": "bool"},
                tags=["orchestration", "validation"]
            )
        )
        self.validator_service = PlanValidatorService()

    async def execute(self, context: ToolContext, **kwargs) -> Any:
        plan = kwargs.get("execution_plan")
        return self.validator_service.validate(plan)
