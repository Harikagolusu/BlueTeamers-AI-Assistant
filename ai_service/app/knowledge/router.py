"""Admin/ops endpoints for static knowledge ingestion and status."""

import logging
from fastapi import APIRouter, Depends, HTTPException

from app.knowledge.dependencies import get_knowledge_pipeline
from app.knowledge.pipeline import KnowledgeIngestionPipeline
from app.knowledge.schemas import KnowledgeStatusResponse, KnowledgeIngestResponse
from app.knowledge.sources import load_lesson_content, load_course_catalog
from app.api.dependencies import require_internal_token

logger = logging.getLogger("app.knowledge.router")

router = APIRouter(prefix="/api/knowledge", tags=["Knowledge"])


@router.get("/status", response_model=KnowledgeStatusResponse)
async def knowledge_status(
    _auth: bool = Depends(require_internal_token),
    pipeline: KnowledgeIngestionPipeline = Depends(get_knowledge_pipeline),
):
    lessons = load_lesson_content()
    catalog = load_course_catalog()
    status = pipeline.status()
    return KnowledgeStatusResponse(
        vector_count=status["vector_count"],
        loaded=status["loaded"],
        lesson_count=sum(len(v) for v in lessons.values()),
        course_count=len(catalog),
        source_files={
            "lessons": str(len(lessons)) + " courses",
            "catalog": str(len(catalog)) + " courses",
        },
    )


@router.post("/ingest", response_model=KnowledgeIngestResponse)
async def knowledge_ingest(
    _auth: bool = Depends(require_internal_token),
    pipeline: KnowledgeIngestionPipeline = Depends(get_knowledge_pipeline),
):
    try:
        summary = pipeline.ingest()
        return KnowledgeIngestResponse(ingested=True, summary=summary)
    except Exception as e:
        logger.exception("Knowledge ingestion failed.")
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")
