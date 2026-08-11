from pydantic import BaseModel, Field
from typing import Dict, Any, List
from datetime import datetime

class Token(BaseModel):
    token_id: str
    principal: str
    claims: Dict[str, Any] = Field(default_factory=dict)
    issued_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime
    is_revoked: bool = False
