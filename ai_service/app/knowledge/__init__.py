"""Knowledge ingestion package for the Hybrid Knowledge Architecture."""

import logging

from app.knowledge.pipeline import KnowledgeIngestionPipeline
from app.knowledge.sources import (
    load_lesson_content,
    load_course_catalog,
    build_all_static_documents,
    build_course_level_documents,
    build_lesson_documents,
    content_hash,
)

logger = logging.getLogger("app.knowledge")

__all__ = [
    "KnowledgeIngestionPipeline",
    "load_lesson_content",
    "load_course_catalog",
    "build_all_static_documents",
    "build_course_level_documents",
    "build_lesson_documents",
    "content_hash",
]