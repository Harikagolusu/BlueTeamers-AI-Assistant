from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime, timezone
from enum import Enum
import uuid

class SessionState(str, Enum):
    INITIALIZING = "initializing"
    ACTIVE = "active"
    IDLE = "idle"
    CLOSED = "closed"
    ERROR = "error"

class MCPSession(BaseModel):
    session_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    server_name: str
    state: SessionState = SessionState.INITIALIZING
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_active: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    def update_activity(self):
        self.last_active = datetime.now(timezone.utc)
