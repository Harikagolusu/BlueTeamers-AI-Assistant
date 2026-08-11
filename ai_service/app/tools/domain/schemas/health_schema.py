from pydantic import Field
from app.tools.domain.schemas.base_schema import BaseSchema

class HealthSchema(BaseSchema):
    component: str = Field("all", description="Specific component to check, or 'all'")
