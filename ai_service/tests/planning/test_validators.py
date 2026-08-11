import pytest
from app.planning.models.plan import ExecutionPlan, ExecutionStep, Capability
from app.planning.validators.dag_validator import DAGValidator

def test_dag_validator_valid():
    step1 = ExecutionStep(name="A", required_capability=Capability.LLM)
    step2 = ExecutionStep(name="B", required_capability=Capability.LLM, dependencies=[step1.step_id])
    plan = ExecutionPlan(goal="Test", steps=[step1, step2])
    
    errors = DAGValidator.validate(plan)
    assert len(errors) == 0

def test_dag_validator_missing_dependency():
    step1 = ExecutionStep(name="A", required_capability=Capability.LLM, dependencies=["nonexistent_id"])
    plan = ExecutionPlan(goal="Test", steps=[step1])
    
    errors = DAGValidator.validate(plan)
    assert len(errors) == 1
    assert "depends on non-existent step" in errors[0]

def test_dag_validator_circular_dependency():
    step1 = ExecutionStep(name="A", required_capability=Capability.LLM)
    step2 = ExecutionStep(name="B", required_capability=Capability.LLM)
    
    # Create cycle A -> B -> A
    step1.dependencies = [step2.step_id]
    step2.dependencies = [step1.step_id]
    
    plan = ExecutionPlan(goal="Test", steps=[step1, step2])
    errors = DAGValidator.validate(plan)
    
    assert len(errors) == 1
    assert "Circular dependency detected" in errors[0]
