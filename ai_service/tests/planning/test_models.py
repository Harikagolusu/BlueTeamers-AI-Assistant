import pytest
from pydantic import ValidationError
from app.planning.models.plan import ExecutionPlan, ExecutionStep, Capability, ExecutionPlanStatus

def test_execution_plan_immutability():
    plan = ExecutionPlan(goal="Test")
    with pytest.raises(ValidationError):
        plan.goal = "Changed Goal"

def test_execution_step_creation():
    step = ExecutionStep(name="Step 1", required_capability=Capability.LLM)
    assert step.step_id is not None
    assert step.required_capability == Capability.LLM

def test_plan_status():
    plan = ExecutionPlan(goal="Test", status=ExecutionPlanStatus.DRAFT)
    assert plan.status == ExecutionPlanStatus.DRAFT
