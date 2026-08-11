from app.platform.platform_agent_orchestrator.models import ExecutionPlan

class PlanValidationException(Exception):
    pass

class PlanValidatorService:
    def validate(self, plan: ExecutionPlan) -> bool:
        """
        Validates the execution plan for circular dependencies, missing targets, etc.
        """
        if not plan.execution_steps:
            return True # Allowed for general chat or unknown intent
            
        step_ids = {step.step_id for step in plan.execution_steps}
        
        for step in plan.execution_steps:
            if not step.target_agent:
                raise PlanValidationException(f"Step {step.step_id} missing target agent for capability {step.capability}.")
            
            for dep in step.dependencies:
                if dep not in step_ids:
                    raise PlanValidationException(f"Step {step.step_id} has unresolvable dependency {dep}.")
        
        # Simple circular dependency check (Kahn's algorithm or DFS could be used here)
        # Assuming linear ordering via execution_order for MVP
        for step in plan.execution_steps:
            for dep in step.dependencies:
                dep_step = next((s for s in plan.execution_steps if s.step_id == dep), None)
                if dep_step and dep_step.execution_order >= step.execution_order:
                    raise PlanValidationException(f"Circular or out-of-order dependency detected between {step.step_id} and {dep_step.step_id}.")
                    
        return True
