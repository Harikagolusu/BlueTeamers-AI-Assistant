from pydantic import Field
from typing import Dict, Any
from app.tools.domain.results.base_result import BaseResult

class EnvironmentResult(BaseResult):
    environment_variables: Dict[str, str] = Field(..., description="Safe environment variables")

class ConfigResult(BaseResult):
    config_values: Dict[str, Any] = Field(..., description="Configuration values for the section")

class PlatformResult(BaseResult):
    os_name: str = Field(..., description="Operating system name")
    python_version: str = Field(..., description="Python version")
    architecture: str = Field(..., description="System architecture")

class VersionResult(BaseResult):
    app_version: str = Field(..., description="Application version")
    api_version: str = Field(..., description="API version")
