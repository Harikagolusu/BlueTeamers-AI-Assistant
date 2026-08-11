import pytest
from unittest.mock import MagicMock

from app.retrieval.schemas import RetrievalRequest, BatchRetrievalRequest
from app.retrieval.service import RetrievalService
from app.retrieval.reranker import IdentityReranker
from app.retrieval.exceptions import EmbeddingFailure, SearchFailure

from app.embeddings.schemas import EmbeddingResponse
from app.vector_store.schemas import SearchResponse as VSearchResponse
from app.vector_store.schemas import SearchResult

@pytest.fixture
def mock_embeddings():
    service = MagicMock()
    service.generate_embedding.return_value = EmbeddingResponse(
        embedding=[0.1, 0.2, 0.3],
        dimension=3,
        model="test",
        processing_time_ms=10.0
    )
    provider_mock = MagicMock()
    provider_mock.health_check.return_value = {"status": "healthy"}
    service.provider = provider_mock
    return service

@pytest.fixture
def mock_vector_store():
    service = MagicMock()
    service.get_health.return_value = {"loaded": True, "metadata_count": 5}
    
    # Return two fake chunks
    service.search.return_value = VSearchResponse(
        results=[
            SearchResult(id="c1", score=0.9, metadata={"text": "Hello", "source": "A"}),
            SearchResult(id="c2", score=0.5, metadata={"text": "World", "source": "B"})
        ],
        processing_time_ms=5.0
    )
    return service

@pytest.fixture
def retrieval_service(mock_embeddings, mock_vector_store):
    return RetrievalService(mock_embeddings, mock_vector_store, IdentityReranker())

def test_query_embedding_and_retrieval(retrieval_service, mock_embeddings, mock_vector_store):
    req = RetrievalRequest(query="test query")
    res = retrieval_service.retrieve(req)
    
    mock_embeddings.generate_embedding.assert_called_once()
    mock_vector_store.search.assert_called_once()
    
    assert res.query_length == 10
    assert len(res.results) == 2
    assert res.results[0].chunk_id == "c1"
    assert res.results[0].text == "Hello"

def test_top_k_handling(retrieval_service, mock_vector_store):
    # Ask for top_k 100, should be capped at max_top_k (20)
    req = RetrievalRequest(query="q", top_k=100)
    retrieval_service.retrieve(req)
    # Get the search request passed to vector_store
    call_args = mock_vector_store.search.call_args[0][0]
    assert call_args.top_k == 20

def test_similarity_filtering(retrieval_service):
    # One chunk has score 0.9, one has 0.5. Filter by 0.8
    req = RetrievalRequest(query="q", min_score=0.8)
    res = retrieval_service.retrieve(req)
    assert len(res.results) == 1
    assert res.results[0].chunk_id == "c1"

def test_metadata_filtering(retrieval_service):
    req = RetrievalRequest(query="q", metadata_filters={"source": "B"})
    res = retrieval_service.retrieve(req)
    assert len(res.results) == 1
    assert res.results[0].chunk_id == "c2"

def test_metadata_filtering_with_list_membership(retrieval_service):
    # List/tuple/set values use membership, enabling course-slug scoping for
    # course-material-first retrieval.
    req = RetrievalRequest(query="q", metadata_filters={"source": ["A", "B"]})
    res = retrieval_service.retrieve(req)
    assert len(res.results) == 2

    req = RetrievalRequest(query="q", metadata_filters={"source": ["A"]})
    res = retrieval_service.retrieve(req)
    assert len(res.results) == 1
    assert res.results[0].chunk_id == "c1"

def test_dependency_failures(retrieval_service, mock_embeddings):
    # Force embedding to fail
    mock_embeddings.generate_embedding.side_effect = Exception("Crash")
    req = RetrievalRequest(query="q")
    with pytest.raises(EmbeddingFailure):
        retrieval_service.retrieve(req)

def test_health_check(retrieval_service):
    health = retrieval_service.health_check()
    assert health.overall_health is True
    assert health.embedding_service == "healthy"
    assert health.vector_store == "healthy"
