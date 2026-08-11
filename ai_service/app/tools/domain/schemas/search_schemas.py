from pydantic import Field
from app.tools.domain.schemas.base_schema import BaseSchema

class VectorSearchSchema(BaseSchema):
    query: str = Field(..., description="Natural language search query")
    limit: int = Field(5, description="Maximum number of results to return")

class DocumentSearchSchema(BaseSchema):
    keyword: str = Field(..., description="Keyword to search for")
    limit: int = Field(5, description="Maximum number of results")

class SemanticSearchSchema(BaseSchema):
    query: str = Field(..., description="Natural language search query")
    limit: int = Field(5, description="Maximum number of results")
