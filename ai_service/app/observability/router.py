from fastapi import APIRouter, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from app.core.config import settings

router = APIRouter()

@router.get(settings.METRICS_ENDPOINT, tags=["Observability"])
async def metrics():
    """
    Exposes Prometheus metrics.
    """
    if not settings.METRICS_ENABLED:
        return Response(status_code=404, content="Metrics disabled")
    
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
