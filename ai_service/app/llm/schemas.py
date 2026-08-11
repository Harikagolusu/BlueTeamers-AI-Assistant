from pydantic import BaseModel
from typing import Optional, Dict, Any, List


class LLMRequest(BaseModel):
    """Standardized request schema for all LLM providers."""
    prompt: str
    system_prompt: Optional[str] = None
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    context: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None
    stream: bool = False
    # Multimodal support: list of {mime, format, bytes} image payloads.
    images: Optional[List[Dict[str, Any]]] = None


class LLMResponse(BaseModel):
    """Standardized response schema for all LLM providers."""
    text: str
    provider: str
    model: str
    latency_ms: float
    finish_reason: Optional[str] = None
    usage: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None
