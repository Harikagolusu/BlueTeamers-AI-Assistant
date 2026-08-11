"""Tests for the Course-Aware Assessment Agent gating & progress tracking."""
import pytest
from unittest.mock import AsyncMock, MagicMock

from app.agents.assessment.agent import AssessmentAgent
from app.agents.assessment.course_context import (
    CourseContextService,
    CourseOfferAction,
)
from app.agents.assessment.events import AssessmentEventPublisher
from app.agents.assessment.models import DifficultyLevel, QuizResult
from app.agents.assessment.profile_store import InMemoryAssessmentProfileStore
from app.agents.assessment.session_store import InMemoryQuizSessionStore
from app.platform.models import Course


class FakeSettings:
    ENABLE_ASSESSMENT_AGENT = True
    ASSESSMENT_MINIMUM_CONFIDENCE_THRESHOLD = 0.6
    ASSESSMENT_DEFAULT_QUIZ_LENGTH = 3
    ASSESSMENT_DEFAULT_DIFFICULTY = "beginner"
    ASSESSMENT_MAXIMUM_QUESTIONS = 10
    ASSESSMENT_ALLOW_ADAPTIVE_DIFFICULTY = True
    ASSESSMENT_REQUIRE_ENROLLMENT = True
    ASSESSMENT_RECENT_WINDOW_SECONDS = 604800
    ASSESSMENT_COURSE_RECOMMENDATION_COUNT = 3


class LegacySettings(FakeSettings):
    ASSESSMENT_REQUIRE_ENROLLMENT = False


def make_course(slug: str, title: str) -> Course:
    # Course.id is declared with alias="slug"; pydantic v2 validates by alias
    # unless populate_by_name is set, so we must pass slug=.
    return Course(slug=slug, title=title, description="", level="beginner", duration_hours=1)


class FakeRepo:
    def __init__(self, enrolled=None):
        self._enrolled = list(enrolled or [])

    async def get_enrolled_courses(self, token):
        return self._enrolled


def build_agent(enrolled=None, settings=None, profile_store=None, course_context=None):
    if course_context is None:
        course_context = CourseContextService(FakeRepo(enrolled=enrolled))
    return AssessmentAgent(
        llm=AsyncMock(),
        session_store=InMemoryQuizSessionStore(),
        profile_store=profile_store or InMemoryAssessmentProfileStore(),
        event_publisher=AssessmentEventPublisher(MagicMock()),
        settings=settings or FakeSettings(),
        course_context=course_context,
    )


# ------------------------------------------------------------------ matcher

@pytest.mark.asyncio
async def test_match_course_by_topic():
    svc = CourseContextService(FakeRepo())
    courses = [
        make_course("siem-fundamentals", "SIEM Fundamentals"),
        make_course("network-fundamentals", "Network Fundamentals"),
    ]
    matched = svc.match_course("Explain how SIEM correlation rules work", courses)
    assert matched is not None and matched.id == "siem-fundamentals"


@pytest.mark.asyncio
async def test_match_course_no_topic_returns_none():
    svc = CourseContextService(FakeRepo())
    courses = [make_course("siem-fundamentals", "SIEM Fundamentals")]
    assert svc.match_course("How do I bake a cake", courses) is None

# ------------------------------------------------------------------ resolve_offer

@pytest.mark.asyncio
async def test_enrolled_matching_course_offers_quiz():
    agent = build_agent(enrolled=[make_course("siem-fundamentals", "SIEM Fundamentals")])
    d = await agent.resolve_offer("Explain SIEM correlation", session_user="u1",
                                  token="tok", intent_type="RAG_CHAT", domain="knowledge")
    assert d.action == CourseOfferAction.OFFER_QUIZ.value
    assert d.course_slug == "siem-fundamentals"


@pytest.mark.asyncio
async def test_not_enrolled_recommends_course():
    agent = build_agent(enrolled=[])
    d = await agent.resolve_offer("What is SIEM?", session_user="u2",
                                  token="tok", intent_type="RAG_CHAT", domain="knowledge")
    assert d.action == CourseOfferAction.RECOMMEND_COURSE.value
    assert d.course is None


