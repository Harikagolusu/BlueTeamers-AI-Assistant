from fastapi import Depends
from app.core.config import settings
from .interfaces import BaseCacheStore
from .cache_store import InMemoryCacheStore
from .cache_service import CacheService
from .health import CacheHealthService

def get_cache_store() -> BaseCacheStore:
    # In the future, branch here if settings.CACHE_BACKEND == "redis"
    return InMemoryCacheStore(max_size=settings.CACHE_MAX_SIZE)

from app.observability.service import ObservabilityService
from app.observability.dependencies import get_observability_service

def get_cache_service(
    store: BaseCacheStore = Depends(get_cache_store),
    obs: ObservabilityService = Depends(get_observability_service)
) -> CacheService:
    return CacheService(
        store=store,
        enabled=settings.CACHE_ENABLED,
        ttl=settings.CACHE_TTL,
        cache_version=settings.CACHE_VERSION,
        model_name=settings.LLM_PROVIDER,
        prompt_template_version="v1", # This could be extracted from settings later if we version prompts
        obs=obs
    )

def get_cache_health_service(
    cache_service: CacheService = Depends(get_cache_service)
) -> CacheHealthService:
    return CacheHealthService(cache_service)
