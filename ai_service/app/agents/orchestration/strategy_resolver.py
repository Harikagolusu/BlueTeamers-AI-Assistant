from app.chat.context.execution_context import ExecutionContext
from app.planning.models.plan import ExecutionPlan
from app.planning.models.context import PlanningContext
from app.chat.interfaces.i_execution_engine import IExecutionEngine
from app.models.chat.chat_models import ExecutionResult
from app.agents.interfaces.i_agent_coordinator import IAgentCoordinator
from app.agents.interfaces.i_agent_planner import IAgentPlanner

class ExecutionStrategyResolver(IExecutionEngine):
    """
    Sits between PlanningStage and Execution Engines.
    Decides whether to route the ExecutionPlan to the standard single AgentExecutor,
    or the multi-agent AgentCoordinator.
    """
    def __init__(
        self, 
        single_agent_executor: IExecutionEngine, 
        coordinator: IAgentCoordinator,
        planner: IAgentPlanner
    ):
        self._single_executor = single_agent_executor
        self._coordinator = coordinator
        self._planner = planner

    @property
    def name(self) -> str:
        return "STRATEGY_RESOLVER"

    async def execute(self, context: ExecutionContext) -> ExecutionResult:
        planning_context: PlanningContext = context.metadata.get("planning")
        if not planning_context or not planning_context.plan:
            return ExecutionResult.failed("STRATEGY_RESOLVER", [{"error": "No ExecutionPlan found"}])
            
        plan: ExecutionPlan = planning_context.plan
        
        # Heuristic: if there are multiple capabilities required, or an explicit flag, 
        # use multi-agent coordination. Otherwise, single agent.
        is_multi_agent = len(set(plan.capabilities_required)) > 1 or plan.metadata.get("force_multi_agent", False)
        
        if is_multi_agent:
            multi_plan = self._planner.create_multi_agent_plan(plan)
            return await self._coordinator.coordinate(multi_plan, context)
        else:
            return await self._single_executor.execute(context)
