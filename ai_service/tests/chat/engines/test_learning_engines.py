import pytest
from unittest.mock import AsyncMock, MagicMock

from app.chat.engines.learning_engines import (
    NotesGenerationEngine,
    TopicSummaryEngine,
    CourseFirstAgentEngine,
)
from app.chat.context.execution_context import ExecutionContext
from app.rag.interfaces import Document


def _doc(content, course_slug=None, lesson_title=None, source="lesson_content", lesson_id="1.1"):
    return Document(
        content=content,
        metadata={
            "course_slug": course_slug,
            "course_title": course_slug,
            "lesson_title": lesson_title,
            "lesson_id": lesson_id,
            "source": source,
        },
        score=0.8,
    )


class TestNotesGenerationEngine:
    @pytest.mark.asyncio
    async def test_uses_course_first_retrieval_and_notes_persona(self):
        mock_llm = AsyncMock()
        mock_llm.generate.return_value = "# SIEM Notes\n## Overview\n..."
        mock_prompt_builder = MagicMock()
        mock_prompt_builder.build_prompt.return_value = ("P", "S")

        mock_retriever = AsyncMock()
        mock_retriever.search.return_value = [_doc("siem lesson", course_slug="siem-fundamentals", lesson_title="SIEM")]

        mock_repo = AsyncMock()
        mock_repo.get_enrolled_courses.return_value = [MagicMock(id="siem-fundamentals")]

        engine = NotesGenerationEngine(mock_retriever, mock_llm, mock_prompt_builder, platform_repo=mock_repo)
        ctx = ExecutionContext(metadata={"query": "Generate study notes on SIEM", "token": "tok"})

        result = await engine.execute(ctx)

        assert result.status == "SUCCESS"
        assert result.metadata["engine"] == "NOTES_GENERATOR"
        assert result.metadata["agent"] == "notes_generator"
        assert result.metadata["answer_source"] == "course"
        filters = mock_retriever.search.call_args.kwargs.get("metadata_filters")
        assert filters["source"] == "lesson_content"
        assert filters["course_slug"] == ["siem-fundamentals"]

        _, prompt_context = mock_prompt_builder.build_prompt.call_args.args
        assert "notes" in prompt_context["agent_persona"].lower()
        assert prompt_context["answer_source"] == "course"

    @pytest.mark.asyncio
    async def test_notes_falls_back_to_general_knowledge(self):
        mock_llm = AsyncMock()
        mock_llm.generate.return_value = "# Notes"
        mock_prompt_builder = MagicMock()
        mock_prompt_builder.build_prompt.return_value = ("P", "S")

        mock_retriever = AsyncMock()
        mock_retriever.search.side_effect = [[], [_doc("general", source="document")]]

        mock_repo = AsyncMock()
        mock_repo.get_enrolled_courses.return_value = [MagicMock(id="soc-201")]

        engine = NotesGenerationEngine(mock_retriever, mock_llm, mock_prompt_builder, platform_repo=mock_repo)
        ctx = ExecutionContext(metadata={"query": "Generate notes on phishing", "token": "tok"})

        result = await engine.execute(ctx)

        assert result.status == "SUCCESS"
        assert result.metadata["answer_source"] == "general"
        assert mock_retriever.search.call_count == 2

    @pytest.mark.asyncio
    async def test_notes_streaming_mode(self):
        mock_llm = AsyncMock()
        mock_prompt_builder = MagicMock()
        mock_prompt_builder.build_prompt.return_value = ("P", "S")

        mock_retriever = AsyncMock()
        mock_retriever.search.return_value = [_doc("lesson", course_slug="soc-201", lesson_title="SIEM")]
        engine = NotesGenerationEngine(mock_retriever, mock_llm, mock_prompt_builder, platform_repo=None)
        ctx = ExecutionContext(metadata={"query": "Generate notes on SIEM"}, streaming_mode=True)

        result = await engine.execute(ctx)

        assert result.status == "SUCCESS"
        assert "generator" in result.metadata


