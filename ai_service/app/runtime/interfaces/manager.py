from abc import ABC, abstractmethod
from app.runtime.models.context import RuntimeContext
from typing import Callable, Any, Awaitable

class IRuntimeManager(ABC):
    """
    Central Façade coordinating Governance, Telemetry, Accounting, and Resilience.
    """
    @abstractmethod
    async def execute_with_governance(self, operation: Callable[..., Awaitable[Any]], context: RuntimeContext) -> Any:
        """
        Applies rate limiting, quota checks, and audit logging before/after execution.
        """
        pass
        
    @abstractmethod
    async def execute_with_resilience(self, operation: Callable[..., Awaitable[Any]], *args, **kwargs) -> Any:
        """
        Applies resilience strategies (Retry, Circuit Breaker) for engine calls.
        """
        pass
        
    @abstractmethod
    async def check_health(self) -> dict:
        pass
