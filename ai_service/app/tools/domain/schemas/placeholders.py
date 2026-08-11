from app.tools.domain.schemas.base_schema import BaseSchema
from pydantic import Field

class CalculatorSchema(BaseSchema):
    expression: str = Field(..., description="Math expression to evaluate")

class SearchSchema(BaseSchema):
    query: str = Field(..., description="The query string to search for")
    limit: int = Field(10, description="Max results")

class HashSchema(BaseSchema):
    data: str = Field(..., description="Data to hash")
    algorithm: str = Field("sha256", description="Hashing algorithm")

class TimeSchema(BaseSchema):
    timezone: str = Field("UTC", description="Timezone name")
