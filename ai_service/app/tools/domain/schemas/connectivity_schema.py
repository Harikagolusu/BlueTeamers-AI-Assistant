from pydantic import Field
from app.tools.domain.schemas.base_schema import BaseSchema

class ConnectivitySchema(BaseSchema):
    host: str = Field(..., description="Hostname or IP to check")
    port: int = Field(80, description="Port to check")
