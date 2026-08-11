from fastapi import Depends
from app.llm.base import BaseLLMProvider
from app.llm.factory import LLMFactory

def get_llm_provider() -> BaseLLMProvider:
    """
    FastAPI dependency injection for the LLM Provider.
    Routes and AI agents should depend on this abstract interface,
    ensuring they are decoupled from the specific provider.
    """
    return LLMFactory.get_provider()
