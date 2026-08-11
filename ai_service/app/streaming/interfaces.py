from abc import ABC, abstractmethod
from typing import AsyncGenerator
from app.rag.schemas import RAGRequest

class BaseStreamingService(ABC):
    @abstractmethod
    async def stream_chat(self, request: RAGRequest, conversation_id: str = None) -> AsyncGenerator[str, None]:
        """
        Yields SSE-formatted strings (`data: {...}\n\n`) to the router.
        """
        pass
        
    @abstractmethod
    async def health_check(self) -> dict:
        pass
