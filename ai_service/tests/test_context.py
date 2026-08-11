import pytest

from app.context.schemas import ContextRequest
from app.context.service import ContextBuilderService
from app.retrieval.schemas import RetrievedChunk
from app.context.tokenizer import TokenEstimator

@pytest.fixture
def service():
    return ContextBuilderService()

def test_deduplication(service):
    chunks = [
        RetrievedChunk(chunk_id="c1", score=0.9, text="t1", metadata={}),
        RetrievedChunk(chunk_id="c1", score=0.9, text="t1", metadata={}),
    ]
    req = ContextRequest(chunks=chunks, max_tokens=1000)
    res = service.build_context(req)
    
    assert res.original_chunk_count == 2
    assert res.merged_chunk_count == 1
    assert len(res.document.chunks) == 1

def test_adjacent_merging(service):
    chunks = [
        RetrievedChunk(
            chunk_id="c2", score=0.8, text="Second",
            metadata={"lesson_id": "l1", "chunk_index": 2}
        ),
        RetrievedChunk(
            chunk_id="c1", score=0.9, text="First",
            metadata={"lesson_id": "l1", "chunk_index": 1}
        ),
    ]
    req = ContextRequest(chunks=chunks, max_tokens=1000)
    res = service.build_context(req)
    
    # Should merge into 1 chunk because they are lesson 1, index 1 & 2
    assert res.merged_chunk_count == 1
    assert "First\n\nSecond" in res.document.chunks[0].text
    # Keeps max score
    assert res.document.chunks[0].score == 0.9

def test_token_trimming(service):
    # Force max tokens to 10
    chunks = [
        RetrievedChunk(chunk_id="c1", score=0.9, text="This is a long sentence taking tokens", metadata={}),
        RetrievedChunk(chunk_id="c2", score=0.5, text="This is another sentence", metadata={}),
    ]
    req = ContextRequest(chunks=chunks, max_tokens=10)
    res = service.build_context(req)
    
    # c1 is ~9 tokens. c2 is ~5 tokens. Total ~14.
    # Budget is 10. c2 has lowest score (0.5), should be trimmed.
    assert res.trimmed_chunk_count == 1
    assert len(res.document.chunks) == 1
    assert res.document.chunks[0].id == "c1"

def test_health_check(service):
    h = service.health_check()
    assert h["builder_status"] == "healthy"
