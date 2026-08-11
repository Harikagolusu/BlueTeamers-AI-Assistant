from pydantic import Field
from app.tools.domain.schemas.base_schema import BaseSchema

class TimeSchema(BaseSchema):
    timezone: str = Field("UTC", description="Timezone (e.g., UTC, America/New_York)")
