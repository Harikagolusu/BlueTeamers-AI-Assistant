import pytest
from unittest.mock import AsyncMock, MagicMock

from app.chat.engines.specialist_engines import ThreatIntelExecutionEngine
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


class FakeIndicatorTool:
    name = "IndicatorFetcherTool"

    async def execute(self, context, **kwargs):
        return {"malicious": True, "reputation_score": 5, "tags": ["c2", "malware"]}


class TestThreatIntelExternalFallback:
    @pytest.mark.asyncio
    async def test_entity_not_in_kb_uses_external_fallback(self):
        mock_llm = AsyncMock()
        mock_llm.generate.return_value = "# CVE Report"
        mock_prompt_builder = MagicMock()
        mock_prompt_builder.build_prompt.return_value = ("P", "S")

        # Retrieval returns course docs that do NOT mention CVE-2024-1234.
        mock_retriever = AsyncMock()
        mock_retriever.search.return_value = [
            _doc("A related CVE: CVE-2024-5678 with CVSS 9.8", course_slug="soc-201", lesson_title="Vuln Mgmt")
        ]

        tool = FakeIndicatorTool()
        engine = ThreatIntelExecutionEngine(mock_retriever, mock_llm, mock_prompt_builder, external_tools=[tool])
        ctx = ExecutionContext(metadata={"query": "Explain CVE-2024-1234", "intent": "THREAT_INTEL"})

        result = await engine.execute(ctx)

        assert result.status == "SUCCESS"
        assert result.metadata["external_fallback"] is True
        assert result.metadata["external_entities"] == ["CVE-2024-1234"]
        assert len(result.metadata["external_tool_results"]) >= 1
        assert result.metadata["external_tool_results"][0]["tool"] == "IndicatorFetcherTool"

        _, prompt_context = mock_prompt_builder.build_prompt.call_args.args
        assert prompt_context["external_fallback"] is True
        assert "external tool results" in prompt_context["agent_persona"].lower()

    @pytest.mark.asyncio
    async def test_entity_in_kb_uses_normal_path(self):
        mock_llm = AsyncMock()
        mock_llm.generate.return_value = "## Overview\n..."
        mock_prompt_builder = MagicMock()
        mock_prompt_builder.build_prompt.return_value = ("P", "S")

        mock_retriever = AsyncMock()
        mock_retriever.search.return_value = [
            _doc("CVE-2024-1234 is a buffer overflow in the DHCP client.", course_slug="soc-201", lesson_title="Vuln Mgmt")
        ]

        engine = ThreatIntelExecutionEngine(mock_retriever, mock_llm, mock_prompt_builder, external_tools=[FakeIndicatorTool()])
        ctx = ExecutionContext(metadata={"query": "Explain CVE-2024-1234", "intent": "THREAT_INTEL"})

        result = await engine.execute(ctx)

        assert result.status == "SUCCESS"
        assert result.metadata.get("external_fallback") in (None, False)
        assert result.metadata["answer_source"] == "general"

    @pytest.mark.asyncio
    async def test_no_entity_query_uses_normal_path(self):
        mock_llm = AsyncMock()
        mock_llm.generate.return_value = "## Overview\n..."
        mock_prompt_builder = MagicMock()
        mock_prompt_builder.build_prompt.return_value = ("P", "S")

        mock_retriever = AsyncMock()
        mock_retriever.search.return_value = [_doc("Threat actor group analysis")]

        engine = ThreatIntelExecutionEngine(mock_retriever, mock_llm, mock_prompt_builder, external_tools=[FakeIndicatorTool()])
        ctx = ExecutionContext(metadata={"query": "Tell me about APT28 threat actor"})

        result = await engine.execute(ctx)

        assert result.status == "SUCCESS"
        assert result.metadata.get("external_fallback") in (None, False)

    @pytest.mark.asyncio
    async def test_external_tool_failure_does_not_break_response(self):
        mock_llm = AsyncMock()
        mock_llm.generate.return_value = "## Overview\nGeneral knowledge answer"
        mock_prompt_builder = MagicMock()
        mock_prompt_builder.build_prompt.return_value = ("P", "S")

        mock_retriever = AsyncMock()
        mock_retriever.search.return_value = []

        class BrokenTool:
            name = "BrokenTool"

            async def execute(self, context, **kwargs):
                raise RuntimeError("external provider down")

        engine = ThreatIntelExecutionEngine(mock_retriever, mock_llm, mock_prompt_builder, external_tools=[BrokenTool()])
        ctx = ExecutionContext(metadata={"query": "Explain CVE-2024-9999"})

        result = await engine.execute(ctx)

        assert result.status == "SUCCESS"
        assert result.metadata["external_fallback"] is True
        assert result.metadata["external_tool_results"] == []

    @pytest.mark.asyncio
    async def test_streaming_external_fallback(self):
        mock_llm = AsyncMock()
        mock_prompt_builder = MagicMock()
        mock_prompt_builder.build_prompt.return_value = ("P", "S")

        mock_retriever = AsyncMock()
        mock_retriever.search.return_value = []

        engine = ThreatIntelExecutionEngine(mock_retriever, mock_llm, mock_prompt_builder, external_tools=[FakeIndicatorTool()])
        ctx = ExecutionContext(metadata={"query": "Explain CVE-2024-7777"}, streaming_mode=True)

        result = await engine.execute(ctx)

        assert result.status == "SUCCESS"
        assert result.metadata["external_fallback"] is True
        assert "generator" in result.metadata
