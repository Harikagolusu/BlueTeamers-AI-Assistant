from pydantic import Field
from typing import List
from app.tools.domain.results.base_result import BaseResult
from app.tools.domain.models.search_models import SearchDocument

class VectorSearchResult(BaseResult):
    documents: List[SearchDocument] = Field(..., description="Top matching documents")

class DocumentSearchResult(BaseResult):
    documents: List[SearchDocument] = Field(..., description="Top matching documents")

class SemanticSearchResult(BaseResult):
    documents: List[SearchDocument] = Field(..., description="Top matching documents")
