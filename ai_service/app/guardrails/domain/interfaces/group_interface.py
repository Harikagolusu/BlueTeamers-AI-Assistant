from abc import ABC, abstractmethod
from typing import List
from app.guardrails.domain.models.context import GuardrailContext
from app.guardrails.domain.models.result import GuardrailResult
from app.guardrails.domain.interfaces.policy_interface import IGuardrailPolicy
from app.guardrails.domain.models.enums import PolicyPriority

class IPolicyGroup(ABC):
    """Interface for a logical group of guardrail policies."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the policy group."""
        pass

    @property
    @abstractmethod
    def priority(self) -> PolicyPriority:
        """Priority of the group in the pipeline execution order."""
        pass

    @property
    @abstractmethod
    def policies(self) -> List[IGuardrailPolicy]:
        """List of policies managed by this group."""
        pass

    @abstractmethod
    async def evaluate_all(self, context: GuardrailContext) -> List[GuardrailResult]:
        """Evaluates all policies in the group, typically in parallel."""
        pass
