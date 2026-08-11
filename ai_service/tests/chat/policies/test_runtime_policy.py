import pytest
from unittest.mock import AsyncMock
from app.chat.policies.runtime_policy import RuntimePolicyProxy
from app.chat.exceptions.chat_exceptions import ProviderFailure
from app.chat.context.execution_context import ExecutionContext
from app.models.chat.chat_models import ExecutionResult

@pytest.mark.asyncio
async def test_runtime_policy_proxy_success():
    mock_engine = AsyncMock()
    mock_engine.name = "MOCK"
    mock_engine.execute.return_value = ExecutionResult.success(engine="MOCK", message="Success")
    
    proxy = RuntimePolicyProxy(mock_engine)
    ctx = ExecutionContext()
    
    result = await proxy.execute(ctx)
    assert result.status == "SUCCESS"
    assert mock_engine.execute.call_count == 1

@pytest.mark.asyncio
async def test_runtime_policy_cancellation():
    mock_engine = AsyncMock()
    mock_engine.name = "MOCK"
    
    proxy = RuntimePolicyProxy(mock_engine)
    ctx = ExecutionContext().request_cancellation()
    
    result = await proxy.execute(ctx)
    assert result.status == "FAILED"
    assert "cancelled" in result.errors[0]["error"]
    # Ensure the wrapped engine was never called
    mock_engine.execute.assert_not_called()

# We won't strictly test tenacity retries sleeping in tests as it slows them down,
# but we can verify that unhandled exceptions are raised out of the proxy
@pytest.mark.asyncio
async def test_runtime_policy_passes_unhandled_errors():
    mock_engine = AsyncMock()
    mock_engine.name = "MOCK"
    mock_engine.execute.side_effect = ValueError("Fatal Error")
    
    proxy = RuntimePolicyProxy(mock_engine)
    ctx = ExecutionContext()
    
    with pytest.raises(ValueError):
        await proxy.execute(ctx)
