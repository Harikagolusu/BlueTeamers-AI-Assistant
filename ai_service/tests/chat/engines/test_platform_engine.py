import pytest
from unittest.mock import AsyncMock, MagicMock
from app.chat.engines.platform_engine import PlatformExecutionEngine
from app.chat.context.execution_context import ExecutionContext
from app.chat.intent.models.intent_types import IntentType
from app.platform.models import Course, Progress, Certificate

def _build_engine(mock_repo=None, mock_retriever=None):
    repo = mock_repo or AsyncMock()
    user_ctx = AsyncMock()
    user_ctx.build.return_value = "### User Platform Context ###\nName: Test"
    rec_service = AsyncMock()
    rec_service.generate_recommendations.return_value = []
    rec_service.generate_for_domain.return_value = []
    llm = AsyncMock()
    llm.generate.return_value = "Platform Response"
    prompt_builder = MagicMock()
    prompt_builder.build_prompt.return_value = ("query", "System prompt")
    retriever = mock_retriever or AsyncMock()
    retriever.search.return_value = []
    return PlatformExecutionEngine(repo, user_ctx, rec_service, retriever, llm, prompt_builder)

def _ctx(query, intent):
    from app.chat.intent.models.analysis_result import IntentAnalysisResult
    analysis = MagicMock()
    analysis.primary_intent.type = intent
    return ExecutionContext(metadata={
        "query": query,
        "token": "jwt-token",
        "intent_analysis": analysis,
    })

@pytest.mark.asyncio
async def test_platform_engine_enrolled_courses_non_streaming():
    repo = AsyncMock()
    repo.get_enrolled_courses.return_value = [
        Course(id="siem-fundamentals", title="SIEM Fundamentals", description="d", level="medium", duration_hours=6)
    ]
    engine = _build_engine(mock_repo=repo)
    ctx = _ctx("What courses do I have?", IntentType.PLATFORM_COURSE)

    result = await engine.execute(ctx)

    assert result.status == "SUCCESS"
    # Pure platform intents are answered deterministically WITHOUT the LLM.
    assert "SIEM Fundamentals" in result.message
    assert result.metadata["llm_used"] is False
    engine._llm.generate.assert_not_awaited()
    repo.get_enrolled_courses.assert_awaited_once_with("jwt-token")
    cards = result.metadata["platform"]["cards"]
    assert cards[0]["title"] == "SIEM Fundamentals"
    assert cards[0]["type"] == "course"
    assert result.metadata["platform_cards"][0]["title"] == "SIEM Fundamentals"

@pytest.mark.asyncio
async def test_platform_engine_progress_dispatch():
    repo = AsyncMock()
    repo.get_enrolled_courses.return_value = [
        Course(id="siem-fundamentals", title="SIEM Fundamentals", description="d", level="medium", duration_hours=6)
    ]
    repo.get_progress.return_value = Progress(course_slug="siem-fundamentals", percent_complete=50, completed_lessons=["1.1"])
    engine = _build_engine(mock_repo=repo)
    ctx = _ctx("What is my progress?", IntentType.PLATFORM_PROGRESS)

    result = await engine.execute(ctx)

    assert result.status == "SUCCESS"
    repo.get_progress.assert_awaited_once()
    assert "progress" in result.metadata["platform"]["context_used"]
    assert result.metadata["llm_used"] is False

@pytest.mark.asyncio
async def test_platform_engine_recommendation_is_llm_grounded():
    repo = AsyncMock()
    repo.get_enrolled_courses.return_value = []
    engine = _build_engine(mock_repo=repo)
    # Recommendation phrasing -> content-grounded recommendation answer: the
    # engine retrieves BlueTeamers lessons and uses the LLM to explain the
    # "why" (the answer must reference real lessons, not a flat list).
    ctx = _ctx("suggest a course", IntentType.PLATFORM_COURSE)

    result = await engine.execute(ctx)

    assert result.status == "SUCCESS"
    assert result.metadata["llm_used"] is True
    engine._llm.generate.assert_awaited_once()
    engine._recommendation_service.generate_for_domain.assert_awaited_once()
    engine._retriever.search.assert_awaited_once()
    assert result.metadata["recommendation_used"] is False  # no recs returned by mock

@pytest.mark.asyncio
async def test_platform_engine_unavailable_apologizes_without_inventing():
    repo = AsyncMock()
    repo.get_enrolled_courses.side_effect = Exception("Django down")
    engine = _build_engine(mock_repo=repo)
    ctx = _ctx("What courses do I have?", IntentType.PLATFORM_COURSE)

    result = await engine.execute(ctx)

    assert result.status == "SUCCESS"
    assert result.metadata["platform"]["cards"] == []


def _page_course_context(query):
    from app.chat.intent.models.analysis_result import IntentAnalysisResult
    analysis = MagicMock()
    analysis.primary_intent.type = IntentType.PLATFORM_COURSE
    return ExecutionContext(metadata={
        "query": query,
        "token": "jwt-token",
        "intent_analysis": analysis,
        "context": {
            "page": {
                "type": "course",
                "path": "/courses/blue-team-soc-fundamentals",
                "course": "blue-team-soc-fundamentals",
                "course_title": "Blue Team & SOC Fundamentals",
            }
        },
    })


@pytest.mark.asyncio
async def test_platform_engine_page_reference_explains_current_course():
    """'explain about this course' while on a course page must describe THAT
    course from the catalog, never the generic enrolled-courses list."""
    repo = AsyncMock()
    repo.get_enrolled_courses.return_value = [
        Course(slug="blue-team-soc-fundamentals", title="Blue Team & SOC Fundamentals", description="d", level="easy", duration_hours=12)
    ]
    repo.get_progress.return_value = Progress(course_slug="blue-team-soc-fundamentals", percent_complete=25, completed_lessons=["1.1"])
    engine = _build_engine(mock_repo=repo)
    ctx = _page_course_context("explain about this course")

    result = await engine.execute(ctx)

    assert result.status == "SUCCESS"
    assert "Blue Team & SOC Fundamentals" in result.message
    assert "25% complete" in result.message
    assert "What you'll learn" in result.message
    assert result.metadata["llm_used"] is False
    # The enrolled-courses greeting must not leak as the primary answer.
    assert "Your enrolled courses" not in result.message
    assert result.metadata["course_info"]["course_slug"] == "blue-team-soc-fundamentals"


@pytest.mark.asyncio
async def test_platform_engine_page_reference_without_page_context_falls_through():
    """A 'this course' reference with NO page context keeps the normal path."""
    repo = AsyncMock()
    repo.get_enrolled_courses.return_value = [
        Course(id="siem-fundamentals", title="SIEM Fundamentals", description="d", level="medium", duration_hours=6)
    ]
    engine = _build_engine(mock_repo=repo)
    ctx = _ctx("explain about this course", IntentType.PLATFORM_COURSE)

    result = await engine.execute(ctx)

    assert result.status == "SUCCESS"
    assert result.metadata["llm_used"] is False
    assert "SIEM Fundamentals" in result.message
