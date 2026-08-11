from abc import ABC, abstractmethod
from typing import Callable, Any, Awaitable

class IResilienceStrategy(ABC):
    @abstractmethod
    async def execute(self, operation: Callable[..., Awaitable[Any]], *args, **kwargs) -> Any:
        """Executes an operation wrapped in the specific resilience policy."""
        pass
