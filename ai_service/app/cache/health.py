from typing import Dict, Any
from .cache_service import CacheService

class CacheHealthService:
    def __init__(self, cache_service: CacheService):
        self.cache_service = cache_service

    async def check_health(self) -> Dict[str, Any]:
        try:
            # Lightweight verification: can we access the store?
            if not self.cache_service.enabled:
                return {"status": "healthy", "message": "Cache is disabled"}
            
            # Simple exists check
            await self.cache_service.store.exists("healthcheck")
            
            # Simple read/write check
            from app.rag.schemas import RAGResponse, PipelineMetrics
            dummy_res = RAGResponse(query="health", answer="ok", citations=[], metrics=PipelineMetrics())
            await self.cache_service.store.set("health_test", dummy_res, ttl=1)
            await self.cache_service.store.get("health_test")
            await self.cache_service.store.delete("health_test")
            
            metrics = await self.cache_service.get_metrics()
            
            return {
                "status": "healthy",
                "backend": self.cache_service.store.__class__.__name__,
                "enabled": True,
                "metrics": metrics
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }
