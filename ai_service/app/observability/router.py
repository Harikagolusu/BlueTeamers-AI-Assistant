from fastapi import APIRouter, Depends, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from app.api.dependencies import require_internal_token
from app.core.config import settings

router = APIRouter()

@router.get(settings.METRICS_ENDPOINT, tags=["Observability"])
async def metrics(_auth: bool = Depends(require_internal_token)):
    """
    Exposes Prometheus metrics.

    Protected by the internal admin token (audit B-04): operational metrics
    are not world-readable. Development mode short-circuits the token check
    (see ``require_internal_token``) so local tooling keeps working.
    """
    if not settings.METRICS_ENABLED:
        return Response(status_code=404, content="Metrics disabled")
    
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
