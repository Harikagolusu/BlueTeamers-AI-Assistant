from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional
import datetime
import uuid

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class MemoryMessage(BaseModel):
    role: MessageRole
    content: str
    timestamp: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))

class ConversationSession(BaseModel):
    session_id: str
    created_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))
    messages: List[MemoryMessage] = Field(default_factory=list)
