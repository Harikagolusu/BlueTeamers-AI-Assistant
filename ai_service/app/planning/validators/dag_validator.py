from typing import List, Dict, Set
from app.planning.models.plan import ExecutionPlan

class DAGValidator:
    """Validates that the ExecutionPlan steps form a valid Directed Acyclic Graph (DAG)."""
    
    @staticmethod
    def validate(plan: ExecutionPlan) -> List[str]:
        errors = []
        if not plan.steps:
            return ["ERROR: Plan must contain at least one step."]
            
        step_ids = {step.step_id for step in plan.steps}
        adj_list: Dict[str, List[str]] = {step.step_id: step.dependencies for step in plan.steps}
        
        # 1. Check for missing dependencies
        for step in plan.steps:
            for dep in step.dependencies:
                if dep not in step_ids:
                    errors.append(f"ERROR: Step {step.step_id} depends on non-existent step {dep}.")
                    
        # 2. Check for circular dependencies (DFS)
        visited = set()
        rec_stack = set()
        
        def is_cyclic(node: str) -> bool:
            visited.add(node)
            rec_stack.add(node)
            
            for neighbor in adj_list.get(node, []):
                if neighbor not in visited:
                    if is_cyclic(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True
                    
            rec_stack.remove(node)
            return False
            
        for step_id in step_ids:
            if step_id not in visited:
                if is_cyclic(step_id):
                    errors.append("ERROR: Circular dependency detected in plan steps.")
                    break
                    
        return errors
