from pydantic import BaseModel, Field
from typing import Dict, Any, List
from datetime import datetime

class DiagnosticSnapshot(BaseModel):
    snapshot_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    correlation_id: str
    trace_data: Dict[str, Any]
    logs: List[str]
    metrics: List[Any]
    timeline: List[Any]
    environment: Dict[str, str] = Field(default_factory=dict)
