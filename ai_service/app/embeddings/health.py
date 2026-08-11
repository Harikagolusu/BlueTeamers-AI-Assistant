from app.embeddings.base import BaseEmbeddingProvider
from typing import Dict, Any

def get_embedding_health(provider: BaseEmbeddingProvider) -> Dict[str, Any]:
    """Expose a dedicated health check utility."""
    return provider.health_check()
