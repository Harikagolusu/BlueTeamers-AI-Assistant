from pydantic import BaseModel, Field
from typing import Optional
import uuid
from datetime import datetime

class ObservabilityContext(BaseModel):
    correlation_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    trace_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    span_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    parent_span_id: Optional[str] = None
    request_id: Optional[str] = None
    start_time: datetime = Field(default_factory=datetime.utcnow)
    tenant: str = "default"
    user: str = "anonymous"
    current_component: Optional[str] = None
    current_module: Optional[str] = None

    @classmethod
    def create_empty(cls):
        return cls()
