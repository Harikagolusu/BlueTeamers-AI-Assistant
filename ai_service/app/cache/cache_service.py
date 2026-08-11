import hashlib
import json
import logging
from typing import Optional, Dict, Any
import time

from app.rag.schemas import RAGRequest, RAGResponse
from app.observability.service import ObservabilityService
from .interfaces import BaseCacheStore

logger = logging.getLogger("app.cache.service")

class CacheService:
    def __init__(
        self, 
        store: BaseCacheStore, 
        enabled: bool, 
        ttl: int,
        cache_version: str = "v1",
        model_name: str = "auto",
        prompt_template_version: str = "v1",
        obs: Optional[ObservabilityService] = None
    ):
        self.store = store
        self.enabled = enabled
        self.ttl = ttl
        self.cache_version = cache_version
        self.model_name = model_name
        self.prompt_template_version = prompt_template_version
        self.obs = obs

    def generate_key(self, request: RAGRequest) -> str:
        """
        Generate deterministic hashed cache key based on query, filters, top_k, and template.
        """
        key_dict = {
            "query": request.query,
            "filters": request.metadata_filters,
            "top_k": request.top_k,
            "template": request.template_name,
            "cache_version": self.cache_version,
            "model_name": self.model_name,
            "prompt_template_version": self.prompt_template_version
        }
        key_str = json.dumps(key_dict, sort_keys=True)
        return hashlib.sha256(key_str.encode("utf-8")).hexdigest()

    async def get_cached_response(self, request: RAGRequest) -> Optional[RAGResponse]:
        if not self.enabled:
            return None
            
        start_time = time.time()
        key = self.generate_key(request)
        response = await self.store.get(key)
        
        if self.obs:
            self.obs.observe_histogram("cache_lookup_latency_seconds", time.time() - start_time, {"cache_backend": "in_memory"})
        
        if response:
            logger.info(f"Cache HIT for key: {key}")
            if self.obs:
                self.obs.increment_counter("cache_hits_total", 1.0, {"cache_backend": "in_memory"})
        else:
            logger.info(f"Cache MISS for key: {key}")
            if self.obs:
                self.obs.increment_counter("cache_misses_total", 1.0, {"cache_backend": "in_memory"})
            
        return response

    async def set_cached_response(self, request: RAGRequest, response: RAGResponse) -> None:
        if not self.enabled:
            return
            
        key = self.generate_key(request)
        await self.store.set(key, response, self.ttl)
        logger.info(f"Cache SET for key: {key} (TTL: {self.ttl}s)")

    async def get_metrics(self) -> Dict[str, Any]:
        return await self.store.get_metrics()

    async def clear(self) -> None:
        await self.store.clear()
        
    async def delete(self, request: RAGRequest) -> None:
        key = self.generate_key(request)
        await self.store.delete(key)
