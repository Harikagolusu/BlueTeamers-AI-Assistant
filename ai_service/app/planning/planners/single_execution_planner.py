from typing import Dict, Any
from app.planning.interfaces.i_planner import IExecutionPlanner
from app.planning.models.plan import ExecutionPlan, ExecutionStep, Capability, ExecutionStrategy, ExecutionPlanStatus

class SingleExecutionPlanner(IExecutionPlanner):
    @property
    def name(self) -> str:
        return "SingleExecutionPlanner"
        
    async def build_plan(self, intent_analysis: Any, conversation_context: Dict[str, Any]) -> ExecutionPlan:
        # Intent Intelligence outputs typically map directly to a single engine capability
        intent_type = intent_analysis.primary_intent.type.name if intent_analysis.primary_intent else "GENERAL_CHAT"
        
        # Map intent to Capability
        cap = Capability.LLM
        if intent_type == "TOOL_EXECUTION":
            cap = Capability.TOOL
        elif intent_type == "KNOWLEDGE_RETRIEVAL":
            cap = Capability.RAG
            
        step = ExecutionStep(
            name=f"Execute {cap.value}",
            description="A single step execution.",
            required_capability=cap
        )
        
        return ExecutionPlan(
            goal=f"Fulfill intent {intent_type}",
            execution_strategy=ExecutionStrategy.SEQUENTIAL,
            steps=[step],
            capabilities_required=[cap],
            status=ExecutionPlanStatus.DRAFT
        )
