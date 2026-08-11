from app.indexing.schemas import HealthResponse
from app.indexing.service import IndexingService

def get_indexing_health(service: IndexingService) -> HealthResponse:
    return service.health_check()
