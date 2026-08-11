import asyncio
from typing import Callable, Any, Awaitable
from app.runtime.interfaces.resilience import IResilienceStrategy

class TimeoutStrategy(IResilienceStrategy):
    """Enforces a strict timeout on the operation."""
    def __init__(self, timeout_seconds: float):
        self.timeout_seconds = timeout_seconds

    async def execute(self, operation: Callable[..., Awaitable[Any]], *args, **kwargs) -> Any:
        try:
            return await asyncio.wait_for(operation(*args, **kwargs), timeout=self.timeout_seconds)
        except asyncio.TimeoutError as e:
            # Re-raise as a standard Exception or a specific TimeoutException if you have one
            raise TimeoutError(f"Operation timed out after {self.timeout_seconds}s") from e
