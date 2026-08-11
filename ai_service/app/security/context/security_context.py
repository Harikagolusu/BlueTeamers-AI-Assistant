from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
import uuid

class SecurityContext(BaseModel):
    principal: str
    user: str = "anonymous"
    roles: List[str] = Field(default_factory=list)
    permissions: List[str] = Field(default_factory=list)
    tenant: str = "default"
    organization: Optional[str] = None
    session: Optional[str] = None
    auth_method: str = "none"
    token_metadata: Dict[str, Any] = Field(default_factory=dict)
    correlation_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))

    @classmethod
    def anonymous(cls):
        return cls(principal="anonymous")
