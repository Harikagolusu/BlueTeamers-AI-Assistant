from pydantic import BaseModel
from typing import Optional
from app.guardrails.domain.models.enums import PolicyAction

class GuardrailResult(BaseModel):
    """Result of a guardrail policy evaluation."""
    action: PolicyAction
    reason: Optional[str] = None
    modified_text: Optional[str] = None
    
    @classmethod
    def allow(cls) -> "GuardrailResult":
        return cls(action=PolicyAction.ALLOW)

    @classmethod
    def warn(cls, reason: str, modified_text: Optional[str] = None) -> "GuardrailResult":
        return cls(action=PolicyAction.WARN, reason=reason, modified_text=modified_text)

    @classmethod
    def block(cls, reason: str) -> "GuardrailResult":
        return cls(action=PolicyAction.BLOCK, reason=reason)
