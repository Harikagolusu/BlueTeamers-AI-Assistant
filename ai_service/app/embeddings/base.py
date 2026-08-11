from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseEmbeddingProvider(ABC):
    """
    Abstract interface for embedding generation.
    Decouples the core application logic from the underlying model (e.g., SentenceTransformers, 
    AWS Bedrock, OpenAI). Complies strictly with the Open/Closed Principle.
    """
    
    @abstractmethod
    def load_model(self) -> None:
        """Load the embedding model into memory (supports lazy loading)."""
        pass

    @abstractmethod
    def embed(self, text: str) -> List[float]:
        """Generate a vector embedding for a single text string."""
        pass

    @abstractmethod
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate vector embeddings for a batch of text strings."""
        pass

    @abstractmethod
    def health_check(self) -> Dict[str, Any]:
        """Verify the model is loaded and functional without running inference."""
        pass
