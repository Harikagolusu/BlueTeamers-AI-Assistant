from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class GuardrailContext(BaseModel):
    """Context passed through the guardrails pipeline."""
    text: str
    trace_id: str
    request_id: str
    tenant_id: Optional[str] = None
    user_id: Optional[str] = None
    client_application: Optional[str] = None
    environment: str = "production"
    is_audit_mode: bool = False
    metadata: Dict[str, Any] = Field(default_factory=dict)
