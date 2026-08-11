import pytest
from unittest.mock import AsyncMock, MagicMock
from app.chat.engines.general_engine import GeneralExecutionEngine
from app.chat.engines.rag_engine import RagExecutionEngine
from app.chat.engines.tool_engine import ToolExecutionEngine
from app.chat.context.execution_context import ExecutionContext
from app.rag.interfaces import Document

@pytest.mark.asyncio
async def test_general_engine_non_streaming():
    mock_llm = AsyncMock()
    mock_llm.generate.return_value = "Hello World"

    mock_prompt_builder = MagicMock()
    mock_prompt_builder.build_prompt.return_value = ("User: Hi", "System: You are an AI")

    engine = GeneralExecutionEngine(mock_llm, mock_prompt_builder)
    ctx = ExecutionContext(metadata={"query": "Hi"})

    result = await engine.execute(ctx)

    assert result.status == "SUCCESS"
    assert result.message == "Hello World"
    mock_prompt_builder.build_prompt.assert_called_once_with("Hi", {})
    mock_llm.generate.assert_called_once_with("User: Hi", system_prompt="System: You are an AI", images=None)

@pytest.mark.asyncio
async def test_general_engine_off_topic_refuses_without_llm():
    mock_llm = AsyncMock()
    mock_prompt_builder = MagicMock()

    engine = GeneralExecutionEngine(mock_llm, mock_prompt_builder)
    ctx = ExecutionContext(
        metadata={"query": "Tell me a joke", "intent": "OFF_TOPIC", "domain": "general"}
    )

    result = await engine.execute(ctx)

    assert result.status == "SUCCESS"
    assert "outside my scope" in result.message
    assert result.metadata["llm_used"] is False
    mock_llm.generate.assert_not_called()
    mock_llm.stream.assert_not_called()
    mock_prompt_builder.build_prompt.assert_not_called()

@pytest.mark.asyncio
async def test_rag_engine_non_streaming():
    mock_llm = AsyncMock()
    mock_llm.generate.return_value = "RAG Response"

    mock_prompt_builder = MagicMock()
    mock_prompt_builder.build_prompt.return_value = ("RAG Prompt", "RAG System")

    mock_retriever = AsyncMock()
    doc1 = Document(
        content="info",
        metadata={"course_title": "Course A", "lesson_title": "Lesson 1", "chunk_id": "chunk-1", "source": "doc1.txt"},
        score=0.85,
    )
    mock_retriever.search.return_value = [doc1]

    engine = RagExecutionEngine(mock_retriever, mock_llm, mock_prompt_builder)
    ctx = ExecutionContext(metadata={"query": "search query"})

    result = await engine.execute(ctx)

    assert result.status == "SUCCESS"
    assert result.message == "RAG Response"
    assert len(result.documents) == 1
    # Citations must conform to the SourceCitation contract.
    assert result.citations == [{
        "course": "Course A",
        "lesson": "Lesson 1",
        "chunk_id": "chunk-1",
        "similarity_score": 0.85,
        "source_title": "Course A - Lesson 1",
        "source_reference": "doc1.txt",
    }]
    mock_retriever.search.assert_called_once_with("search query", top_k=5)

@pytest.mark.asyncio
async def test_tool_engine_execution():
    mock_resolver = MagicMock()
    mock_provider = AsyncMock()
    mock_provider.execute.return_value = {"result": "success", "result_message": "Action complete", "data": 123}
    mock_resolver.resolve.return_value = mock_provider
    engine = ToolExecutionEngine(mock_resolver)
    ctx = ExecutionContext(metadata={"target_tool": "calculator", "tool_args": {"a": 1}}, permissions={"test.read": True})
    result = await engine.execute(ctx)

    assert result.status == "SUCCESS"
    assert result.message == "Action complete"
    assert len(result.tool_outputs) == 1
    assert result.tool_outputs[0]["tool"] == "calculator"
    assert result.tool_outputs[0]["response"]["data"] == 123
