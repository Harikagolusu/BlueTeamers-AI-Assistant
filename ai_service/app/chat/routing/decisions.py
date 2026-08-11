"""Router request/decision/response models and structured request logging."""
import json
import logging
import time
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from app.chat.routing.domains import CyberDomain

logger = logging.getLogger("app.chat.router")


class RoutingDecision(BaseModel):
    """The single, deterministic outcome of the Query Router (no LLM involved)."""

    query: str = ""
    intent: str = "UNKNOWN"
    domain: CyberDomain = CyberDomain.GENERAL
    domain_confidence: float = 0.0
    agent_id: str = "general_assistant"
    agent_name: str = "General Assistant"
    engine: str = "GENERAL"
    llm_required: bool = True
    supports_recommendations: bool = False
    rationale: List[str] = Field(default_factory=list)


class RouterRequest(BaseModel):
    query: str
    token: Optional[str] = None
    conversation_id: Optional[str] = None
    stream: bool = False
    images: Optional[List[str]] = None
    files: Optional[List[Dict[str, Any]]] = None
    request_id: Optional[str] = None
    user_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None


class RouterResponse(BaseModel):
    """Structured engine output shaped for pure frontend rendering."""

    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    citations: List[Dict[str, Any]] = Field(default_factory=list)
    agent: str = "general_assistant"
    engine: str = "GENERAL"
    llm_used: bool = True
    recommendation_used: bool = False
    latency_ms: float = 0.0


class RoutingEventLogger:
    """Emits a single structured log line per routed request."""

    @staticmethod
    def log(
        *,
        query: str,
        intent: str,
        domain: str,
        agent_id: str,
        engine: str,
        repositories: List[str],
        llm_used: bool,
        recommendation_used: bool,
        latency_ms: float,
        status: str = "success",
    ) -> None:
        record = {
            "event": "chat_request_routed",
            "query": query,
            "intent": intent,
            "domain": domain,
            "agent": agent_id,
            "engine": engine,
            "repositories": repositories,
            "llm_used": llm_used,
            "recommendation_used": recommendation_used,
            "latency_ms": round(latency_ms, 2),
            "status": status,
            "timestamp": time.time(),
        }
        logger.info(json.dumps(record))
