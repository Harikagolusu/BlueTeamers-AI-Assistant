import pytest
from app.runtime.context_manager import RuntimeContextManager

def test_context_lifecycle():
    token = RuntimeContextManager.initialize("test-trace", "test-session", "user-1")
    ctx = RuntimeContextManager.get()
    
    assert ctx.trace_id == "test-trace"
    assert ctx.session_id == "test-session"
    assert ctx.user_id == "user-1"
    assert ctx.retry_count == 0
    
    RuntimeContextManager.update(retry_count=1, cache_status="HIT")
    
    updated_ctx = RuntimeContextManager.get()
    assert updated_ctx.retry_count == 1
    assert updated_ctx.cache_status == "HIT"
    assert updated_ctx.trace_id == "test-trace" # Unchanged
    
    RuntimeContextManager.dispose(token)
    
    with pytest.raises(LookupError):
        RuntimeContextManager.get()
