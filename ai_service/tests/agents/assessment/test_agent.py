import pytest
from unittest.mock import AsyncMock, MagicMock

from app.agents.assessment.agent import AssessmentAgent
from app.agents.assessment.events import AssessmentEventPublisher
from app.agents.assessment.fallback import generate_questions, evaluate_fallback
from app.agents.assessment.models import (
    DifficultyLevel,
    QuestionType,
    QuizSession,
    QuizSessionStatus,
)
from app.agents.assessment.prompts import parse_json
from app.agents.assessment.profile_store import InMemoryAssessmentProfileStore
from app.agents.assessment.session_store import InMemoryQuizSessionStore
from app.agents.events.agent_events import AssessmentStartedEvent


class FakeSettings:
    ENABLE_ASSESSMENT_AGENT = True
    ASSESSMENT_MINIMUM_CONFIDENCE_THRESHOLD = 0.6
    ASSESSMENT_DEFAULT_QUIZ_LENGTH = 3
    ASSESSMENT_DEFAULT_DIFFICULTY = "beginner"
    ASSESSMENT_MAXIMUM_QUESTIONS = 10
    ASSESSMENT_ALLOW_ADAPTIVE_DIFFICULTY = True


def build_agent(llm=None, events=None):
    if llm is None:
        llm = AsyncMock()
        llm.generate.return_value = "[]"
    event_bus = MagicMock()
    publisher = AssessmentEventPublisher(event_bus)
    return AssessmentAgent(
        llm=llm,
        session_store=InMemoryQuizSessionStore(),
        profile_store=InMemoryAssessmentProfileStore(),
        event_publisher=publisher,
        settings=FakeSettings(),
    )


@pytest.mark.asyncio
async def test_suitability_learning_query():
    agent = build_agent()
    result = agent.evaluate_suitability("Explain how RAG works", intent_type="RAG_CHAT", domain="knowledge")
    assert result.suitable is True
    assert result.confidence >= 0.6
    assert "RAG" in result.topic


@pytest.mark.asyncio
async def test_suitability_greeting_blocked():
    agent = build_agent()
    result = agent.evaluate_suitability("hi", intent_type="GREETING", domain="general")
    assert result.suitable is False


@pytest.mark.asyncio
async def test_suitability_bugfix_blocked():
    agent = build_agent()
    result = agent.evaluate_suitability("fix this bug in my code", intent_type="GENERAL_CHAT", domain="general")
    assert result.suitable is False


@pytest.mark.asyncio
async def test_parse_json_with_fences():
    raw = '```json\n[{"type": "mcq", "text": "Q?", "options": ["A", "B"], "correct_answer": "A", "explanation": "E", "difficulty": "beginner", "topic": "RAG"}]\n```'
    parsed = parse_json(raw)
    assert isinstance(parsed, list)
    assert parsed[0]["text"] == "Q?"


@pytest.mark.asyncio
async def test_fallback_questions_cover_requested_count():
    questions = generate_questions("RAG", "beginner", 4, ["mcq", "true_false", "short_answer", "code"])
    assert len(questions) == 4
    assert questions[0].type == QuestionType.MCQ


@pytest.mark.asyncio
async def test_mcq_evaluation_option_letter():
    q = generate_questions("IAM", "beginner", 1, ["mcq"])[0]
    q.correct_answer = "Defending systems and responding to security incidents"
    q.options[0] = q.correct_answer
    correct, partial, _ = evaluate_fallback(q, "A")
    assert correct is True


@pytest.mark.asyncio
async def test_start_quiz_and_answer_flow():
    agent = build_agent()
    message = await agent.start_quiz("user1", "RAG", count=2, conversation="")
    assert message is not None
    assert "Question 1 of 2" in message

    session = agent.get_session("user1")
    assert session.is_active
    assert len(session.questions) == 2

    payload = await agent.answer("user1", "A")
    assert payload["kind"] == "next"
    assert "Question 2 of 2" in payload["message"]

    payload2 = await agent.answer("user1", "B")
    assert payload2["kind"] == "summary"
    assert "scored" in payload2["message"]
    assert "strengths" in payload2["message"].lower() or "Strengths" in payload2["message"]

    profile = agent._profiles.get_or_create("user1")
    assert profile.assessment_count == 1


@pytest.mark.asyncio
async def test_answer_after_completion_returns_none():
    agent = build_agent()
    await agent.start_quiz("user2", "RAG", count=1)
    await agent.answer("user2", "A")
    payload = await agent.answer("user2", "A")
    assert payload is None


@pytest.mark.asyncio
async def test_cancel_sets_abandoned():
    agent = build_agent()
    await agent.start_quiz("user3", "SIEM", count=2)
    message = await agent.cancel("user3")
    assert message
    session = agent.get_session("user3")
    assert session.status == QuizSessionStatus.ABANDONED


@pytest.mark.asyncio
async def test_confirmation_decline_detection():
    agent = build_agent()
    assert agent.is_confirmation("yes let's start") is True
    assert agent.is_decline("no thanks") is True
    assert agent.is_cancel("stop the quiz") is True
    assert agent.is_another_quiz("another quiz please") is True


@pytest.mark.asyncio
async def test_confirmation_is_word_boundary_aware():
    agent = build_agent()
    # "go" must not match the "go" inside "got" (e.g. after a lab completes).
    assert agent.is_confirmation("I got it now, report and delete") is False
    assert agent.is_confirmation("go ahead") is True
    assert agent.is_confirmation("yes please") is True
    assert agent.is_confirmation("yesterday I tried") is False


@pytest.mark.asyncio
async def test_adaptive_difficulty_bump():
    agent = build_agent()
    bumped = agent._adaptive_difficulty(DifficultyLevel.BEGINNER)
    assert bumped == DifficultyLevel.INTERMEDIATE


@pytest.mark.asyncio
async def test_llm_generation_used_when_available():
    llm = AsyncMock()
    llm.generate.return_value = (
        '[{"type": "mcq", "text": "What is RAG?", "options": ["A", "B", "C"], '
        '"correct_answer": "A", "explanation": "E", "difficulty": "beginner", "topic": "RAG"}]'
    )
    agent = build_agent(llm=llm)
    await agent.start_quiz("user4", "RAG", count=1)
    session = agent.get_session("user4")
    assert session.questions[0].text == "What is RAG?"
    assert llm.generate.await_count >= 1


@pytest.mark.asyncio
async def test_events_published_on_start():
    event_bus = MagicMock()
    publisher = AssessmentEventPublisher(event_bus)
    agent = AssessmentAgent(
        llm=AsyncMock(),
        session_store=InMemoryQuizSessionStore(),
        profile_store=InMemoryAssessmentProfileStore(),
        event_publisher=publisher,
        settings=FakeSettings(),
    )
    await agent.start_quiz("user5", "Python", count=1)
    assert event_bus.publish.call_count >= 1
