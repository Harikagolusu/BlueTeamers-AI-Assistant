from typing import Optional
from app.cache.interfaces import ICacheService, BaseCacheStore

class DefaultCacheManager(ICacheService):
    """
    Adapter implementing ICacheService, wrapping a BaseCacheStore to store 
    and retrieve semantic chat cache entries.
    """
    def __init__(self, store: BaseCacheStore):
        self._store = store

    async def get(self, key: str) -> Optional[str]:
        val = await self._store.get(key)
        if val is None:
            return None
        if hasattr(val, "answer"):
            return val.answer
        return str(val)

    async def set(self, key: str, value: str, ttl: int = 3600) -> None:
        await self._store.set(key, value, ttl)
