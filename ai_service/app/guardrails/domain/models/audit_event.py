from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime, timezone
from app.guardrails.domain.models.enums import PolicyAction

class AuditEvent(BaseModel):
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    trace_id: str
    request_id: str
    policy_name: str
    policy_group: str
    policy_version: str
    execution_time_ms: float
    decision: PolicyAction
    severity: str
    reason: Optional[str] = None
    user_id: Optional[str] = None
    tenant_id: Optional[str] = None
    client_application: Optional[str] = None
    environment: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
