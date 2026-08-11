import pytest
import numpy as np
from unittest.mock import MagicMock

from app.vector_store.metadata_store import MetadataStore
from app.vector_store.provider import FaissVectorStore
from app.vector_store.service import VectorStoreService
from app.vector_store.schemas import VectorDocument, SearchRequest

@pytest.fixture
def mock_embedding_provider():
    mock = MagicMock()
    mock.health_check.return_value = {"embedding_dimension": 4, "loaded": True}
    return mock

@pytest.fixture
def faiss_provider(tmp_path):
    provider = FaissVectorStore()
    provider.filepath = tmp_path / "index.faiss"
    provider.initialize(4)
    return provider

@pytest.fixture
def metadata_store(tmp_path):
    store = MetadataStore()
    # Override filepath for isolated testing
    store.filepath = tmp_path / "metadata.json"
    return store

@pytest.fixture
def service(faiss_provider, metadata_store, mock_embedding_provider):
    return VectorStoreService(faiss_provider, metadata_store, mock_embedding_provider)

def test_initialization(service):
    health = service.get_health()
    assert health["loaded"] is True
    assert health["dimension"] == 4
    assert health["vector_count"] == 0
    assert health["metadata_count"] == 0

def test_add_and_search(service):
    doc = VectorDocument(
        id="chunk-1",
        vector=[1.0, 0.0, 0.0, 0.0],
        metadata={"title": "Test Lesson"}
    )
    service.add_document(doc)
    
    assert service.get_health()["vector_count"] == 1
    
    req = SearchRequest(query_vector=[0.9, 0.1, 0.0, 0.0], top_k=1)
    res = service.search(req)
    
    assert len(res.results) == 1
    assert res.results[0].id == "chunk-1"
    assert res.results[0].metadata["title"] == "Test Lesson"
    # Score for inner product between [1,0,0,0] and [0.9,0.1,0,0] is 0.9
    assert abs(res.results[0].score - 0.9) < 0.01

def test_batch_add(service):
    docs = [
        VectorDocument(id=f"doc-{i}", vector=[0.5, 0.5, 0.0, 0.0], metadata={"idx": i})
        for i in range(10)
    ]
    service.add_documents(docs)
    
    assert service.get_health()["vector_count"] == 10
    assert service.get_health()["metadata_count"] == 10

def test_delete(service):
    doc = VectorDocument(id="delete-me", vector=[1.0, 1.0, 1.0, 1.0], metadata={})
    service.add_document(doc)
    assert service.get_health()["vector_count"] == 1
    
    service.delete("delete-me")
    assert service.get_health()["vector_count"] == 0
    assert service.get_health()["metadata_count"] == 0

def test_save_and_load(faiss_provider, metadata_store, mock_embedding_provider, tmp_path):
    faiss_provider.filepath = tmp_path / "index.faiss"
    service1 = VectorStoreService(faiss_provider, metadata_store, mock_embedding_provider)
    
    service1.add_document(VectorDocument(id="test-1", vector=[1.0, 0.0, 0.0, 0.0], metadata={"x": 1}))
    service1.save()
    
    # Create new instances to test load
    new_faiss = FaissVectorStore()
    new_faiss.filepath = tmp_path / "index.faiss"
    new_meta = MetadataStore()
    new_meta.filepath = tmp_path / "metadata.json"
    
    service2 = VectorStoreService(new_faiss, new_meta, mock_embedding_provider)
    
    assert service2.get_health()["vector_count"] == 1
    assert service2.get_health()["metadata_count"] == 1
    
    res = service2.search(SearchRequest(query_vector=[1.0, 0.0, 0.0, 0.0], top_k=1))
    assert res.results[0].id == "test-1"
