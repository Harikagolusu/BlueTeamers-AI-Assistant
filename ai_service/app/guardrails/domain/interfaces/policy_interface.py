from abc import ABC, abstractmethod
from typing import Dict, Any
from app.guardrails.domain.models.context import GuardrailContext
from app.guardrails.domain.models.result import GuardrailResult

class IGuardrailPolicy(ABC):
    """Interface for a single guardrail policy."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the policy."""
        pass
        
    @property
    @abstractmethod
    def metadata(self) -> Dict[str, Any]:
        """Metadata about the policy (version, author, etc.)."""
        pass

    @abstractmethod
    async def evaluate(self, context: GuardrailContext) -> GuardrailResult:
        """Evaluates the context against the policy."""
        pass

    async def before_policy(self, context: GuardrailContext) -> None:
        """Optional lifecycle hook called before evaluation."""
        pass
        
    async def after_policy(self, context: GuardrailContext, result: GuardrailResult) -> None:
        """Optional lifecycle hook called after evaluation."""
        pass
        
    async def cleanup(self) -> None:
        """Optional lifecycle hook for resource cleanup."""
        pass
