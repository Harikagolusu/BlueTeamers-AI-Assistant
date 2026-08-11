from abc import ABC, abstractmethod
from app.guardrails.domain.models.context import GuardrailContext

class IGuardrailsService(ABC):
    """Facade for the guardrails module."""
    
    @abstractmethod
    async def validate_input(self, context: GuardrailContext) -> GuardrailContext:
        """Validates the input prior to RAG/LLM processing."""
        pass
        
    @abstractmethod
    async def validate_output(self, context: GuardrailContext) -> GuardrailContext:
        """Validates the output after RAG/LLM processing."""
        pass