class TestTopicSummaryEngine:
    @pytest.mark.asyncio
    async def test_summarizer_persona_and_retrieval(self):
        mock_llm = AsyncMock()
        mock_llm.generate.return_value = "## Overview\n..."
        mock_prompt_builder = MagicMock()
        mock_prompt_builder.build_prompt.return_value = ("P", "S")

        mock_retriever = AsyncMock()
        mock_retriever.search.return_value = [_doc("phishing lesson", course_slug="soc-101", lesson_title="Phishing")]

        mock_repo = AsyncMock()
        mock_repo.get_enrolled_courses.return_value = [MagicMock(id="soc-101")]

        engine = TopicSummaryEngine(mock_retriever, mock_llm, mock_prompt_builder, platform_repo=mock_repo)
        ctx = ExecutionContext(metadata={"query": "Summarize phishing", "token": "tok"})

        result = await engine.execute(ctx)

        assert result.status == "SUCCESS"
        assert result.metadata["engine"] == "TOPIC_SUMMARIZER"
        assert result.metadata["answer_source"] == "course"
        assert result.metadata.get("content_gated") is not True

        _, prompt_context = mock_prompt_builder.build_prompt.call_args.args
        assert "summary" in prompt_context["agent_persona"].lower()

    @pytest.mark.asyncio
    async def test_summarizer_no_enrollment(self):
        mock_llm = AsyncMock()
        mock_llm.generate.return_value = "## Key Points"
        mock_prompt_builder = MagicMock()
        mock_prompt_builder.build_prompt.return_value = ("P", "S")

        mock_retriever = AsyncMock()
        mock_retriever.search.return_value = [_doc("general", source="document")]

        engine = TopicSummaryEngine(mock_retriever, mock_llm, mock_prompt_builder, platform_repo=None)
        ctx = ExecutionContext(metadata={"query": "Summarize zero trust"})

        result = await engine.execute(ctx)

        assert result.status == "SUCCESS"
        assert result.metadata["answer_source"] == "general"
        assert result.metadata.get("content_gated") is not True
        mock_retriever.search.assert_awaited_once()


