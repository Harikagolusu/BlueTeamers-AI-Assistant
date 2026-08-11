import pytest
import threading
from unittest.mock import MagicMock, patch

from app.embeddings.schemas import EmbeddingRequest, BatchEmbeddingRequest
from app.embeddings.exceptions import InvalidInputException, ModelLoadException
from app.embeddings.provider import SentenceTransformerEmbeddingProvider
from app.embeddings.service import EmbeddingService

@pytest.fixture(autouse=True)
def reset_singleton():
    SentenceTransformerEmbeddingProvider._instance = None
    yield

@pytest.fixture
def mock_sentence_transformer():
    with patch('app.embeddings.provider.SentenceTransformer') as mock_st:
        mock_model = MagicMock()
        # Mock the dimension detection
        mock_model.get_embedding_dimension.return_value = 384
        
        # Mock encode for both single and batched
        def encode_mock(text_or_texts, **kwargs):
            import numpy as np
            if isinstance(text_or_texts, str):
                return np.array([0.1] * 384)
            else:
                return np.array([[0.1] * 384 for _ in text_or_texts])
                
        mock_model.encode.side_effect = encode_mock
        mock_st.return_value = mock_model
        yield mock_model

@pytest.fixture
def provider(mock_sentence_transformer):
    return SentenceTransformerEmbeddingProvider()

def test_lazy_loading(provider, mock_sentence_transformer):
    # Model should be None immediately after init
    assert provider.model is None
    assert provider.dimension is None
    
    # Model should load upon first request
    provider.load_model()
    assert provider.model is not None
    assert provider.dimension == 384

def test_singleton_thread_safety(mock_sentence_transformer):
    # Ensure multiple concurrent attempts only create one instance
    instances = []
    
    def create_instance():
        instances.append(SentenceTransformerEmbeddingProvider())
        
    threads = [threading.Thread(target=create_instance) for _ in range(5)]
    for t in threads: t.start()
    for t in threads: t.join()
    
    # All threads should have received the exact same memory instance
    assert all(inst is instances[0] for inst in instances)

def test_internal_batching(provider, mock_sentence_transformer):
    # Force a very small batch size to test internal chunking
    provider.batch_size = 2
    
    # Send 5 texts, which should result in 3 separate calls to the mocked encode
    texts = ["T1", "T2", "T3", "T4", "T5"]
    result = provider.embed_batch(texts)
    
    assert len(result) == 5
    assert len(result[0]) == 384
    # The mock model's encode method should have been called 3 times (2, 2, 1)
    assert provider.model.encode.call_count == 3

def test_health_check(provider, mock_sentence_transformer):
    # Test pre-load health
    health_pre = provider.health_check()
    assert health_pre["model_loaded"] is False
    assert health_pre["embedding_dimension"] is None
    
    # Test post-load health
    provider.load_model()
    health_post = provider.health_check()
    assert health_post["model_loaded"] is True
    assert health_post["embedding_dimension"] == 384
    
def test_exceptions_wrap_properly(provider):
    # With no mocking, trying to load a garbage model should throw ModelLoadException
    with patch('app.embeddings.provider.SentenceTransformer', side_effect=Exception("Fake Error")):
        with pytest.raises(ModelLoadException):
            provider.load_model()
