from abc import ABC, abstractmethod
from typing import List
from app.retrieval.schemas import RetrievedChunk

class BaseReranker(ABC):
    @abstractmethod
    def rerank(self, query: str, chunks: List[RetrievedChunk]) -> List[RetrievedChunk]:
        """Re-orders and potentially filters the retrieved chunks based on a cross-encoder or heuristic."""
        pass

class IdentityReranker(BaseReranker):
    """
    Placeholder reranker that returns the results exactly as provided by the Vector Store.
    Obeys the Open/Closed Principle to allow future Cross-Encoder rerankers to drop in seamlessly.
    """
    def rerank(self, query: str, chunks: List[RetrievedChunk]) -> List[RetrievedChunk]:
        return chunks
