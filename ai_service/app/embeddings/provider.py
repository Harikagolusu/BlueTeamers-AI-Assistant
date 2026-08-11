import logging
import threading
from typing import List, Dict, Any

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None

from app.core.config import settings
from app.embeddings.base import BaseEmbeddingProvider
from app.embeddings.exceptions import ModelLoadException, EmbeddingGenerationException

logger = logging.getLogger("app.embeddings.provider")

class SentenceTransformerEmbeddingProvider(BaseEmbeddingProvider):
    """
    Thread-safe Singleton provider utilizing local SentenceTransformers.
    Implements lazy-loading to optimize application startup, and internal batching 
    for memory-safe processing of massive text arrays.
    """
    _instance = None
    _singleton_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._singleton_lock:
                if not cls._instance:
                    cls._instance = super(SentenceTransformerEmbeddingProvider, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # Prevent re-initialization in singleton pattern
        if not hasattr(self, "initialized"):
            # Configuration binding
            self.model_name = getattr(settings, "EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5")
            self.device = getattr(settings, "EMBEDDING_DEVICE", "cpu")
            self.batch_size = getattr(settings, "EMBEDDING_BATCH_SIZE", 32)
            self.normalize = getattr(settings, "EMBEDDING_NORMALIZE", True)
            
            # Lazy loading state and locks
            self.model = None
            self.dimension = None
            self._model_lock = threading.Lock()
            self.initialized = True
            
            # Note: Model is NOT eagerly loaded here to ensure fast startup.

    def load_model(self) -> None:
        """
        Thread-safe lazy loader for the embedding model.
        Uses double-checked locking to avoid unnecessary lock contention on subsequent calls.
        """
        if self.model is not None:
            return
            
        with self._model_lock:
            # Check again inside the lock (double-checked locking)
            if self.model is not None:
                return
            
            if SentenceTransformer is None:
                raise ModelLoadException("sentence-transformers library is not installed.")
                
            try:
                logger.info(f"Lazy loading Embedding Model: {self.model_name} on {self.device}")
                self.model = SentenceTransformer(self.model_name, device=self.device)
                
                # Auto-detect embedding dimension dynamically
                self.dimension = self.model.get_embedding_dimension()
                logger.info(f"Model {self.model_name} loaded successfully. Dimension: {self.dimension}")
            except Exception as e:
                logger.error(f"Failed to load embedding model: {str(e)}")
                raise ModelLoadException(f"Could not load model {self.model_name}: {str(e)}")

    def embed(self, text: str) -> List[float]:
        """
        Generates an embedding for a single text.
        """
        self.load_model()
        try:
            vector = self.model.encode(
                text,
                batch_size=1,
                normalize_embeddings=self.normalize,
                show_progress_bar=False
            )
            return vector.tolist()
        except Exception as e:
            logger.error(f"Embedding generation failed: {str(e)}")
            raise EmbeddingGenerationException(f"Failed to embed text: {str(e)}")

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generates embeddings for a batch of texts.
        Implements internal chunking based on EMBEDDING_BATCH_SIZE to prevent OOM errors
        on massive arrays.
        """
        self.load_model()
        
        all_vectors = []
        try:
            # Internal batching loop
            for i in range(0, len(texts), self.batch_size):
                batch_chunk = texts[i:i + self.batch_size]
                
                vectors = self.model.encode(
                    batch_chunk,
                    batch_size=len(batch_chunk),
                    normalize_embeddings=self.normalize,
                    show_progress_bar=False
                )
                all_vectors.extend(vectors.tolist())
                
            return all_vectors
        except Exception as e:
            logger.error(f"Batch embedding generation failed: {str(e)}")
            raise EmbeddingGenerationException(f"Failed to embed batch: {str(e)}")

    def health_check(self) -> Dict[str, Any]:
        """
        Provides health metrics and model capabilities without triggering inference.
        """
        is_loaded = self.model is not None
        dim = self.dimension if is_loaded else None
        
        return {
            "provider": "SentenceTransformer",
            "model_name": self.model_name,
            "device": self.device,
            "model_loaded": is_loaded,
            "embedding_dimension": dim,
            "normalization_enabled": self.normalize,
            "status": "healthy"
        }
