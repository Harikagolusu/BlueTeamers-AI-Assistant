import pytest
from unittest.mock import AsyncMock, MagicMock

from app.chat.engines.specialist_engines import InvestigationExecutionEngine
from app.chat.context.execution_context import ExecutionContext


class TestInvestigationLogAnalysis:
    @pytest.fixture
    def engine(self):
        mock_llm = AsyncMock()
        mock_llm.generate.return_value = "Log analysis result"
        mock_prompt_builder = MagicMock()
        mock_prompt_builder.build_prompt.return_value = ("P", "S")
        retriever = AsyncMock()
        return InvestigationExecutionEngine(retriever, mock_llm, mock_prompt_builder)

    def _ctx(self, files=None, stream=False):
        return ExecutionContext(
            metadata={
                "query": "analyze this log file",
                "files": files or [],
                "intent": "INVESTIGATION",
                "domain": "investigation",
            },
            streaming_mode=stream,
        )

    @pytest.mark.asyncio
    async def test_log_attachment_uses_log_analysis_path(self, engine):
        ctx = self._ctx(files=[{"name": "Android_2k.log", "type": "text/plain", "content": "log data"}])
        result = await engine.execute(ctx)

        assert result.status == "SUCCESS"
        assert result.message == "Log analysis result"
        assert result.metadata["agent"] == "investigation_assistant"
        assert result.metadata["answer_source"] == "log_attachment"
        # No RAG retrieval and no course source cards for log analysis.
        engine._retriever.search.assert_not_awaited()
        assert result.metadata.get("course_sources") in (None, [])
        assert result.documents == []

    @pytest.mark.asyncio
    async def test_log_analysis_persona_used(self, engine):
        ctx = self._ctx(files=[{"name": "server.log", "type": "text/plain", "content": "x"}])
        await engine.execute(ctx)
        _, kwargs = engine._llm.generate.call_args
        assert "senior SOC analyst performing log analysis" in kwargs["system_prompt"]
        assert "Executive Summary" in kwargs["system_prompt"]

    @pytest.mark.asyncio
    async def test_no_attachment_uses_course_grounded_path(self, engine):
        # Without an attachment the investigation engine stays on the
        # RAG-grounded path (retrieval + course sources).
        engine._retriever.search.return_value = []
        ctx = self._ctx(files=[])
        result = await engine.execute(ctx)

        assert result.status == "SUCCESS"
        engine._retriever.search.assert_awaited_once()
        assert result.metadata.get("answer_source") != "log_attachment"

    @pytest.mark.asyncio
    async def test_streaming_log_analysis(self, engine):
        ctx = self._ctx(
            files=[{"name": "app.json", "type": "application/json", "content": "{}"}],
            stream=True,
        )
        result = await engine.execute(ctx)
        assert result.status == "SUCCESS"
        assert result.metadata["answer_source"] == "log_attachment"
        assert "generator" in result.metadata
