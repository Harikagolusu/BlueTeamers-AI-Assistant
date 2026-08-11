from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime
import uuid

class AuditRecord(BaseModel):
    audit_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    principal: str
    correlation_id: str
    action: str
    resource: str
    result: str # "SUCCESS", "DENIED", "FAILED"
    risk_score: str = "LOW"
    metadata: Dict[str, Any] = Field(default_factory=dict)
