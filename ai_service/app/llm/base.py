from abc import ABC, abstractmethod
from typing import AsyncGenerator, Dict, Any
from app.llm.schemas import LLMRequest, LLMResponse

class BaseLLMProvider(ABC):
    """
    Abstract base class for all LLM providers.
    Ensures that every provider implements the exact same interface,
    allowing the frontend and business logic to remain completely agnostic
    of the underlying implementation.
    """
    
    @abstractmethod
    async def generate(self, request: LLMRequest) -> LLMResponse:
        """Generate a complete response from the LLM."""
        pass

    @abstractmethod
    async def stream_generate(self, request: LLMRequest) -> AsyncGenerator[str, None]:
        """Stream the response from the LLM chunk by chunk."""
        pass

    @abstractmethod
    async def health_check(self) -> Dict[str, Any]:
        """Check the health and latency of the provider."""
        pass
