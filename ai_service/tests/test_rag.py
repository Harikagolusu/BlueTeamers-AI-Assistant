import pytest
import uuid
from unittest.mock import MagicMock

from app.rag.schemas import RAGRequest, RAGResponse
from app.rag.engine import RAGEngine
from app.rag.service import RAGService
from app.rag.validator import ResponseValidator
from app.rag.exceptions import EmptyContextException, ValidationFailure, OrchestrationFailure

from app.retrieval.schemas import RetrievalResponse, RetrievedChunk
from app.context.schemas import ContextResponse, ContextDocument, ContextChunk
from app.prompt_builder.schemas import PromptResponse, PromptPayload
from app.llm.schemas import LLMResponse

@pytest.fixture
def mock_retrieval():
    mock = MagicMock()
    mock.retrieve.return_value = RetrievalResponse(
        query_length=5,
        results=[RetrievedChunk(chunk_id="c1", score=0.9, text="data", metadata={"course_slug": "cs", "lesson_id": "ls", "lesson_title": "t"})],
        processing_time_ms=1.0
    )
    return mock

@pytest.fixture
def mock_context():
    mock = MagicMock()
    mock.build_context.return_value = ContextResponse(
        document=ContextDocument(
            chunks=[ContextChunk(id="c1", text="data", score=0.9, metadata={"course_slug": "cs", "lesson_id": "ls", "lesson_title": "t"})],
            estimated_tokens=5,
            formatted_text="context"
        ),
        original_chunk_count=1,
        merged_chunk_count=1,
        trimmed_chunk_count=0,
        processing_time_ms=1.0
    )
    return mock

@pytest.fixture
def mock_prompt():
    mock = MagicMock()
    mock.build_prompt.return_value = PromptResponse(
        payload=PromptPayload(system="sys", user="user"),
        estimated_tokens=10,
        processing_time_ms=1.0,
        template_used="test"
    )
    return mock

@pytest.fixture
def mock_llm():
    mock = MagicMock()
    mock.generate.return_value = LLMResponse(
        text="answer",
        provider="test",
        model="test",
        latency_ms=5.0
    )
    return mock

@pytest.fixture
def validator():
    return ResponseValidator()

@pytest.fixture
def rag_engine(mock_retrieval, mock_context, mock_prompt, mock_llm, validator):
    return RAGEngine(mock_retrieval, mock_context, mock_prompt, mock_llm, validator)

@pytest.fixture
def rag_service(rag_engine):
    return RAGService(rag_engine)

def test_rag_pipeline_success(rag_service):
    req = RAGRequest(query="test")
    res = rag_service.generate_answer(req)
    
    # Verify request_id was assigned by service
    assert req.request_id is not None
    assert isinstance(req.request_id, uuid.UUID)
    
    # Verify response structure
    assert isinstance(res, RAGResponse)
    assert res.answer == "answer"
    assert len(res.citations) == 1
    assert res.citations[0].chunk_id == "c1"
    
    # Verify metrics aggregated exclusively by RAGEngine
    assert res.metrics.retrieval_latency_ms > 0
    assert res.metrics.total_latency_ms > 0

def test_empty_context_exception(rag_service, mock_retrieval):
    # Simulate empty retrieval
    mock_retrieval.retrieve.return_value = RetrievalResponse(
        query_length=5, results=[], processing_time_ms=1.0
    )
    req = RAGRequest(query="fail")
    with pytest.raises(EmptyContextException):
        rag_service.generate_answer(req)

def test_validation_failure(rag_service, mock_llm):
    # Simulate empty LLM output
    mock_llm.generate.return_value = LLMResponse(
        text="   ", provider="test", model="test", latency_ms=5.0
    )
    req = RAGRequest(query="fail")
    with pytest.raises(ValidationFailure):
        rag_service.generate_answer(req)

def test_orchestration_failure(rag_service, rag_engine):
    # Simulate unhandled python fault escaping the engine
    rag_engine.generate_answer = MagicMock(side_effect=TypeError("Boom"))
    req = RAGRequest(query="fail")
    with pytest.raises(OrchestrationFailure):
        rag_service.generate_answer(req)
