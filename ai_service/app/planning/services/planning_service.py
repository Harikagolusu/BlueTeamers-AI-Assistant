from typing import Dict, Any, List
from app.planning.interfaces.i_planning_service import IPlanningService
from app.planning.models.context import PlanningContext
from app.planning.models.plan import ExecutionPlanStatus, ExecutionConstraint
from app.planning.planners.single_execution_planner import SingleExecutionPlanner
from app.planning.planners.hybrid_execution_planner import HybridExecutionPlanner
from app.planning.planners.clarification_planner import ClarificationPlanner
from app.planning.planners.multi_agent_planner import MultiAgentPlanner
from app.planning.validators.dag_validator import DAGValidator
from app.planning.policies.cost_policy import CostPolicy
from app.planning.estimation.heuristic_estimator import HeuristicEstimator

class PlanningService(IPlanningService):
    def __init__(self):
        self.single_planner = SingleExecutionPlanner()
        self.hybrid_planner = HybridExecutionPlanner()
        self.clarification_planner = ClarificationPlanner()
        self.multi_agent_planner = MultiAgentPlanner()

    async def create_plan(self, intent_analysis: Any, conversation_context: Dict[str, Any]) -> PlanningContext:
        ctx = PlanningContext(metadata={"source": "PlanningService"})
        
        # 1. Selection
        primary_intent = getattr(intent_analysis, "primary_intent", None)
        intent_type = getattr(primary_intent, "type", None) if primary_intent else None
        
        if getattr(intent_analysis, "clarification_request", None):
            plan = await self.clarification_planner.build_plan(intent_analysis, conversation_context)
        elif intent_type and intent_type.value == "INVESTIGATION":
            plan = await self.multi_agent_planner.build_plan(intent_analysis, conversation_context)
        elif len(getattr(intent_analysis, "secondary_intents", [])) > 0:
            plan = await self.hybrid_planner.build_plan(intent_analysis, conversation_context)
        else:
            plan = await self.single_planner.build_plan(intent_analysis, conversation_context)
            
        # 2. Estimation
        HeuristicEstimator.estimate(plan)
        ctx.estimates = {
            "cost": plan.estimated_cost,
            "tokens": plan.estimated_tokens,
            "time_ms": plan.estimated_time_ms
        }
            
        # 3. Validation
        validation_results = DAGValidator.validate(plan)
        
        # 4. Policy Checks
        constraint = ExecutionConstraint(max_cost=2.0, max_tokens=100000)
        validation_results.extend(CostPolicy.apply(plan, constraint))
        
        ctx.validation_results = validation_results
        
        if any(msg.startswith("ERROR") for msg in validation_results):
            object.__setattr__(plan, "status", ExecutionPlanStatus.FAILED)
        else:
            object.__setattr__(plan, "status", ExecutionPlanStatus.READY)
            
        ctx.plan = plan
        return ctx