class TestCourseAccessGate:
    """Course-aware content gate: full content only for enrolled learners."""

    @pytest.mark.asyncio
    async def test_notes_gated_when_course_not_enrolled(self):
        mock_llm = AsyncMock()
        mock_llm.generate.return_value = "## Overview\nSIEM is...\n## Why It Matters"
        mock_prompt_builder = MagicMock()
        mock_prompt_builder.build_prompt.return_value = ("P", "S")

        mock_retriever = AsyncMock()
        mock_retriever.search.return_value = [_doc("siem lesson", course_slug="siem-fundamentals", lesson_title="SIEM")]

        mock_repo = AsyncMock()
        mock_repo.get_enrolled_courses.return_value = [MagicMock(id="soc-201")]

        engine = NotesGenerationEngine(mock_retriever, mock_llm, mock_prompt_builder, platform_repo=mock_repo)
        ctx = ExecutionContext(metadata={"query": "Generate notes on SIEM", "token": "tok"})

        result = await engine.execute(ctx)

        assert result.status == "SUCCESS"
        assert result.metadata["content_gated"] is True
        assert result.metadata["gated_course_slug"] == "siem-fundamentals"
        assert result.metadata["recommendation_used"] is True
        assert result.metadata["answer_source"] == "gated"

        # The LLM must never receive the not-enrolled course's lesson content.
        _, prompt_context = mock_prompt_builder.build_prompt.call_args.args
        assert not prompt_context.get("retrieved_documents")
        assert "Overview" in prompt_context["agent_persona"]

        # A course recommendation card is emitted (reuses the existing UI).
        cards = result.metadata.get("course_sources", [])
        assert len(cards) == 1
        card = cards[0]
        assert card["course_slug"] == "siem-fundamentals"
        assert card["action"]["label"] == "View Course"
        assert card["action"]["url"] == "/courses/siem-fundamentals"
        assert card["course_action"]["url"] == "/courses/siem-fundamentals"
        assert card.get("level")
        assert card.get("duration")
        assert card.get("description")

    @pytest.mark.asyncio
    async def test_summary_gated_when_course_not_enrolled(self):
        mock_llm = AsyncMock()
        mock_llm.generate.return_value = "## Overview\nshort..."
        mock_prompt_builder = MagicMock()
        mock_prompt_builder.build_prompt.return_value = ("P", "S")

        mock_retriever = AsyncMock()
        mock_retriever.search.return_value = [_doc("ir lesson", course_slug="incident-response-fundamentals", lesson_title="IR")]

        mock_repo = AsyncMock()
        mock_repo.get_enrolled_courses.return_value = []

        engine = TopicSummaryEngine(mock_retriever, mock_llm, mock_prompt_builder, platform_repo=mock_repo)
        ctx = ExecutionContext(metadata={"query": "Summarize incident response", "token": "tok"})

        result = await engine.execute(ctx)

        assert result.status == "SUCCESS"
        assert result.metadata["content_gated"] is True
        assert result.metadata["gated_course_slug"] == "incident-response-fundamentals"
        assert len(result.metadata["course_sources"]) == 1

    @pytest.mark.asyncio
    async def test_not_gated_when_enrolled_in_course(self):
        mock_llm = AsyncMock()
        mock_llm.generate.return_value = "# SIEM Notes\n## Overview\n..."
        mock_prompt_builder = MagicMock()
        mock_prompt_builder.build_prompt.return_value = ("P", "S")

        mock_retriever = AsyncMock()
        mock_retriever.search.return_value = [_doc("siem lesson", course_slug="siem-fundamentals", lesson_title="SIEM")]

        mock_repo = AsyncMock()
        mock_repo.get_enrolled_courses.return_value = [MagicMock(id="siem-fundamentals")]

        engine = NotesGenerationEngine(mock_retriever, mock_llm, mock_prompt_builder, platform_repo=mock_repo)
        ctx = ExecutionContext(metadata={"query": "Generate notes on SIEM", "token": "tok"})

        result = await engine.execute(ctx)

        assert result.status == "SUCCESS"
        assert result.metadata.get("content_gated") is not True
        assert result.metadata["answer_source"] == "course"
        assert result.metadata["course_sources"]  # Continue Learning cards still shown

    @pytest.mark.asyncio
    async def test_gate_skipped_when_no_course_content_matched(self):
        # General knowledge query: not tied to any BlueTeamers course.
        mock_llm = AsyncMock()
        mock_llm.generate.return_value = "# Notes\n## Overview"
        mock_prompt_builder = MagicMock()
        mock_prompt_builder.build_prompt.return_value = ("P", "S")

        mock_retriever = AsyncMock()
        mock_retriever.search.return_value = [_doc("general knowledge", source="document")]

        mock_repo = AsyncMock()
        mock_repo.get_enrolled_courses.return_value = []

        engine = NotesGenerationEngine(mock_retriever, mock_llm, mock_prompt_builder, platform_repo=mock_repo)
        ctx = ExecutionContext(metadata={"query": "Generate notes on python programming", "token": "tok"})

        result = await engine.execute(ctx)

        assert result.status == "SUCCESS"
        assert result.metadata.get("content_gated") is not True
        assert result.metadata["answer_source"] == "general"

    @pytest.mark.asyncio
    async def test_gate_streaming_mode_emits_generator(self):
        mock_llm = AsyncMock()
        mock_prompt_builder = MagicMock()
        mock_prompt_builder.build_prompt.return_value = ("P", "S")

        mock_retriever = AsyncMock()
        mock_retriever.search.return_value = [_doc("mitre lesson", course_slug="blue-team-soc-fundamentals", lesson_title="MITRE")]

        mock_repo = AsyncMock()
        mock_repo.get_enrolled_courses.return_value = []

        engine = NotesGenerationEngine(mock_retriever, mock_llm, mock_prompt_builder, platform_repo=mock_repo)
        ctx = ExecutionContext(metadata={"query": "Cheat sheet for MITRE", "token": "tok"}, streaming_mode=True)

        result = await engine.execute(ctx)

        assert result.status == "SUCCESS"
        assert result.metadata["content_gated"] is True
        assert "generator" in result.metadata

    @pytest.mark.asyncio
    async def test_gate_uses_named_course_when_query_matches_enrolled_catalog_course(self):
        # Query names a non-enrolled catalog course, but the retriever (scoped
        # to enrolled courses) would only return the enrolled course's docs.
        # The gate must resolve the target from the query text against the
        # public catalog, not from retrieval alone.
        mock_llm = AsyncMock()
        mock_llm.generate.return_value = "## Overview\nshort..."
        mock_prompt_builder = MagicMock()
        mock_prompt_builder.build_prompt.return_value = ("P", "S")

        mock_retriever = AsyncMock()
        mock_retriever.search.return_value = [_doc("incident lesson", course_slug="blue-team-soc-fundamentals", lesson_title="Incident Documentation")]

        mock_repo = AsyncMock()
        mock_repo.get_enrolled_courses.return_value = [MagicMock(id="blue-team-soc-fundamentals")]

        engine = NotesGenerationEngine(mock_retriever, mock_llm, mock_prompt_builder, platform_repo=mock_repo)
        ctx = ExecutionContext(metadata={"query": "Generate study notes on incident response fundamentals", "token": "tok"})

        result = await engine.execute(ctx)

        assert result.status == "SUCCESS"
        assert result.metadata["content_gated"] is True
        assert result.metadata["gated_course_slug"] == "incident-response-fundamentals"
        assert result.metadata["course_sources"][0]["course_slug"] == "incident-response-fundamentals"
        assert mock_retriever.search.call_count == 0

    @pytest.mark.asyncio
    async def test_gate_not_triggered_for_enrolled_named_course(self):
        # Query names a course the learner IS enrolled in -> full content.
        mock_llm = AsyncMock()
        mock_llm.generate.return_value = "# SIEM Notes\n## Overview\n..."
        mock_prompt_builder = MagicMock()
        mock_prompt_builder.build_prompt.return_value = ("P", "S")

        mock_retriever = AsyncMock()
        mock_retriever.search.return_value = [_doc("siem lesson", course_slug="siem-fundamentals", lesson_title="SIEM")]

        mock_repo = AsyncMock()
        mock_repo.get_enrolled_courses.return_value = [MagicMock(id="siem-fundamentals")]

        engine = NotesGenerationEngine(mock_retriever, mock_llm, mock_prompt_builder, platform_repo=mock_repo)
        ctx = ExecutionContext(metadata={"query": "Generate study notes on siem fundamentals", "token": "tok"})

        result = await engine.execute(ctx)

        assert result.status == "SUCCESS"
        assert result.metadata.get("content_gated") is not True
        assert result.metadata["answer_source"] == "course"

    @pytest.mark.asyncio
    async def test_gate_fails_closed_when_enrollment_unresolvable(self):
        mock_llm = AsyncMock()
        mock_llm.generate.return_value = "# Notes\n## Overview"
        mock_prompt_builder = MagicMock()
        mock_prompt_builder.build_prompt.return_value = ("P", "S")

        mock_retriever = AsyncMock()
        mock_retriever.search.return_value = [_doc("siem lesson", course_slug="siem-fundamentals", lesson_title="SIEM")]

        mock_repo = AsyncMock()
        mock_repo.get_enrolled_courses.side_effect = RuntimeError("platform down")

        engine = NotesGenerationEngine(mock_retriever, mock_llm, mock_prompt_builder, platform_repo=mock_repo)
        ctx = ExecutionContext(metadata={"query": "Generate notes on SIEM", "token": "tok"})

        result = await engine.execute(ctx)

        assert result.status == "SUCCESS"
        assert result.metadata.get("content_gated") is True
        assert result.metadata["gated_course_slug"] == "siem-fundamentals"


class TestCourseFirstAgentEngine:
    @pytest.mark.asyncio
    async def test_resolve_enrolled_slugs_never_raises(self):
        mock_retriever = AsyncMock()
        mock_retriever.search.return_value = []
        mock_repo = AsyncMock()
        mock_repo.get_enrolled_courses.side_effect = RuntimeError("platform down")
        mock_prompt_builder = MagicMock()
        mock_prompt_builder.build_prompt.return_value = ("P", "S")
        mock_llm = AsyncMock()
        mock_llm.generate.return_value = "ok"

        engine = CourseFirstAgentEngine(mock_retriever, mock_llm, mock_prompt_builder, platform_repo=mock_repo)
        ctx = ExecutionContext(metadata={"query": "notes on SIEM", "token": "tok"})

        result = await engine.execute(ctx)
        assert result.status == "SUCCESS"
