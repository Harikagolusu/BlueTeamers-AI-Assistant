from abc import ABC, abstractmethod
from app.chunking.schemas import ChunkRequest, ChunkResponse

class BaseChunker(ABC):
    """Abstract base interface for all chunking implementations."""
    
    @abstractmethod
    def clean_text(self, text: str) -> str:
        """Remove unnecessary whitespace and artifacts from raw text."""
        pass

    @abstractmethod
    def validate(self, text: str) -> bool:
        """Ensure the text meets structural and size requirements."""
        pass

    @abstractmethod
    def chunk(self, request: ChunkRequest) -> ChunkResponse:
        """Process the request and return standardized chunks."""
        pass
