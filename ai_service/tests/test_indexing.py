import pytest
from unittest.mock import MagicMock

from app.indexing.schemas import IndexDocumentRequest, BatchIndexRequest, DeleteIndexRequest
from app.indexing.service import IndexingService
from app.indexing.exceptions import ChunkingFailure, EmbeddingFailure

from app.chunking.schemas import ChunkResponse, Chunk, ChunkMetadata
from app.embeddings.schemas import BatchEmbeddingResponse

@pytest.fixture
def mock_chunker():
    chunker = MagicMock()
    
    def fake_chunk(req):
        meta = ChunkMetadata(
            chunk_id=f"{req.course_slug}:{req.lesson_id}:chunk-0",
            chunk_index=0,
            course_slug=req.course_slug,
            lesson_id=req.lesson_id,
            lesson_title=req.lesson_title,
            source="test",
            created_at="2026-07-18T00:00:00Z"
        )
        return ChunkResponse(
            lesson_id=req.lesson_id,
            total_chunks=1,
            chunks=[Chunk(text=req.content, metadata=meta)]
        )
    
    chunker.chunk.side_effect = fake_chunk
    return chunker

@pytest.fixture
def mock_embeddings():
    service = MagicMock()
    service.generate_batch_embeddings.return_value = BatchEmbeddingResponse(
        embeddings=[[0.1, 0.2, 0.3]],
        dimension=3,
        model="test",
        batch_size=1,
        processing_time_ms=10.0
    )
    provider_mock = MagicMock()
    provider_mock.health_check.return_value = {"status": "healthy"}
    service.provider = provider_mock
    return service

@pytest.fixture
def mock_vector_store():
    service = MagicMock()
    service.get_health.return_value = {"loaded": True}
    
    meta_mock = MagicMock()
    meta_mock._lock = MagicMock()
    meta_mock._lock.__enter__ = MagicMock()
    meta_mock._lock.__exit__ = MagicMock()
    
    # Mock finding chunks for deletion
    meta_mock.metadata = {
        "test-course:test-lesson:chunk-0": {"lesson_id": "test-lesson"}
    }
    
    service.metadata_store = meta_mock
    return service

@pytest.fixture
def indexing_service(mock_chunker, mock_embeddings, mock_vector_store):
    return IndexingService(mock_chunker, mock_embeddings, mock_vector_store)

def test_single_document_indexing(indexing_service, mock_vector_store):
    req = IndexDocumentRequest(
        lesson_id="test-lesson",
        course_slug="test-course",
        lesson_title="Title",
        content="Hello world"
    )
    res = indexing_service.index_document(req)
    
    assert res.status == "success"
    assert res.chunks_generated == 1
    assert res.embeddings_generated == 1
    assert res.vectors_stored == 1
    mock_vector_store.add_documents.assert_called_once()

def test_batch_indexing(indexing_service):
    req = BatchIndexRequest(documents=[
        IndexDocumentRequest(lesson_id="l1", course_slug="c", lesson_title="t", content="c1"),
        IndexDocumentRequest(lesson_id="l2", course_slug="c", lesson_title="t", content="c2")
    ])
    res = indexing_service.index_documents(req)
    
    assert res.total_documents == 2
    assert res.successful == 2
    assert res.failed == 0

def test_partial_failures(indexing_service, mock_chunker):
    # Make chunker fail on second document
    def failing_chunk(req):
        if req.lesson_id == "l2":
            raise Exception("Chunking crash")
        meta = ChunkMetadata(
            chunk_id=f"{req.course_slug}:{req.lesson_id}:chunk-0",
            chunk_index=0,
            course_slug=req.course_slug,
            lesson_id=req.lesson_id,
            lesson_title=req.lesson_title,
            source="test",
            created_at="2026-07-18T00:00:00Z"
        )
        return ChunkResponse(lesson_id=req.lesson_id, total_chunks=1, chunks=[Chunk(text=req.content, metadata=meta)])
        
    mock_chunker.chunk.side_effect = failing_chunk
    
    req = BatchIndexRequest(documents=[
        IndexDocumentRequest(lesson_id="l1", course_slug="c", lesson_title="t", content="c1"),
        IndexDocumentRequest(lesson_id="l2", course_slug="c", lesson_title="t", content="c2")
    ])
    res = indexing_service.index_documents(req)
    
    assert res.total_documents == 2
    assert res.successful == 1
    assert res.failed == 1
    assert res.results[1].status == "failed"
    assert "Chunking crash" in res.results[1].error

def test_delete_document(indexing_service, mock_vector_store):
    req = DeleteIndexRequest(lesson_id="test-lesson")
    res = indexing_service.delete_document(req)
    assert res is True
    # Verify vector store delete was called with chunk-0
    mock_vector_store.delete.assert_called_with("test-course:test-lesson:chunk-0")

def test_update_document(indexing_service, mock_vector_store):
    req = IndexDocumentRequest(
        lesson_id="test-lesson", course_slug="test-course",
        lesson_title="Title", content="Updated content"
    )
    res = indexing_service.update_document(req)
    
    assert res.status == "success"
    # Should have deleted old and added new
    mock_vector_store.delete.assert_called_with("test-course:test-lesson:chunk-0")
    mock_vector_store.add_documents.assert_called_once()
