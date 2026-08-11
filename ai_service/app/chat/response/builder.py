"""Structured response building for pure frontend rendering."""
from typing import Any, Dict, List

from app.models.chat.chat_models import ChatResponse, ExecutionResult
from app.chat.routing.decisions import RoutingDecision, RouterResponse


def _platform_cards(result_metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
    nested = result_metadata.get("platform", {})
    cards = (
        result_metadata.get("platform_cards")
        or nested.get("cards")
        or []
    )
    return list(cards)


def _actions(result_metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
    nested = result_metadata.get("platform", {})
    return list(result_metadata.get("actions") or nested.get("actions") or [])


class ResponseBuilder:
    """Shapes engine output into the standard {content, metadata} contract."""

    def build(
        self,
        result: ExecutionResult,
        decision: RoutingDecision | None = None,
        trace_id: str = "",
    ) -> RouterResponse:
        result_metadata = result.metadata or {}
        agent = decision.agent_id if decision else result_metadata.get("agent", "general_assistant")
        engine = decision.engine if decision else result_metadata.get("engine", result.engine_name)
        llm_used = result_metadata.get("llm_used", bool(decision.llm_required) if decision else True)
        recommendation_used = result_metadata.get("recommendation_used", False)

        metadata = {
            "agent": agent,
            "engine": engine,
            "llm_used": llm_used,
            "recommendation_used": recommendation_used,
            "platform_cards": _platform_cards(result_metadata),
            "actions": _actions(result_metadata),
            "citations": result.citations,
            "sources": result.documents,
            "course_sources": result_metadata.get("course_sources", []),
            "latency": result.latency_ms,
            "trace_id": trace_id,
            **result_metadata,
        }
        metadata.pop("generator", None)

        return RouterResponse(
            content=result.message,
            metadata=metadata,
            citations=result.citations,
            agent=agent,
            engine=engine,
            llm_used=llm_used,
            recommendation_used=recommendation_used,
            latency_ms=result.latency_ms,
        )

    def from_chat_response(
        self,
        chat_response: ChatResponse,
        request: Any = None,
    ) -> RouterResponse:
        metadata = dict(chat_response.metadata or {})
        agent = metadata.get("agent", "general_assistant")
        engine = metadata.get("engine", "GENERAL")
        llm_used = metadata.get("llm_used", True)
        recommendation_used = metadata.get("recommendation_used", False)

        # Guarantee the structured contract is always present for the frontend.
        metadata["agent"] = agent
        metadata["engine"] = engine
        metadata["llm_used"] = bool(llm_used)
        metadata["recommendation_used"] = bool(recommendation_used)
        metadata.setdefault("platform_cards", [])
        metadata.setdefault("actions", [])
        metadata.setdefault("sources", [])
        metadata.setdefault("course_sources", [])
        metadata.setdefault("citations", [])

        return RouterResponse(
            content=chat_response.message,
            metadata=metadata,
            citations=list(metadata.get("citations", [])),
            agent=agent,
            engine=engine,
            llm_used=bool(llm_used),
            recommendation_used=bool(recommendation_used),
            latency_ms=float(metadata.get("latency", 0.0)),
        )
