import asyncio
from typing import Optional, OrderedDict, Dict, Any
import collections
import time
from app.rag.schemas import RAGResponse
from .interfaces import BaseCacheStore

class InMemoryCacheStore(BaseCacheStore):
    def __init__(self, max_size: int):
        self.max_size = max_size
        self._cache: collections.OrderedDict[str, tuple[RAGResponse, float]] = collections.OrderedDict()
        self._lock = asyncio.Lock()
        
        # Metrics
        self._hits = 0
        self._misses = 0
        self._evictions = 0
        self._expired = 0

    async def get(self, key: str) -> Optional[RAGResponse]:
        async with self._lock:
            if key in self._cache:
                value, expires_at = self._cache[key]
                if time.time() > expires_at:
                    del self._cache[key]
                    self._expired += 1
                    self._misses += 1
                    return None
                self._cache.move_to_end(key)
                self._hits += 1
                return value
            self._misses += 1
            return None

    async def set(self, key: str, value: RAGResponse, ttl: int) -> None:
        async with self._lock:
            if key in self._cache:
                del self._cache[key]
            elif len(self._cache) >= self.max_size:
                # LRU Eviction
                self._cache.popitem(last=False)
                self._evictions += 1
            
            expires_at = time.time() + ttl
            self._cache[key] = (value, expires_at)

    async def delete(self, key: str) -> None:
        async with self._lock:
            if key in self._cache:
                del self._cache[key]

    async def exists(self, key: str) -> bool:
        async with self._lock:
            if key in self._cache:
                _, expires_at = self._cache[key]
                if time.time() > expires_at:
                    del self._cache[key]
                    self._expired += 1
                    return False
                return True
            return False

    async def clear(self) -> None:
        async with self._lock:
            self._cache.clear()
            self._hits = 0
            self._misses = 0
            self._evictions = 0
            self._expired = 0

    async def get_metrics(self) -> Dict[str, Any]:
        async with self._lock:
            total_requests = self._hits + self._misses
            hit_ratio = (self._hits / total_requests) if total_requests > 0 else 0.0
            return {
                "cache_hits": self._hits,
                "cache_misses": self._misses,
                "cache_evictions": self._evictions,
                "expired_entries": self._expired,
                "current_cache_size": len(self._cache),
                "hit_ratio": hit_ratio
            }
