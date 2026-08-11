from abc import ABC, abstractmethod
from typing import AsyncGenerator, Union
from app.models.chat.chat_models import ChatRequest, ChatResponse

class IChatService(ABC):
    """
    Application Layer boundary. Prevents the API from knowing about orchestration.
    Handles request validation, transaction boundaries, dependency resolution,
    streaming selection, and feature flag evaluation before calling the Orchestrator.
    """
    @abstractmethod
    async def process_request(self, request: ChatRequest) -> Union[ChatResponse, AsyncGenerator[str, None]]:
        """Process the incoming chat request and return a response or an SSE stream."""
        pass
