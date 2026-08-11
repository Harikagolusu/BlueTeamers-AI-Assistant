from pydantic import Field
from app.tools.domain.results.base_result import BaseResult

class ConnectivityResult(BaseResult):
    reachable: bool = Field(..., description="True if host is reachable")
    latency_ms: float = Field(0.0, description="Latency in milliseconds")
