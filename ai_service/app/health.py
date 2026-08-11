from fastapi import APIRouter, Depends
from typing import Dict, Any

from app.core.config import settings
from app.rag.health import RAGHealthService
from app.rag.dependencies import get_rag_health_service
from app.chat.health import ChatHealthService
from app.chat.dependencies import get_chat_health_service
from app.memory.health import MemoryHealthService
from app.memory.dependencies import get_memory_health_service
from app.streaming.health import StreamingHealthService
from app.streaming.dependencies import get_streaming_health_service
from app.cache.health import CacheHealthService
from app.cache.dependencies import get_cache_health_service
from app.observability.service_health import ObservabilityHealthService
from app.observability.dependencies import get_observability_health_service
from app.guardrails.domain.services.guardrails_service import GuardrailsService
from app.guardrails.dependencies import get_guardrails_service

router = APIRouter(tags=["Health"])

@router.get("/", response_model=Dict[str, Any])
async def root():
    """
    Service information endpoint.
    """
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.APP_ENV,
        "status": "online",
        "docs_url": "/docs"
    }

@router.get("/health", response_model=Dict[str, Any])
async def aggregated_health(
    chat_health: ChatHealthService = Depends(get_chat_health_service),
    rag_health: RAGHealthService = Depends(get_rag_health_service),
    memory_health: MemoryHealthService = Depends(get_memory_health_service),
    streaming_health: StreamingHealthService = Depends(get_streaming_health_service),
    cache_health: CacheHealthService = Depends(get_cache_health_service),
    obs_health: ObservabilityHealthService = Depends(get_observability_health_service),
    guardrails_service: GuardrailsService = Depends(get_guardrails_service)
):
    """
    Aggregated health check endpoint for the entire application.
    """
    return await compute_aggregated_health(
        chat_health, rag_health, memory_health, streaming_health,
        cache_health, obs_health, guardrails_service
    )


async def compute_aggregated_health(
    chat_health: ChatHealthService,
    rag_health: RAGHealthService,
    memory_health: MemoryHealthService,
    streaming_health: StreamingHealthService,
    cache_health: CacheHealthService,
    obs_health: ObservabilityHealthService,
    guardrails_service: GuardrailsService,
) -> Dict[str, Any]:
    """Shared aggregated health computation (used by /health and /api/health)."""
    import asyncio
    import inspect

    _chat_coro = chat_health.check_health()
    _rag_coro = rag_health.check_health()
    _memory_coro = memory_health.check_health()
    _streaming_coro = streaming_health.check_health()
    _cache_coro = cache_health.check_health()
    _obs_coro = obs_health.get_health_status()
    _guardrails_coro = guardrails_service.get_health_status()

    async def ensure_awaitable(obj):
        return await obj if inspect.isawaitable(obj) else obj

    chat_status, rag_status, memory_status, streaming_status, cache_status, obs_status, guardrails_status = await asyncio.gather(
        ensure_awaitable(_chat_coro),
        ensure_awaitable(_rag_coro),
        ensure_awaitable(_memory_coro),
        ensure_awaitable(_streaming_coro),
        ensure_awaitable(_cache_coro),
        ensure_awaitable(_obs_coro),
        ensure_awaitable(_guardrails_coro)
    )

    overall_status = "healthy" if (
        chat_status.get("status") == "healthy" and
        rag_status.get("status") == "healthy" and
        memory_status.get("status") == "healthy" and
        streaming_status.get("status") == "healthy" and
        cache_status.get("status") == "healthy" and
        obs_status.get("metrics") == "healthy" and
        guardrails_status.get("status") in ("healthy", "disabled")
    ) else "degraded"

    return {
        "status": overall_status,
        "version": settings.APP_VERSION,
        "components": {
            "chat_api": chat_status,
            "rag_engine": rag_status,
            "memory": memory_status,
            "streaming": streaming_status,
            "cache": cache_status,
            "observability": obs_status,
            "guardrails": guardrails_status
        }
    }
