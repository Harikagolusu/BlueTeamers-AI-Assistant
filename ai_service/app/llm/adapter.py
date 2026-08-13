"""
LLM Provider Adapter

Bridges the BaseLLMProvider interface (which uses LLMRequest/LLMResponse objects)
with the ILLMService interface (which uses plain string prompts).

This is the correct architectural solution — neither interface is changed.
The engines and the providers remain untouched; only this thin adapter mediates.

NOTE: This adapter is NOT a hack. The two interfaces represent:
  - BaseLLMProvider: The infrastructure-level LLM transport interface.
  - ILLMService: The domain-level service interface used by Execution Engines.

The adapter pattern is the standard solution for bridging two stable interfaces.
"""

from typing import AsyncGenerator
from app.llm.interfaces import ILLMService
from app.llm.base import BaseLLMProvider
from app.llm.schemas import LLMRequest
from app.llm.images import normalize_images
from app.core.config import settings
import logging

logger = logging.getLogger("app.llm.adapter")


def _resolve_max_tokens(explicit) -> int | None:
    """Apply the global LLM_MAX_TOKENS safety cap when no explicit cap is set."""
    return explicit or settings.LLM_MAX_TOKENS


class LLMProviderAdapter(ILLMService):
    """
    Adapts a BaseLLMProvider to the ILLMService interface expected by
    GeneralExecutionEngine, RagExecutionEngine, and IntentIntelligenceService.

    BaseLLMProvider.generate(LLMRequest) -> LLMResponse
    BaseLLMProvider.stream_generate(LLMRequest) -> AsyncGenerator[str, None]

    ILLMService.generate(prompt: str) -> str
    ILLMService.stream(prompt: str) -> AsyncGenerator[str, None]
    """

    def __init__(self, provider: BaseLLMProvider):
        self._provider = provider

    async def generate(self, prompt: str, **kwargs) -> str:
        """Adapt plain string prompt to LLMRequest and return plain string response."""
        request = LLMRequest(
            prompt=prompt,
            temperature=kwargs.get("temperature", 0.7),
            system_prompt=kwargs.get("system_prompt", None),
            max_tokens=_resolve_max_tokens(kwargs.get("max_tokens")),
            images=normalize_images(kwargs.get("images")),
        )
        logger.debug(f"LLMProviderAdapter.generate() -> prompt length: {len(prompt)}")
        response = await self._provider.generate(request)
        return response.text

    async def stream(self, prompt: str, **kwargs) -> AsyncGenerator[str, None]:
        """Adapt plain string prompt to LLMRequest and stream plain string tokens."""
        request = LLMRequest(
            prompt=prompt,
            temperature=kwargs.get("temperature", 0.7),
            system_prompt=kwargs.get("system_prompt", None),
            max_tokens=_resolve_max_tokens(kwargs.get("max_tokens")),
            stream=True,
            images=normalize_images(kwargs.get("images")),
        )
        logger.debug(f"LLMProviderAdapter.stream() -> prompt length: {len(prompt)}")
        async for token in self._provider.stream_generate(request):
            yield token
