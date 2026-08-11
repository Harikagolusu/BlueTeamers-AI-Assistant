from app.planning.models.plan import ExecutionPlan, ExecutionConstraint
from typing import List

class CostPolicy:
    """Ensures the plan does not exceed maximum constraints."""
    
    @staticmethod
    def apply(plan: ExecutionPlan, constraints: ExecutionConstraint) -> List[str]:
        errors = []
        if constraints.max_cost > 0 and plan.estimated_cost > constraints.max_cost:
            errors.append(f"ERROR: Estimated cost {plan.estimated_cost} exceeds max {constraints.max_cost}")
        
        if constraints.max_tokens > 0 and plan.estimated_tokens > constraints.max_tokens:
            errors.append(f"ERROR: Estimated tokens {plan.estimated_tokens} exceeds max {constraints.max_tokens}")
            
        return errors
