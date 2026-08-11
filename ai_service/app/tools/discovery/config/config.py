from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class DiscoveryConfig(BaseSettings):
    tool_packages: List[str] = ["app.tools.concrete_tools"]
    excluded_packages: List[str] = []
    auto_register: bool = True
    include_experimental: bool = False
    allow_deprecated: bool = True
    
    model_config = SettingsConfigDict(env_prefix="DISCOVERY_")
