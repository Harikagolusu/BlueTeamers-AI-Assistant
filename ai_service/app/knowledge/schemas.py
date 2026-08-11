from pydantic import BaseModel
from typing import Dict, Any, List


class KnowledgeStatusResponse(BaseModel):
    vector_count: int
    loaded: bool
    lesson_count: int
    course_count: int
    source_files: Dict[str, str]


class KnowledgeIngestResponse(BaseModel):
    ingested: bool
    summary: Dict[str, Any]