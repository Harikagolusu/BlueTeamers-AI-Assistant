import asyncio
from typing import Callable, Any, Awaitable, Tuple, Type
from app.runtime.interfaces.resilience import IResilienceStrategy

class RetryStrategy(IResilienceStrategy):
    """Simple exponential backoff retry strategy."""
    def __init__(self, max_attempts: int = 3, base_delay: float = 1.0, exceptions: Tuple[Type[Exception], ...] = (Exception,)):
        self.max_attempts = max_attempts
        self.base_delay = base_delay
        self.exceptions = exceptions

    async def execute(self, operation: Callable[..., Awaitable[Any]], *args, **kwargs) -> Any:
        from app.runtime.context_manager import RuntimeContextManager
        
        attempt = 1
        while True:
            try:
                # Update runtime context with attempt count
                RuntimeContextManager.update(retry_count=attempt - 1)
                return await operation(*args, **kwargs)
            except self.exceptions as e:
                if attempt >= self.max_attempts:
                    raise
                delay = self.base_delay * (2 ** (attempt - 1))
                await asyncio.sleep(delay)
                attempt += 1
