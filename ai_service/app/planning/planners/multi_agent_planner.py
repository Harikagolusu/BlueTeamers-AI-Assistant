from typing import Dict, Any
from app.planning.interfaces.i_planner import IExecutionPlanner
from app.planning.models.plan import ExecutionPlan, ExecutionStep, Capability, ExecutionStrategy, ExecutionPlanStatus

class MultiAgentPlanner(IExecutionPlanner):
    """Generates a graph-based multi-step plan for complex multi-agent collaboration."""
    @property
    def name(self) -> str:
        return "MultiAgentPlanner"
        
    async def build_plan(self, intent_analysis: Any, conversation_context: Dict[str, Any]) -> ExecutionPlan:
        # Step 1: Knowledge Assistant (RAG context)
        step1 = ExecutionStep(
            name="Knowledge Assistant",
            description="Retrieve internal knowledge and context.",
            required_capability=Capability.KNOWLEDGE_ASSISTANT
        )
        
        # Step 2: Investigation Agent (Tool execution)
        step2 = ExecutionStep(
            name="Investigation Agent",
            description="Run required tools based on retrieved knowledge.",
            required_capability=Capability.INVESTIGATION_AGENT,
            dependencies=[step1.step_id]
        )
        
        # Step 3: Learning Coach (Coaching & analysis)
        step3 = ExecutionStep(
            name="Learning Coach",
            description="Analyze the findings and provide educational context.",
            required_capability=Capability.LEARNING_COACH,
            dependencies=[step2.step_id]
        )
        
        # Step 4: Aggregator (Final response)
        step4 = ExecutionStep(
            name="Aggregator",
            description="Compile outputs from all agents into a final cohesive response.",
            required_capability=Capability.AGGREGATOR,
            dependencies=[step1.step_id, step2.step_id, step3.step_id]
        )
        
        return ExecutionPlan(
            goal="Multi-Agent Investigation Fulfillment",
            execution_strategy=ExecutionStrategy.SEQUENTIAL,
            steps=[step1, step2, step3, step4],
            capabilities_required=[
                Capability.KNOWLEDGE_ASSISTANT, 
                Capability.INVESTIGATION_AGENT, 
                Capability.LEARNING_COACH, 
                Capability.AGGREGATOR
            ],
            status=ExecutionPlanStatus.DRAFT
        )
