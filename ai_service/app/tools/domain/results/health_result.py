from pydantic import Field
from typing import Dict
from app.tools.domain.results.base_result import BaseResult

class HealthResult(BaseResult):
    status: str = Field(..., description="Overall health status (healthy, degraded, down)")
    components: Dict[str, str] = Field(default_factory=dict, description="Component level health")
