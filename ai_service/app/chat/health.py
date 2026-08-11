from app.rag.health import RAGHealthService

class ChatHealthService:
    """
    Aggregates health for the Chat API endpoints.
    Delegates to the RAGHealthService to verify underlying dependencies.
    Performs NO orchestration.
    """
    def __init__(self, rag_health: RAGHealthService):
        self.rag_health = rag_health

    async def check_health(self) -> dict:
        import inspect
        _rag_status = self.rag_health.check_health()
        rag_status = await _rag_status if inspect.isawaitable(_rag_status) else _rag_status
        
        status = "healthy" if rag_status.get("status") == "healthy" else "degraded"
        
        return {
            "status": status,
            "api_layer": "healthy",
            "dependencies": {
                "rag_engine": rag_status
            }
        }
