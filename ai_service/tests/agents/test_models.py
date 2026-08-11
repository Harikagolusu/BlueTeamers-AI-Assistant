import pytest
from app.planning.models.plan import ExecutionPlan, ExecutionStep, Capability
from app.agents.models.cursor import ExecutionCursor

def test_execution_cursor_initialization():
    step1 = ExecutionStep(name="A", required_capability=Capability.LLM)
    step2 = ExecutionStep(name="B", required_capability=Capability.RAG, dependencies=[step1.step_id])
    plan = ExecutionPlan(goal="Test DAG", steps=[step1, step2])
    
    cursor = ExecutionCursor.initialize(plan)
    
    assert cursor.current_node is None
    assert len(cursor.ready_queue) == 1
    assert cursor.ready_queue[0] == step1.step_id
    assert len(cursor.blocked_nodes) == 1
    assert step2.step_id in cursor.blocked_nodes

def test_execution_cursor_completion():
    step1 = ExecutionStep(name="A", required_capability=Capability.LLM)
    step2 = ExecutionStep(name="B", required_capability=Capability.RAG, dependencies=[step1.step_id])
    plan = ExecutionPlan(goal="Test DAG", steps=[step1, step2])
    
    cursor = ExecutionCursor.initialize(plan)
    
    # Simulate picking up step1
    cursor.current_node = cursor.ready_queue.pop(0)
    
    # Complete step1
    cursor.mark_completed(step1.step_id, plan)
    
    # Step2 should now be unblocked and ready
    assert step1.step_id in cursor.completed_nodes
    assert len(cursor.blocked_nodes) == 0
    assert len(cursor.ready_queue) == 1
    assert cursor.ready_queue[0] == step2.step_id
    assert cursor.current_node is None
