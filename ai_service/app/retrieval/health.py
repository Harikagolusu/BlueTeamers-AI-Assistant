from app.retrieval.schemas import HealthResponse
from app.retrieval.service import RetrievalService

def get_retrieval_health(service: RetrievalService) -> HealthResponse:
    return service.health_check()
