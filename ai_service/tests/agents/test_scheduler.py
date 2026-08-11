import pytest
from app.planning.models.plan import ExecutionPlan, ExecutionStep, Capability
from app.agents.models.cursor import ExecutionCursor
from app.agents.schedulers.sequential_scheduler import SequentialScheduler

def test_sequential_scheduler_yields_ready():
    step1 = ExecutionStep(name="A", required_capability=Capability.LLM)
    plan = ExecutionPlan(goal="Test", steps=[step1])
    cursor = ExecutionCursor.initialize(plan)
    
    scheduler = SequentialScheduler()
    next_step = scheduler.get_next_step(plan, cursor)
    assert next_step is not None
    assert next_step.step_id == step1.step_id
    assert cursor.current_node == step1.step_id

def test_sequential_scheduler_waits_for_completion():
    step1 = ExecutionStep(name="A", required_capability=Capability.LLM)
    plan = ExecutionPlan(goal="Test", steps=[step1])
    cursor = ExecutionCursor.initialize(plan)
    
    scheduler = SequentialScheduler()
    scheduler.get_next_step(plan, cursor)
    
    # Try calling again before completion
    next_step_again = scheduler.get_next_step(plan, cursor)
    assert next_step_again is None # Prevent concurrent dispatch
