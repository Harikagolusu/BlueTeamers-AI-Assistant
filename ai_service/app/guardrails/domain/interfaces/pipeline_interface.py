from abc import ABC, abstractmethod
from typing import List
from app.guardrails.domain.models.context import GuardrailContext
from app.guardrails.domain.interfaces.group_interface import IPolicyGroup

class IGuardrailPipeline(ABC):
    """Interface for a pipeline that orchestrates policy groups."""
    
    @abstractmethod
    def add_group(self, group: IPolicyGroup) -> None:
        """Adds a policy group to the pipeline."""
        pass
        
    @abstractmethod
    async def execute(self, context: GuardrailContext) -> GuardrailContext:
        """Executes the pipeline, potentially raising exceptions if blocked."""
        pass
