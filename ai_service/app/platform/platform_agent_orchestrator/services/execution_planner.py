import uuid
from typing import List, Dict, Any
from app.platform.platform_agent_orchestrator.models import UserIntent, ExecutionPlan, ExecutionStep, ExecutionStrategy

class ExecutionPlannerService:
    def generate_plan(self, intent: UserIntent, resolved_capabilities: Dict[str, str], payload: Dict[str, Any]) -> ExecutionPlan:
        """
        Builds the execution step list and dependency graph based on the intent and capabilities.
        """
        plan = ExecutionPlan(
            plan_id=f"plan-{uuid.uuid4().hex[:8]}",
            goal=f"Execute {intent.intent_type.value}",
        )
        
        # Simple sequential execution builder for MVP
        previous_step_id = None
        for order, cap in enumerate(intent.requested_capabilities):
            agent_id = resolved_capabilities.get(cap)
            
            step = ExecutionStep(
                step_id=f"step-{uuid.uuid4().hex[:8]}",
                capability=cap,
                target_agent=agent_id,
                inputs=payload,
                execution_order=order,
                dependencies=[previous_step_id] if previous_step_id else []
            )
            plan.execution_steps.append(step)
            plan.dependencies[step.step_id] = step.dependencies
            previous_step_id = step.step_id
            
        plan.strategy = ExecutionStrategy.SEQUENTIAL if len(plan.execution_steps) > 1 else ExecutionStrategy.DYNAMIC
        # Parallel groups computation omitted for MVP sequential flow
        plan.parallel_groups = [[s.step_id] for s in plan.execution_steps]
        
        return plan
