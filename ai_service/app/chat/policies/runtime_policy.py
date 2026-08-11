from typing import Any
from app.chat.exceptions.chat_exceptions import ProviderFailure, TimeoutError
from app.chat.interfaces.i_execution_engine import IExecutionEngine
from app.chat.context.execution_context import ExecutionContext
from app.models.chat.chat_models import ExecutionResult

from app.runtime.resilience.retry import RetryStrategy
from app.runtime.resilience.circuit_breaker import CircuitBreaker
from app.runtime.resilience.timeout import TimeoutStrategy

class RuntimePolicyProxy(IExecutionEngine):
    """
    Wraps an ExecutionEngine with enterprise Runtime Policies (Retries, Timeouts, Circuit Breakers)
    using the dedicated runtime strategy interfaces.
    """
    def __init__(self, target_engine: IExecutionEngine):
        self._engine = target_engine
        
        # Compose resilience strategies
        self._timeout = TimeoutStrategy(timeout_seconds=300.0)
        self._circuit_breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=60.0, exceptions=(ProviderFailure, TimeoutError))
        self._retry = RetryStrategy(max_attempts=3, base_delay=1.0, exceptions=(ProviderFailure, TimeoutError))

    @property
    def name(self) -> str:
        return self._engine.name

    async def execute(self, context: ExecutionContext) -> ExecutionResult:
        if context.cancellation_requested:
            return ExecutionResult.failed(
                engine=self.name,
                errors=[{"error": "Request was cancelled prior to execution."}]
            )
            
        # Execute through the nested resilience strategies
        # Execution flow: Retry -> Circuit Breaker -> Timeout -> Engine
        
        async def _execute_with_timeout(*args, **kwargs):
            return await self._timeout.execute(self._engine.execute, *args, **kwargs)
            
        async def _execute_with_circuit_breaker(*args, **kwargs):
            return await self._circuit_breaker.execute(_execute_with_timeout, *args, **kwargs)
            
        # Use retry as the outermost strategy
        return await self._retry.execute(_execute_with_circuit_breaker, context)
