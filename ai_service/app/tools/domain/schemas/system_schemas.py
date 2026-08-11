from pydantic import Field
from app.tools.domain.schemas.base_schema import BaseSchema

class EnvironmentSchema(BaseSchema):
    keys: list[str] = Field(default_factory=list, description="Specific env vars to read. Empty for all safe vars.")

class ConfigSchema(BaseSchema):
    section: str = Field(..., description="Configuration section to inspect (e.g., 'database', 'security')")

class PlatformSchema(BaseSchema):
    pass # No input needed for platform details

class VersionSchema(BaseSchema):
    pass # No input needed for version info
