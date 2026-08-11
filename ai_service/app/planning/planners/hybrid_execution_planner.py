from typing import Dict, Any
from app.planning.interfaces.i_planner import IExecutionPlanner
from app.planning.models.plan import ExecutionPlan, ExecutionStep, Capability, ExecutionStrategy, ExecutionPlanStatus

class HybridExecutionPlanner(IExecutionPlanner):
    """Generates a graph-based multi-step plan."""
    @property
    def name(self) -> str:
        return "HybridExecutionPlanner"
        
    async def build_plan(self, intent_analysis: Any, conversation_context: Dict[str, Any]) -> ExecutionPlan:
        step1 = ExecutionStep(
            name="Retrieve Context",
            description="Pull context via RAG",
            required_capability=Capability.RAG
        )
        
        step2 = ExecutionStep(
            name="Execute Tool",
            description="Use tool with context",
            required_capability=Capability.TOOL,
            dependencies=[step1.step_id] # step2 depends on step1
        )
        
        step3 = ExecutionStep(
            name="Generate Final Response",
            description="Summarize results",
            required_capability=Capability.LLM,
            dependencies=[step2.step_id] # step3 depends on step2
        )
        
        return ExecutionPlan(
            goal="Hybrid multi-step fulfillment",
            execution_strategy=ExecutionStrategy.SEQUENTIAL, # Even with a graph, execution may be sequential initially
            steps=[step1, step2, step3],
            capabilities_required=[Capability.RAG, Capability.TOOL, Capability.LLM],
            status=ExecutionPlanStatus.DRAFT
        )
