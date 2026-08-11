from fastapi import Depends

from app.rag.service import RAGService
from app.rag.dependencies import get_rag_service, get_rag_health_service
from app.rag.health import RAGHealthService
from app.chat.health import ChatHealthService

def get_chat_health_service(
    rag_health: RAGHealthService = Depends(get_rag_health_service)
) -> ChatHealthService:
    return ChatHealthService(rag_health)

# Since Chat just uses RAGService, we can just use get_rag_service directly in the router, 
# or alias it here for semantic clarity in the chat module.
def get_chat_rag_service(
    rag_service: RAGService = Depends(get_rag_service)
) -> RAGService:
    return rag_service
