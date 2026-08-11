from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class ToolConfig(BaseSettings):
    """
    Configuration for the Tool Calling Framework.
    Values can be overridden using environment variables prefixed with AI_SERVICE_.
    """
    TOOL_GLOBAL_EXECUTION_TIMEOUT_SEC: int = Field(default=30, gt=0, le=600)
    TOOL_DEFAULT_CACHE_TTL_SEC: int = Field(default=3600, gt=0)
    TOOL_REGISTRY_STRICT_MODE: bool = True
    
    model_config = SettingsConfigDict(env_prefix="AI_SERVICE_")

tool_config = ToolConfig()
