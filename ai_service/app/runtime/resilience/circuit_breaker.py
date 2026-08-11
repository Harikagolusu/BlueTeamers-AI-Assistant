import asyncio
import time
from typing import Callable, Any, Awaitable, Tuple, Type
from app.runtime.interfaces.resilience import IResilienceStrategy

class CircuitOpenException(Exception):
    pass

class CircuitBreaker(IResilienceStrategy):
    """
    Stateful circuit breaker.
    Closed -> Open (on failure threshold) -> Half-Open (after timeout) -> Closed (on success)
    """
    def __init__(self, failure_threshold: int = 3, recovery_timeout: float = 30.0, exceptions: Tuple[Type[Exception], ...] = (Exception,)):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.exceptions = exceptions
        
        self.failures = 0
        self.state = "CLOSED"
        self.last_failure_time = 0.0

    async def execute(self, operation: Callable[..., Awaitable[Any]], *args, **kwargs) -> Any:
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = "HALF_OPEN"
            else:
                raise CircuitOpenException("Circuit is OPEN.")
                
        try:
            result = await operation(*args, **kwargs)
            if self.state == "HALF_OPEN":
                self._reset()
            return result
        except self.exceptions as e:
            self._record_failure()
            raise

    def _record_failure(self):
        self.failures += 1
        self.last_failure_time = time.time()
        if self.failures >= self.failure_threshold:
            self.state = "OPEN"
            
    def _reset(self):
        self.failures = 0
        self.state = "CLOSED"
