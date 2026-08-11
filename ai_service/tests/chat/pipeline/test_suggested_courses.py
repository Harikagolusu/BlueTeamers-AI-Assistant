"""Tests for the Suggested BlueTeamers Courses feature.

Covers:
- `suggested_courses` module: strong-match-only gating, top-3 relevance
  sorting, enrollment-aware CTAs, no raw lesson content exposure.
- `SuggestedCoursesStage`: attaches `suggested_courses` metadata to an
  ExecutionResult produced by the pipeline without touching engines.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock

from app.chat.context.execution_context import ExecutionContext
from app.chat.engines.suggested_courses import build_suggested_courses, _resolve_named_course_slug
from app.chat.pipeline.suggested_courses_stage import SuggestedCoursesStage
from app.models.chat.chat_models import ExecutionResult, ExecutionStatus


ENROLLED = {"blue-team-soc-fundamentals", "log-analysis-for-beginners", "siem-fundamentals"}


def _doc(course_slug: str, lesson_id: str, score: float = 0.8):
    return {
        "metadata": {
            "source": "lesson_content",
            "course_slug": course_slug,
            "lesson_id": lesson_id,
        },
        "score": score,
    }


class TestBuildSuggestedCourses:
    def test_empty_when_no_strong_match(self):
        assert build_suggested_courses("what is the capital of france", enrolled_slugs=ENROLLED) == []

    def test_empty_when_only_generic_docs(self):
        docs = [{"metadata": {"source": "web"}, "score": 0.9}]
        assert build_suggested_courses("tell me a story", documents=docs, enrolled_slugs=ENROLLED) == []

    def test_named_course_not_enrolled_offers_view_and_enroll(self):
        cards = build_suggested_courses(
            "generate study notes on incident response fundamentals",
            enrolled_slugs=ENROLLED,
        )
        assert cards, "a strong named-course match must produce suggestions"
        top = cards[0]
        assert top["course_slug"] == "incident-response-fundamentals"
        assert top["enrolled"] is False
        assert top["action"]["label"] == "Enroll Course"
        assert top["action"]["url"] == "/courses/incident-response-fundamentals/checkout"
        assert top["course_action"]["label"] == "View Course"
        assert top["course_action"]["url"] == "/courses/incident-response-fundamentals"
        assert top["enroll_url"] == "/courses/incident-response-fundamentals/checkout"
        assert top["level"] in {"Beginner", "Intermediate", "Advanced"}
        assert top["duration"]
        assert top["description"]

    def test_named_course_enrolled_uses_continue_course(self):
        cards = build_suggested_courses(
            "generate study notes on siem fundamentals",
            enrolled_slugs=ENROLLED,
        )
        assert cards
        top = cards[0]
        assert top["course_slug"] == "siem-fundamentals"
        assert top["enrolled"] is True
        assert top["action"]["label"] == "Continue Course"
        assert top["action"]["url"] == "/courses/siem-fundamentals"

    def test_enrolled_with_progress_continues_to_lesson(self):
        cards = build_suggested_courses(
            "generate study notes on siem fundamentals",
            enrolled_slugs=ENROLLED,
            progress_by_slug={"siem-fundamentals": 45},
        )
        top = next(c for c in cards if c["course_slug"] == "siem-fundamentals")
        assert top["action"]["label"] == "Continue Course"
        assert top["lesson_url"] and top["lesson_url"].startswith("/courses/siem-fundamentals/lesson/")
        assert top["action"]["url"] == top["lesson_url"]

    def test_top_three_sorted_by_relevance(self):
        cards = build_suggested_courses(
            "incident response playbooks and network monitoring for beginners",
            enrolled_slugs=ENROLLED,
        )
        assert len(cards) <= 3
        ranks = [c["rank"] for c in cards]
        scores = [c["score"] for c in cards]
        assert ranks == sorted(ranks)
        assert scores == sorted(scores, reverse=True)

    def test_no_padding_to_three_for_single_strong_match(self):
        # A focused query about one course must not get unrelated cards padded
        # in just to fill the top-3 slot.
        cards = build_suggested_courses(
            "generate study notes on SIEM fundamentals",
            enrolled_slugs=ENROLLED,
        )
        assert len(cards) == 1
        assert cards[0]["course_slug"] == "siem-fundamentals"

    def test_no_raw_lesson_content_exposed(self):
        docs = [_doc("incident-response-fundamentals", "ir-1", 0.9)]
        cards = build_suggested_courses(
            "generate study notes on incident response fundamentals",
            documents=docs,
            enrolled_slugs=ENROLLED,
        )
        serialized = repr(cards).lower()
        assert "lesson_id" not in serialized
        assert all("lessons" not in c for c in cards)
        assert all(c["description"] for c in cards)

    def test_catalog_slug_resolution(self):
        assert _resolve_named_course_slug("malware analysis fundamentals") == "malware-analysis-fundamentals"
        assert _resolve_named_course_slug("what does a firewall do") is None

    def test_progress_attached_when_available(self):
        cards = build_suggested_courses(
            "generate study notes on siem fundamentals",
            enrolled_slugs=ENROLLED,
            progress_by_slug={"siem-fundamentals": 45},
        )
        top = next(c for c in cards if c["course_slug"] == "siem-fundamentals")
        assert top["progress"] == 45


class TestSuggestedCoursesStage:
    async def _make_context(self, query: str, result: ExecutionResult, token: str = "t"):
        return ExecutionContext(metadata={"query": query, "token": token, "execution_result": result})

    def _make_repo(self):
        repo = MagicMock()
        repo.get_enrolled_courses = AsyncMock(return_value=[
            MagicMock(id="blue-team-soc-fundamentals"),
            MagicMock(id="siem-fundamentals"),
        ])
        repo.get_progress = AsyncMock(return_value=MagicMock(percent_complete=50))
        return repo

    @pytest.mark.asyncio
    async def test_attaches_suggested_courses(self):
        result = ExecutionResult.success(
            "RAG",
            "Here is an answer grounded in lessons.",
            documents=[_doc("incident-response-fundamentals", "ir-1")],
        )
        context = await self._make_context(
            "generate study notes on incident response fundamentals", result
        )
        stage = SuggestedCoursesStage(self._make_repo())
        new_ctx = await stage.execute(context)

        new_result = new_ctx.metadata["execution_result"]
        suggested = new_result.metadata.get("suggested_courses", [])
        assert suggested, "a grounded lesson query must yield suggestions"
        assert suggested[0]["course_slug"] == "incident-response-fundamentals"
        assert suggested[0]["action"]["label"] == "Enroll Course"
        assert suggested[0]["enrolled"] is False

    @pytest.mark.asyncio
    async def test_no_suggestions_for_unrelated_query(self):
        result = ExecutionResult.success("GENERAL", "Just a chat response.")
        context = await self._make_context("what is the capital of france", result)
        stage = SuggestedCoursesStage(self._make_repo())
        new_ctx = await stage.execute(context)
        assert new_ctx.metadata["execution_result"].metadata.get("suggested_courses", []) == []

    @pytest.mark.asyncio
    async def test_enrollment_drives_continue_course(self):
        result = ExecutionResult.success("RAG", "SIEM answer.", documents=[_doc("siem-fundamentals", "s-1")])
        context = await self._make_context("generate study notes on siem fundamentals", result)
        stage = SuggestedCoursesStage(self._make_repo())
        new_ctx = await stage.execute(context)
        suggested = new_ctx.metadata["execution_result"].metadata["suggested_courses"]
        top = next(c for c in suggested if c["course_slug"] == "siem-fundamentals")
        assert top["enrolled"] is True
        assert top["action"]["label"] == "Continue Course"

    @pytest.mark.asyncio
    async def test_missing_execution_result_is_noop(self):
        context = ExecutionContext(metadata={"query": "hello"})
        stage = SuggestedCoursesStage(self._make_repo())
        new_ctx = await stage.execute(context)
        assert "suggested_courses" not in new_ctx.metadata

    @pytest.mark.asyncio
    async def test_tokenless_guest_uses_catalog_only(self):
        result = ExecutionResult.success("RAG", "answer", documents=[_doc("threat-hunting-fundamentals", "t-1")])
        context = await self._make_context("threat hunting basics", result, token=None)
        repo = self._make_repo()
        stage = SuggestedCoursesStage(repo)
        new_ctx = await stage.execute(context)
        suggested = new_ctx.metadata["execution_result"].metadata.get("suggested_courses", [])
        assert suggested
        repo.get_enrolled_courses.assert_not_awaited()