@pytest.mark.asyncio
async def test_no_token_recommends_course():
    agent = build_agent(enrolled=[make_course("siem-fundamentals", "SIEM Fundamentals")])
    d = await agent.resolve_offer("Explain SIEM", session_user="u3", token=None,
                                  intent_type="RAG_CHAT", domain="knowledge")
    assert d.action == CourseOfferAction.RECOMMEND_COURSE.value


@pytest.mark.asyncio
async def test_enrolled_topic_mismatch_recommends():
    agent = build_agent(enrolled=[make_course("siem-fundamentals", "SIEM Fundamentals")])
    d = await agent.resolve_offer("Explain how to cook pasta", session_user="u4",
                                  token="tok", intent_type="RAG_CHAT", domain="knowledge")
    assert d.action == CourseOfferAction.RECOMMEND_COURSE.value


@pytest.mark.asyncio
async def test_recently_assessed_blocks_repeat():
    store = InMemoryAssessmentProfileStore()
    agent = build_agent(
        enrolled=[make_course("siem-fundamentals", "SIEM Fundamentals")],
        profile_store=store,
    )
    store.record_result(
        "u5",
        QuizResult(score=5, total=5, passed=True, difficulty_reached=DifficultyLevel.BEGINNER),
        "siem",
        course_slug="siem-fundamentals",
    )
    d = await agent.resolve_offer("Explain SIEM", session_user="u5",
                                  token="tok", intent_type="RAG_CHAT", domain="knowledge")
    assert d.action == CourseOfferAction.RECENTLY_ASSESSED.value


@pytest.mark.asyncio
async def test_legacy_mode_offers_without_enrollment():
    agent = build_agent(enrolled=[], settings=LegacySettings())
    d = await agent.resolve_offer("Explain SIEM", session_user="u6", token=None,
                                  intent_type="RAG_CHAT", domain="knowledge")
    assert d.action == CourseOfferAction.OFFER_QUIZ.value


@pytest.mark.asyncio
async def test_greeting_never_offers():
    agent = build_agent(enrolled=[make_course("siem-fundamentals", "SIEM Fundamentals")])
    d = await agent.resolve_offer("hi there", session_user="u7", token="tok",
                                  intent_type="GREETING", domain="general")
    assert d.action == CourseOfferAction.OFF.value


# ------------------------------------------------------------------ messages

def test_offer_message_is_course_aware():
    assert "SIEM Fundamentals" in AssessmentAgent.offer_message("SIEM Fundamentals")
    assert "quiz" in AssessmentAgent.offer_message().lower()


def test_course_recommendation_message_never_asks_quiz():
    msg = AssessmentAgent.course_recommendation_message()
    # It must NOT include the quiz offer phrasing.
    assert "Would you like to test your understanding" not in msg
    assert "enrolled" in msg.lower()


# ------------------------------------------------------------------ progress

def test_profile_tracks_course_progress():
    store = InMemoryAssessmentProfileStore()
    store.record_result(
        "u8",
        QuizResult(score=4, total=5, passed=True, strengths=["correlation"],
                   weak_areas=["parsing"], difficulty_reached=DifficultyLevel.BEGINNER),
        "siem",
        course_slug="siem-fundamentals",
    )
    profile = store.get_or_create("u8")
    entry = profile.course_progress["siem-fundamentals"]
    assert entry["assessments_completed"] == 1
    assert "siem-fundamentals:parsing" in profile.revision_topics
    assert profile.completion_percentage == 0.0  # needs 2 passed assessments to count


def test_profile_completion_percentage():
    store = InMemoryAssessmentProfileStore()
    result = QuizResult(score=5, total=5, passed=True, difficulty_reached=DifficultyLevel.BEGINNER)
    store.record_result("u9", result, "siem", course_slug="course-a")
    store.record_result("u9", result, "siem", course_slug="course-a")
    store.record_result("u9", result, "network", course_slug="course-b")
    profile = store.get_or_create("u9")
    # course-a got 2 passes -> complete; course-b has 1 -> not complete.
    assert profile.course_progress["course-a"]["complete"] is True
    assert profile.course_progress["course-b"]["complete"] is False
    assert profile.completion_percentage == 50.0


