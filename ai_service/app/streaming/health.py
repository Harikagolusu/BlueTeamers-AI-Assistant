from app.streaming.interfaces import BaseStreamingService

class StreamingHealthService:
    def __init__(self, service: BaseStreamingService):
        self.service = service

    async def check_health(self) -> dict:
        try:
            return await self.service.health_check()
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
