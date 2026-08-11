from app.planning.models.plan import ExecutionPlan, Capability

class HeuristicEstimator:
    """Provides static heuristic estimates for plans without invoking LLMs."""
    
    @staticmethod
    def estimate(plan: ExecutionPlan) -> None:
        cost = 0.0
        tokens = 0
        time_ms = 0.0
        
        for step in plan.steps:
            if step.required_capability == Capability.LLM:
                cost += 0.02
                tokens += 1000
                time_ms += 1500
            elif step.required_capability == Capability.RAG:
                cost += 0.03
                tokens += 1500
                time_ms += 2500
            elif step.required_capability == Capability.TOOL:
                cost += 0.01
                tokens += 500
                time_ms += 800
            else:
                cost += 0.005
                tokens += 200
                time_ms += 500
                
        # Update the plan via object.__setattr__ to bypass immutability for initialization
        object.__setattr__(plan, "estimated_cost", cost)
        object.__setattr__(plan, "estimated_tokens", tokens)
        object.__setattr__(plan, "estimated_time_ms", time_ms)
