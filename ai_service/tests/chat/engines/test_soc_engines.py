import pytest
from unittest.mock import AsyncMock, MagicMock

from app.chat.engines.soc_engines import (
    SocSpecialistEngine,
    WazuhLabEngine,
    PracticeLabEngine,
    InvestigationGuidanceEngine,
    WindowsEventLogEngine,
    LinuxLogEngine,
    IocAnalysisEngine,
    MitreGuidanceEngine,
    DetectionRuleEngine,
)
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


def _build_engine(engine_cls, **kwargs):
    mock_llm = AsyncMock()
    mock_llm.generate.return_value = "## Overview\n..."
    mock_prompt_builder = MagicMock()
    mock_prompt_builder.build_prompt.return_value = ("P", "S")
    mock_retriever = AsyncMock()
    mock_retriever.search.return_value = [_doc("soc lesson", course_slug="soc-201", lesson_title="SOC")]
    mock_repo = AsyncMock()
    mock_repo.get_enrolled_courses.return_value = [MagicMock(id="soc-201")]
    return (
        engine_cls(mock_retriever, mock_llm, mock_prompt_builder, platform_repo=mock_repo),
        mock_llm,
        mock_prompt_builder,
        mock_retriever,
    )


ALL_SOC_ENGINES = [
    (WazuhLabEngine, "wazuh_lab_assistant", "## Alert Summary", "Analyze this wazuh alert"),
    (PracticeLabEngine, "practice_lab_assistant", "## Lab Objectives", "Help with the phishing email practice lab"),
    (InvestigationGuidanceEngine, "investigation_guidance_assistant", "## Investigation Workflow", "How do I investigate an alert?"),
    (WindowsEventLogEngine, "windows_event_log_assistant", "## Event ID Table", "What does event id 4625 mean?"),
    (LinuxLogEngine, "linux_log_assistant", "## Common Security Events", "How do I analyze auth.log?"),
    (IocAnalysisEngine, "ioc_analysis_assistant", "## Type Analysis", "Analyze this IOC"),
    (MitreGuidanceEngine, "mitre_guidance_assistant", "## Technique Explanation", "Explain MITRE ATT&CK"),
    (DetectionRuleEngine, "detection_rule_assistant", "## Detection Logic", "Write a Sigma rule"),
]


@pytest.mark.asyncio
@pytest.mark.parametrize("engine_cls,agent_id,section,query", ALL_SOC_ENGINES)
async def test_soc_engine_course_first_retrieval_and_persona(engine_cls, agent_id, section, query):
    engine, mock_llm, mock_prompt_builder, mock_retriever = _build_engine(engine_cls)
    ctx = ExecutionContext(metadata={"query": query, "token": "tok"})

    result = await engine.execute(ctx)

    assert result.status == "SUCCESS"
    assert result.metadata["engine"] == agent_id.upper()
    assert result.metadata["agent"] == agent_id
    assert result.metadata["answer_source"] == "course"

    filters = mock_retriever.search.call_args.kwargs.get("metadata_filters")
    assert filters["source"] == "lesson_content"
    assert filters["course_slug"] == ["soc-201"]

    _, prompt_context = mock_prompt_builder.build_prompt.call_args.args
    assert section in prompt_context["agent_persona"]
    assert "Mentor, do not solve" in prompt_context["agent_persona"]
    assert prompt_context["answer_source"] == "course"


@pytest.mark.asyncio
@pytest.mark.parametrize("engine_cls,agent_id,section,query", ALL_SOC_ENGINES)
async def test_soc_engine_falls_back_to_general_knowledge(engine_cls, agent_id, section, query):
    mock_llm = AsyncMock()
    mock_llm.generate.return_value = "## Overview"
    mock_prompt_builder = MagicMock()
    mock_prompt_builder.build_prompt.return_value = ("P", "S")
    mock_retriever = AsyncMock()
    mock_retriever.search.side_effect = [[], [_doc("general", source="document")]]
    mock_repo = AsyncMock()
    mock_repo.get_enrolled_courses.return_value = [MagicMock(id="soc-201")]

    engine = engine_cls(mock_retriever, mock_llm, mock_prompt_builder, platform_repo=mock_repo)
    ctx = ExecutionContext(metadata={"query": query, "token": "tok"})

    result = await engine.execute(ctx)

    assert result.status == "SUCCESS"
    assert result.metadata["answer_source"] == "general"
    assert mock_retriever.search.call_count == 2


@pytest.mark.asyncio
async def test_soc_engine_is_lab_context_aware():
    engine, mock_llm, mock_prompt_builder, _ = _build_engine(WazuhLabEngine)
    ctx = ExecutionContext(
        metadata={
            "query": "Where do I start in this lab?",
            "token": "tok",
            "context": {"lab": {"action": "start", "lab_id": "wazuh-lab-1"}},
        }
    )

    result = await engine.execute(ctx)
    assert result.status == "SUCCESS"

    _, prompt_context = mock_prompt_builder.build_prompt.call_args.args
    assert prompt_context["active_lab"] == {"action": "start", "lab_id": "wazuh-lab-1"}


@pytest.mark.asyncio
async def test_soc_engine_ignores_malformed_lab_context():
    engine, mock_llm, mock_prompt_builder, _ = _build_engine(PracticeLabEngine)
    ctx = ExecutionContext(
        metadata={"query": "help with practice lab", "context": {"lab": None}}
    )

    await engine.execute(ctx)

    _, prompt_context = mock_prompt_builder.build_prompt.call_args.args
    assert "active_lab" not in prompt_context


@pytest.mark.asyncio
async def test_soc_engine_streaming_mode():
    engine, mock_llm, mock_prompt_builder, _ = _build_engine(WindowsEventLogEngine)
    ctx = ExecutionContext(
        metadata={"query": "event id 4625"}, streaming_mode=True
    )

    result = await engine.execute(ctx)
    assert result.status == "SUCCESS"
    assert "generator" in result.metadata


@pytest.mark.asyncio
async def test_base_has_no_active_lab_without_context():
    engine = SocSpecialistEngine.__new__(SocSpecialistEngine)
    ctx = ExecutionContext(metadata={"query": "x"})
    assert engine._active_lab_context(ctx) == {}
