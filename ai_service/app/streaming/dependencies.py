from fastapi import Depends
from app.chat.dependencies import get_chat_rag_service
from app.rag.service import RAGService
from app.memory.dependencies import get_memory_service
from app.memory.memory_service import MemoryService
from app.cache.cache_service import CacheService
from app.cache.dependencies import get_cache_service
from app.streaming.streaming_service import StreamingService
from app.streaming.health import StreamingHealthService
from app.streaming.interfaces import BaseStreamingService
from app.observability.service import ObservabilityService
from app.observability.dependencies import get_observability_service

def get_streaming_service(
    rag_service: RAGService = Depends(get_chat_rag_service),
    memory_service: MemoryService = Depends(get_memory_service),
    cache_service: CacheService = Depends(get_cache_service),
    obs: ObservabilityService = Depends(get_observability_service)
) -> StreamingService:
    return StreamingService(
        rag_service=rag_service,
        memory_service=memory_service,
        cache_service=cache_service,
        obs=obs
    )

def get_streaming_health_service(
    service: BaseStreamingService = Depends(get_streaming_service)
) -> StreamingHealthService:
    return StreamingHealthService(service=service)
