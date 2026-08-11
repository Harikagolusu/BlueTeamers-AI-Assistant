import pytest
import asyncio
import time
from app.runtime.resilience.retry import RetryStrategy
from app.runtime.resilience.timeout import TimeoutStrategy
from app.runtime.resilience.circuit_breaker import CircuitBreaker, CircuitOpenException
from app.runtime.context_manager import RuntimeContextManager

@pytest.mark.asyncio
async def test_retry_strategy_success():
    strategy = RetryStrategy(max_attempts=3, base_delay=0.1)
    
    attempts = 0
    async def _failing_op():
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise ValueError("Failed")
        return "Success"
        
    with RuntimeContextManager.lifecycle(trace_id="test-trace"):
        result = await strategy.execute(_failing_op)
        assert result == "Success"
        assert attempts == 3
        ctx = RuntimeContextManager.get()
        assert ctx.retry_count == 2

@pytest.mark.asyncio
async def test_retry_strategy_failure():
    strategy = RetryStrategy(max_attempts=2, base_delay=0.1)
    
    async def _failing_op():
        raise ValueError("Failed")
        
    with RuntimeContextManager.lifecycle(trace_id="test-trace"):
        with pytest.raises(ValueError):
            await strategy.execute(_failing_op)

@pytest.mark.asyncio
async def test_timeout_strategy():
    strategy = TimeoutStrategy(timeout_seconds=0.2)
    
    async def _slow_op():
        await asyncio.sleep(0.5)
        return "Success"
        
    with pytest.raises(TimeoutError):
        await strategy.execute(_slow_op)

@pytest.mark.asyncio
async def test_circuit_breaker():
    breaker = CircuitBreaker(failure_threshold=2, recovery_timeout=0.2)
    
    async def _failing_op():
        raise ValueError("Failed")
        
    async def _success_op():
        return "Success"
        
    # First failure (CLOSED)
    with pytest.raises(ValueError):
        await breaker.execute(_failing_op)
    assert breaker.state == "CLOSED"
    
    # Second failure trips breaker (CLOSED -> OPEN)
    with pytest.raises(ValueError):
        await breaker.execute(_failing_op)
    assert breaker.state == "OPEN"
    
    # Third failure immediately raises CircuitOpenException
    with pytest.raises(CircuitOpenException):
        await breaker.execute(_success_op)
        
    # Wait for recovery timeout
    await asyncio.sleep(0.3)
    
    # Next call goes through (HALF_OPEN) and succeeds, closing circuit
    result = await breaker.execute(_success_op)
    assert result == "Success"
    assert breaker.state == "CLOSED"
