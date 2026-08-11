from abc import ABC, abstractmethod
from app.rag.schemas import RAGRequest, RAGResponse

class BaseRAGEngine(ABC):
    @abstractmethod
    def generate_answer(self, request: RAGRequest) -> RAGResponse:
        """Executes the complete synchronous RAG pipeline."""
        pass
        
    @abstractmethod
    async def stream_answer(self, request: RAGRequest):
        """
        Executes the RAG pipeline asynchronously and yields chunks.
        Should return an AsyncGenerator that yields strings and finally a RAGResponse.
        """
        pass
