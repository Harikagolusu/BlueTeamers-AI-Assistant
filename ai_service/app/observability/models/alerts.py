from pydantic import BaseModel, Field
from typing import Dict, Any
from datetime import datetime

class Alert(BaseModel):
    alert_id: str
    rule_name: str
    severity: str # INFO, LOW, MEDIUM, HIGH, CRITICAL
    message: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    resolved: bool = False
