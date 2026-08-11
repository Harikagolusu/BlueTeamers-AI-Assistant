from pydantic import BaseModel, Field

class ToolVersion(BaseModel):
    tool_version: str = Field(default="1.0.0", description="Semantic version of the tool implementation")
    api_version: str = Field(default="v1", description="Target API version if applicable")
    schema_version: str = Field(default="1.0", description="Version of the input/output schemas")

    model_config = {"frozen": True}
