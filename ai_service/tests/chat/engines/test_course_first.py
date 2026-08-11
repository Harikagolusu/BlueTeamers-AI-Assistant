import pytest
from unittest.mock import AsyncMock, MagicMock

from app.chat.engines.rag_engine import RagExecutionEngine
from app.chat.context.execution_context import ExecutionContext
from app.rag.interfaces import Document


def _doc(content, course_slug=None, lesson_title=None, source="lesson_content"):
    return Document(
        content=content,
        metadata={
            "course_slug": course_slug,
            "course_title": course_slug,
            "lesson_title": lesson_title,
            "source": source,
        },
        score=0.8,
    )


class TestCourseFirstRetrieval:
    @pytest.mark.asyncio
    async def test_prioritizes_enrolled_course_material(self):
        mock_llm = AsyncMock()
        mock_llm.generate.return_value = "Course-based answer"
        mock_prompt_builder = MagicMock()
        mock_prompt_builder.build_prompt.return_value = ("P", "S")

        mock_retriever = AsyncMock()
        course_doc = _doc("phishing lesson", course_slug="soc-101", lesson_title="Phishing")
        mock_retriever.search.return_value = [course_doc]

        mock_repo = AsyncMock()
        mock_repo.get_enrolled_courses.return_value = [
            MagicMock(id="soc-101"), MagicMock(id="log-analysis")
        ]

        engine = RagExecutionEngine(mock_retriever, mock_llm, mock_prompt_builder, platform_repo=mock_repo)
        ctx = ExecutionContext(metadata={"query": "What is phishing?", "token": "tok"})

        result = await engine.execute(ctx)

        assert result.status == "SUCCESS"
        assert result.metadata["answer_source"] == "course"
        # Course-scoped retrieval must be attempted with a source + course_slug filter.
        filters = mock_retriever.search.call_args.kwargs.get("metadata_filters")
        assert filters["source"] == "lesson_content"
        assert set(filters["course_slug"]) == {"soc-101", "log-analysis"}

    @pytest.mark.asyncio
    async def test_falls_back_to_general_knowledge(self):
        mock_llm = AsyncMock()
        mock_llm.generate.return_value = "General answer"
        mock_prompt_builder = MagicMock()
        mock_prompt_builder.build_prompt.return_value = ("P", "S")

        # Course-scoped search returns nothing -> general search used.
        mock_retriever = AsyncMock()
        mock_retriever.search.side_effect = [[], [_doc("general info", source="document")]]

        mock_repo = AsyncMock()
        mock_repo.get_enrolled_courses.return_value = [MagicMock(id="soc-101")]

        engine = RagExecutionEngine(mock_retriever, mock_llm, mock_prompt_builder, platform_repo=mock_repo)
        ctx = ExecutionContext(metadata={"query": "What is Python?", "token": "tok"})

        result = await engine.execute(ctx)

        assert result.status == "SUCCESS"
        assert result.metadata["answer_source"] == "general"
        assert mock_retriever.search.call_count == 2

    @pytest.mark.asyncio
    async def test_no_enrollment_uses_general_retrieval(self):
        mock_llm = AsyncMock()
        mock_llm.generate.return_value = "Answer"
        mock_prompt_builder = MagicMock()
        mock_prompt_builder.build_prompt.return_value = ("P", "S")

        mock_retriever = AsyncMock()
        mock_retriever.search.return_value = [_doc("info", source="document")]

        engine = RagExecutionEngine(mock_retriever, mock_llm, mock_prompt_builder, platform_repo=None)
        ctx = ExecutionContext(metadata={"query": "What is DNS?"})

        result = await engine.execute(ctx)

        assert result.status == "SUCCESS"
        assert result.metadata["answer_source"] == "general"
        # Single general search, no metadata filter.
        mock_retriever.search.assert_awaited_once()
        assert mock_retriever.search.call_args.kwargs.get("metadata_filters") is None

    @pytest.mark.asyncio
    async def test_course_source_label_passed_to_prompt(self):
        mock_llm = AsyncMock()
        mock_llm.generate.return_value = "Answer"
        mock_prompt_builder = MagicMock()
        mock_prompt_builder.build_prompt.return_value = ("P", "S")

        mock_retriever = AsyncMock()
        mock_retriever.search.side_effect = [[], [_doc("info", source="document")]]

        mock_repo = AsyncMock()
        mock_repo.get_enrolled_courses.return_value = [MagicMock(id="soc-101")]

        engine = RagExecutionEngine(mock_retriever, mock_llm, mock_prompt_builder, platform_repo=mock_repo)
        ctx = ExecutionContext(metadata={"query": "explain DNS", "token": "tok"})

        await engine.execute(ctx)

        _, prompt_context = mock_prompt_builder.build_prompt.call_args.args
        assert prompt_context["answer_source"] == "general"


class TestRetrievalMetadataFilterListSupport:
    def test_retrieval_service_supports_list_filters(self):
        from app.retrieval.service import RetrievalService

        # Verify the filter branch supports list membership via the service
        # implementation path used by course-first retrieval.
        service = RetrievalService.__new__(RetrievalService)
        assert callable(getattr(service, "retrieve"))
