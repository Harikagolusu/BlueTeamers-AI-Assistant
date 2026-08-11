import pytest
from app.planning.models.plan import ExecutionPlan, ExecutionStep, Capability
from app.planning.estimation.heuristic_estimator import HeuristicEstimator

def test_heuristic_estimation():
    step1 = ExecutionStep(name="A", required_capability=Capability.LLM) # 0.02, 1000, 1500
    step2 = ExecutionStep(name="B", required_capability=Capability.RAG) # 0.03, 1500, 2500
    plan = ExecutionPlan(goal="Test", steps=[step1, step2])
    
    HeuristicEstimator.estimate(plan)
    
    assert plan.estimated_cost == 0.05
    assert plan.estimated_tokens == 2500
    assert plan.estimated_time_ms == 4000.0
