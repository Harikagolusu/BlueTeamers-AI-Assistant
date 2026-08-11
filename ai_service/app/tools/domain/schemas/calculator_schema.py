from pydantic import Field
from app.tools.domain.schemas.base_schema import BaseSchema

class CalculatorSchema(BaseSchema):
    expression: str = Field(..., description="Math expression to evaluate")
