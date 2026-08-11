import pytest
import uuid
from app.chat.context.execution_context import ExecutionContext

def test_execution_context_immutability():
    ctx = ExecutionContext()
    
    # Attempting to mutate a field directly should raise an exception
    with pytest.raises(Exception):
        ctx.streaming_mode = True

def test_execution_context_with_memory():
    ctx = ExecutionContext()
    memory_update = {"turns": ["hello", "world"]}
    
    new_ctx = ctx.with_memory(memory_update)
    
    # Original shouldn't change
    assert ctx.memory == {}
    # New should have the update
    assert new_ctx.memory == memory_update
    
    # IDs should be preserved across immutability updates
    assert ctx.correlation_id == new_ctx.correlation_id
    assert ctx.trace_id == new_ctx.trace_id

def test_execution_context_cancellation():
    ctx = ExecutionContext()
    new_ctx = ctx.request_cancellation()
    
    assert ctx.cancellation_requested is False
    assert new_ctx.cancellation_requested is True
