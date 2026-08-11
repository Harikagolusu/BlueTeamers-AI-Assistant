import pytest
from unittest.mock import AsyncMock

from app.agents.assessment.agent import AssessmentAgent
from app.agents.assessment.events import AssessmentEventPublisher
from app.agents.assessment.models import QuizSession, QuizSessionStatus
from app.agents.assessment.profile_store import InMemoryAssessmentProfileStore
from app.agents.assessment.session_store import InMemoryQuizSessionStore
from app.chat.context.execution_context import ExecutionContext
from app.chat.pipeline.assessment_stage import AssessmentStage, _with_suffix
from app.models.chat.chat_models import ExecutionResult


class FakeSettings:
    # These stage-mechanics tests run in "legacy" mode (enrollment not required)
    # so they stay focused on the offer/quiz flow. The course-aware enrollment
    # gate is covered separately by tests/agents/assessment/test_course_context.py
    # and tests/chat/test_assessment_stage_course.py.
    ASSESSMENT_REQUIRE_ENROLLMENT = False
    ENABLE_ASSESSMENT_AGENT = True
    ASSESSMENT_MINIMUM_CONFIDENCE_THRESHOLD = 0.6
    ASSESSMENT_DEFAULT_QUIZ_LENGTH = 2
    ASSESSMENT_DEFAULT_DIFFICULTY = "beginner"
    ASSESSMENT_MAXIMUM_QUESTIONS = 10
    ASSESSMENT_ALLOW_ADAPTIVE_DIFFICULTY = True


def make_agent():
    llm = AsyncMock()
    llm.generate.return_value = "[]"
    return AssessmentAgent(
        llm=llm,
        session_store=InMemoryQuizSessionStore(),
        profile_store=InMemoryAssessmentProfileStore(),
        event_publisher=AssessmentEventPublisher(None),
        settings=FakeSettings(),
    )


def make_stage():
    return AssessmentStage(make_agent(), settings=FakeSettings())


def make_context(query, session_user="user-1", streaming=False, intent="RAG_CHAT",
                 domain="knowledge", selected_engine="RAG", generator=None):
    result = ExecutionResult.success(
        engine="RAG",
        message="RAG stands for Retrieval-Augmented Generation.",
    )
    if generator is not None:
        result = result.model_copy(update={"metadata": {"generator": generator}})
    return ExecutionContext(
        session_user=session_user,
        metadata={
            "query": query,
            "intent": intent,
            "domain": domain,
            "selected_engine": selected_engine,
            "execution_result": result,
        },
        streaming_mode=streaming,
    )


@pytest.mark.asyncio
async def test_offer_appended_for_learning_query():
    stage = make_stage()
    context = make_context("Explain how RAG works")
    out = await stage.execute(context)
    result = out.metadata["execution_result"]
    assert "Would you like to test your understanding" in result.message
    pending = stage._agent._sessions.get("user-1")
    assert pending is not None
    assert pending.status == QuizSessionStatus.PENDING_CONFIRM


@pytest.mark.asyncio
async def test_no_offer_for_greeting():
    stage = make_stage()
    context = make_context("hi there", intent="GREETING", domain="general")
    out = await stage.execute(context)
    result = out.metadata["execution_result"]
    assert "Would you like" not in result.message
    assert stage._agent._sessions.get("user-1") is None


@pytest.mark.asyncio
async def test_no_offer_for_assessment_engine():
    stage = make_stage()
    context = make_context("explain RAG", selected_engine="ASSESSMENT_COACH")
    out = await stage.execute(context)
    assert out.metadata["execution_result"].message == "RAG stands for Retrieval-Augmented Generation."


@pytest.mark.asyncio
async def test_confirmation_starts_quiz():
    stage = make_stage()
    agent = stage._agent
    agent._sessions.put(QuizSession(
        session_key="user-1", topic="RAG", status=QuizSessionStatus.PENDING_CONFIRM
    ))
    context = make_context("yes let's start")
    out = await stage.execute(context)
    result = out.metadata["execution_result"]
    assert "Question 1 of 2" in result.message
    assert agent._sessions.get("user-1").status == QuizSessionStatus.ACTIVE


@pytest.mark.asyncio
async def test_decline_keeps_normal_response():
    stage = make_stage()
    agent = stage._agent
    agent._sessions.put(QuizSession(
        session_key="user-1", topic="RAG", status=QuizSessionStatus.PENDING_CONFIRM
    ))
    context = make_context("no thanks")
    out = await stage.execute(context)
    result = out.metadata["execution_result"]
    assert result.message == "RAG stands for Retrieval-Augmented Generation."
    assert agent._sessions.get("user-1") is None


@pytest.mark.asyncio
async def test_active_quiz_answers_turn():
    stage = make_stage()
    agent = stage._agent
    questions = await agent._generate_questions("RAG", "beginner", 2, [], "")
    agent._sessions.put(QuizSession(
        session_key="user-1",
        topic="RAG",
        status=QuizSessionStatus.ACTIVE,
        questions=questions,
        length=len(questions),
    ))
    context = make_context("A")
    out = await stage.execute(context)
    result = out.metadata["execution_result"]
    assert "Question 2 of 2" in result.message


@pytest.mark.asyncio
async def test_cancel_active_quiz():
    stage = make_stage()
    agent = stage._agent
    questions = await agent._generate_questions("RAG", "beginner", 2, [], "")
    agent._sessions.put(QuizSession(
        session_key="user-1",
        topic="RAG",
        status=QuizSessionStatus.ACTIVE,
        questions=questions,
        length=len(questions),
    ))
    context = make_context("stop")
    out = await stage.execute(context)
    result = out.metadata["execution_result"]
    assert "stopped the quiz" in result.message
    assert agent._sessions.get("user-1").status == QuizSessionStatus.ABANDONED


@pytest.mark.asyncio
async def test_streaming_offer_keeps_generator_and_attaches_meta():
    async def fake_gen():
        yield "RAG "
        yield "explained"

    stage = make_stage()
    context = make_context("explain RAG", streaming=True, generator=fake_gen())
    out = await stage.execute(context)
    result = out.metadata["execution_result"]
    wrapped = result.metadata.get("generator")
    assert wrapped is not None
    tokens = []
    async for token in wrapped:
        tokens.append(token)
    assert "".join(tokens) == "RAG explained"
    assert result.metadata["assessment"]["mode"] == "offered"


@pytest.mark.asyncio
async def test_with_suffix_yields_suffix_after_tokens():
    async def fake_gen():
        yield "a"
        yield "b"

    collected = []
    async for token in _with_suffix(fake_gen(), "SUFFIX"):
        collected.append(token)
    assert collected == ["a", "b", "SUFFIX"]
