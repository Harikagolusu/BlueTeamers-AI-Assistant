from app.memory.interfaces import BaseMemoryStore

class MemoryHealthService:
    """
    Health check aggregator for the memory module.
    """
    def __init__(self, store: BaseMemoryStore, enabled: bool):
        self.store = store
        self.enabled = enabled

    async def check_health(self) -> dict:
        if not self.enabled:
            return {
                "status": "healthy",
                "enabled": False,
                "message": "Memory module is disabled via configuration"
            }
            
        try:
            store_health = await self.store.health_check()
            return {
                "status": "healthy" if store_health.get("status") == "healthy" else "degraded",
                "enabled": True,
                "store": store_health
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
