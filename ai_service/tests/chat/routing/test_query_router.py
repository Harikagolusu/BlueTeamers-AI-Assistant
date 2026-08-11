import pytest
from unittest.mock import AsyncMock, MagicMock

from app.chat.routing.agents import AgentCatalog
from app.chat.routing.domains import CyberDomain, DomainClassifier
from app.chat.routing.decisions import RouterRequest, RouterResponse
from app.chat.routing.query_router import QueryRouter
from app.chat.response.builder import ResponseBuilder
from app.models.chat.chat_models import ChatResponse, ExecutionResult


def _analysis(intent_type):
    analysis = MagicMock()
    analysis.primary_intent.type = intent_type
    return analysis


def _classifier():
    return DomainClassifier()


def test_platform_intent_maps_to_platform_domain():
    from app.chat.intent.models.intent_types import IntentType
    domain, confidence, _ = _classifier().classify(
        "What courses do I have?", _analysis(IntentType.PLATFORM_COURSE)
    )
    assert domain == CyberDomain.PLATFORM
    assert confidence > 0.9


def test_learning_signal_overrides_to_learning_domain():
    from app.chat.intent.models.intent_types import IntentType
    domain, _, _ = _classifier().classify(
        "Create a learning plan to become a SOC analyst", _analysis(IntentType.RAG_CHAT)
    )
    assert domain == CyberDomain.LEARNING


def test_threat_intel_signal_overrides_to_threat_intel():
    from app.chat.intent.models.intent_types import IntentType
    domain, _, _ = _classifier().classify(
        "What is MITRE ATT&CK and who is APT28?", _analysis(IntentType.RAG_CHAT)
    )
    assert domain == CyberDomain.THREAT_INTEL


def test_plain_knowledge_question_stays_knowledge():
    from app.chat.intent.models.intent_types import IntentType
    domain, _, _ = _classifier().classify(
        "what is a SIEM?", _analysis(IntentType.RAG_CHAT)
    )
    assert domain == CyberDomain.KNOWLEDGE


def test_catalog_selects_exactly_one_agent_per_domain():
    catalog = AgentCatalog()
    seen = set()
    for domain in CyberDomain:
        agent = catalog.select_for_domain(domain)
        seen.add(agent.agent_id)
        assert catalog.get(agent.agent_id) is agent
    # Exactly one distinct agent per domain, and never the whole catalog.
    assert len(seen) == len(CyberDomain)


def test_classify_routes_platform_question_to_platform_agent():
    from app.chat.intent.models.intent_types import IntentType
    intent_service = AsyncMock()
    router = QueryRouter(intent_service)
    decision = router.classify("What courses do I have?", _analysis(IntentType.PLATFORM_COURSE))
    assert decision.agent_id == "platform_assistant"
    assert decision.engine == "PLATFORM"
    assert decision.llm_required is False


def test_classify_routes_learning_plan_to_learning_coach():
    from app.chat.intent.models.intent_types import IntentType
    intent_service = AsyncMock()
    router = QueryRouter(intent_service)
    decision = router.classify(
        "Build me a learning plan for threat hunting", _analysis(IntentType.RAG_CHAT)
    )
    assert decision.agent_id == "learning_coach"
    assert decision.engine == "LEARNING_COACH"
    assert decision.supports_recommendations is True


@pytest.mark.asyncio
async def test_process_routes_through_chat_service_and_builds_structured_response():
    intent_service = AsyncMock()
    chat_service = AsyncMock()
    chat_service.process_request.return_value = ChatResponse(
        conversation_id="c1",
        message="Structured answer",
        metadata={
            "agent": "platform_assistant",
            "engine": "PLATFORM",
            "llm_used": False,
            "recommendation_used": True,
            "platform_cards": [{"title": "SIEM"}],
            "actions": [],
            "sources": [],
            "citations": [],
            "latency": 12.3,
        },
        used_tools=[],
    )
    router = QueryRouter(intent_service, chat_service=chat_service, response_builder=ResponseBuilder())

    response = await router.process(
        RouterRequest(query="What courses do I have?", token="t", conversation_id="c1")
    )

    assert isinstance(response, RouterResponse)
    assert response.content == "Structured answer"
    assert response.agent == "platform_assistant"
    assert response.engine == "PLATFORM"
    assert response.llm_used is False
    assert response.recommendation_used is True
    assert response.metadata["platform_cards"] == [{"title": "SIEM"}]
    chat_service.process_request.assert_awaited_once()


def test_response_builder_shapes_execution_result():
    from app.chat.routing.decisions import RoutingDecision
    decision = RoutingDecision(
        query="q", domain=CyberDomain.PLATFORM, agent_id="platform_assistant",
        agent_name="Platform Assistant", engine="PLATFORM", llm_required=False,
    )
    result = ExecutionResult.success(
        engine="PLATFORM",
        message="Your courses: SIEM",
        metadata={
            "platform_cards": [{"title": "SIEM"}],
            "actions": [{"label": "Go"}],
            "llm_used": False,
        },
        documents=[{"content": "x", "metadata": {}}],
        citations=[{"course": "c"}],
    )
    built = ResponseBuilder().build(result, decision, trace_id="trace-1")

    assert built.content == "Your courses: SIEM"
    assert built.agent == "platform_assistant"
    assert built.llm_used is False
    assert built.metadata["platform_cards"] == [{"title": "SIEM"}]
    assert built.metadata["sources"] == [{"content": "x", "metadata": {}}]
    assert built.metadata["citations"] == [{"course": "c"}]
