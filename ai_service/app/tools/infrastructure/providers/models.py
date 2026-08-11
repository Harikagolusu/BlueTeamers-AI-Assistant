from enum import Enum
from pydantic import BaseModel
from datetime import datetime

class ProviderStatus(str, Enum):
    CONNECTED = "CONNECTED"
    DEGRADED = "DEGRADED"
    UNAVAILABLE = "UNAVAILABLE"

class ProviderHealth(BaseModel):
    status: ProviderStatus
    latency_ms: float
    version: str
    provider_name: str
    last_checked: datetime
    error_message: str | None = None
