from typing import Dict, Any
from app.planning.interfaces.i_planner import IExecutionPlanner
from app.planning.models.plan import ExecutionPlan, ExecutionStep, Capability, ExecutionStrategy, ExecutionPlanStatus

class ClarificationPlanner(IExecutionPlanner):
    @property
    def name(self) -> str:
        return "ClarificationPlanner"
        
    async def build_plan(self, intent_analysis: Any, conversation_context: Dict[str, Any]) -> ExecutionPlan:
        step = ExecutionStep(
            name="Ask Clarification",
            description="Prompt the user for missing info.",
            required_capability=Capability.CLARIFICATION
        )
        
        return ExecutionPlan(
            goal="Resolve Ambiguity",
            execution_strategy=ExecutionStrategy.CLARIFICATION,
            steps=[step],
            capabilities_required=[Capability.CLARIFICATION],
            status=ExecutionPlanStatus.DRAFT
        )
