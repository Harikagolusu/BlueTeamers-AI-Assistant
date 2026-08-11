"""QueryRouter: the single deterministic entry point for every chat request.

Responsibilities:
  1. classify(query, intent_analysis) -> RoutingDecision   (pure, no LLM)
  2. process(request) -> RouterResponse | AsyncGenerator   (run pipeline + shape output)

The QueryRouter never generates responses and never calls the LLM directly.
LLM usage is owned by the selected agent's engine and is always gated.
"""
import logging
import time
import uuid
from typing import AsyncGenerator, Dict, Any, Union

from app.chat.intent.intent_service import IntentIntelligenceService
from app.chat.interfaces.i_chat_service import IChatService
from app.chat.response.builder import ResponseBuilder
from app.chat.routing.agents import AgentCatalog
from app.chat.routing.decisions import (
    RoutingDecision,
    RoutingEventLogger,
    RouterRequest,
    RouterResponse,
)
from app.chat.routing.domains import DomainClassifier
from app.models.chat.chat_models import ChatRequest as DomainChatRequest

logger = logging.getLogger("app.chat.router.query_router")


class QueryRouter:
    def __init__(
        self,
        intent_service: IntentIntelligenceService,
        catalog: AgentCatalog | None = None,
        chat_service: IChatService | None = None,
        response_builder: ResponseBuilder | None = None,
    ):
        self._intent_service = intent_service
        self._classifier = DomainClassifier()
        self._catalog = catalog or AgentCatalog()
        self._chat_service = chat_service
        self._response_builder = response_builder or ResponseBuilder()

    @property
    def catalog(self) -> AgentCatalog:
        return self._catalog

    async def analyze_intent(self, query: str, conversation_context: Dict[str, Any] | None = None):
        return await self._intent_service.analyze_intent(query, conversation_context or {})

    def classify(
        self, query: str, intent_analysis: Any = None
    ) -> RoutingDecision:
        """Deterministic classify -> select exactly one agent -> engine. No LLM."""
        domain, confidence, rationale = self._classifier.classify(query, intent_analysis)
        agent = self._catalog.select_for_domain(domain)

        intent = "UNKNOWN"
        if intent_analysis and getattr(intent_analysis, "primary_intent", None):
            intent = intent_analysis.primary_intent.type.value

        decision = RoutingDecision(
            query=query,
            intent=intent,
            domain=domain,
            domain_confidence=confidence,
            agent_id=agent.agent_id,
            agent_name=agent.name,
            engine=agent.engine,
            llm_required=agent.llm_required,
            supports_recommendations=agent.supports_recommendations,
            rationale=rationale,
        )
        logger.info(
            "QueryRouter decision: agent=%s engine=%s domain=%s intent=%s rationale=%s",
            decision.agent_id,
            decision.engine,
            decision.domain.value,
            decision.intent,
            ",".join(rationale),
        )
        return decision

    async def process(
        self, request: RouterRequest
    ) -> Union[RouterResponse, AsyncGenerator[str, None]]:
        """Route one request through the pipeline and shape the structured output."""
        start = time.time()
        req_id = request.request_id or uuid.uuid4()

        domain_request = DomainChatRequest(
            conversation_id=request.conversation_id,
            message=request.query,
            query=request.query,
            stream=request.stream,
            token=request.token,
            images=request.images,
            files=request.files,
            user_id=request.user_id,
            context=request.context,
        )

        result = await self._chat_service.process_request(domain_request)

        if request.stream:
            return self._enrich_stream(result, request, req_id, start)

        latency = (time.time() - start) * 1000
        response = self._response_builder.from_chat_response(result, request)
        response.latency_ms = latency
        self._log_event(request, response, latency)
        return response

    async def _enrich_stream(self, generator, request: RouterRequest, req_id, start):
        """Forward stream tokens and log routing fields from the final metadata event."""
        import json as _json
        final_metadata: Dict[str, Any] = {}
        try:
            async for chunk in generator:
                yield chunk
                if isinstance(chunk, str) and '"metadata"' in chunk:
                    try:
                        prefix, sep, rest = chunk.partition("data: ")
                        if sep:
                            payload = _json.loads(rest.strip())
                            if isinstance(payload.get("metadata"), dict):
                                final_metadata = payload["metadata"]
                    except Exception:
                        pass
        finally:
            latency = (time.time() - start) * 1000
            self._log_event(request, RouterResponse(content="", metadata=final_metadata), latency)

    def _log_event(
        self,
        request: RouterRequest,
        response: RouterResponse,
        latency_ms: float,
    ) -> None:
        md = response.metadata or {}
        repositories = md.get("repositories", [])
        RoutingEventLogger.log(
            query=request.query,
            intent=md.get("intent", ""),
            domain=md.get("domain", ""),
            agent_id=md.get("agent", ""),
            engine=md.get("engine", ""),
            repositories=list(repositories),
            llm_used=bool(md.get("llm_used", False)),
            recommendation_used=bool(md.get("recommendation_used", False)),
            latency_ms=latency_ms,
        )
