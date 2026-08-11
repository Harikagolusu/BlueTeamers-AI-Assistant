from pydantic import BaseModel, Field
from typing import Dict, Any
from datetime import datetime

class MetricRecord(BaseModel):
    name: str
    type: str # counter, gauge, histogram
    value: float
    tags: Dict[str, str] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
