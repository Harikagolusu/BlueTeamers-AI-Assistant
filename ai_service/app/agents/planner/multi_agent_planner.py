from app.agents.interfaces.i_agent_planner import IAgentPlanner
from app.planning.models.plan import ExecutionPlan
from app.agents.models.orchestration_models import MultiAgentExecutionPlan

class MultiAgentPlanner(IAgentPlanner):
    """
    Wraps an ExecutionPlan in a MultiAgentExecutionPlan without mutating the original.
    In the future, this class can analyze the DAG and split tasks intelligently.
    """
    def create_multi_agent_plan(self, plan: ExecutionPlan) -> MultiAgentExecutionPlan:
        # For now, simply encapsulate the plan. 
        # The coordinator will iterate through the original plan's steps.
        return MultiAgentExecutionPlan(
            original_execution_plan=plan
        )
