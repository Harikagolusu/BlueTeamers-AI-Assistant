"""Conversation domain models for the Recent Conversations & Favorites system.

A conversation aggregates the messages of one chat thread together with rich
metadata (title, favorite/pinned flags, conversation type, related course/lesson,
assessment score, progress) so the UI can render Recent Conversations, Favorites,
filters, search and resume context without loading every message.
"""
from enum import Enum
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import uuid

from pydantic import BaseModel, Field, ConfigDict


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ConversationType(str, Enum):
    CHAT = "chat"
    ASSESSMENT = "assessment"
    LEARNING = "learning"
    INVESTIGATION = "investigation"
    TOOL = "tool"
    LAB = "lab"


class ConversationStatus(str, Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"  # future-ready


class ConversationMessage(BaseModel):
    message_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    role: MessageRole = MessageRole.USER
    content: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def turn(cls, role: MessageRole, content: str, **meta) -> "ConversationMessage":
        return cls(role=role, content=content, metadata=dict(meta or {}))


class ConversationSummary(BaseModel):
    """Lightweight projection used for list/search (never includes full body)."""

    conversation_id: str
    user_id: str
    title: str
    created_at: datetime
    updated_at: datetime
    last_message: str = ""
    message_count: int = 0
    favorite: bool = False
    pinned: bool = False
    archived: bool = False
    conversation_type: ConversationType = ConversationType.CHAT
    course_id: Optional[str] = None
    course_title: Optional[str] = None
    lesson_id: Optional[str] = None
    topic: Optional[str] = None
    progress: Optional[float] = None
    assessment_id: Optional[str] = None
    assessment_score: Optional[str] = None
    tags: List[str] = Field(default_factory=list)


class Conversation(ConversationSummary):
    """Full conversation record including the complete message history."""

    model_config = ConfigDict(arbitrary_types_allowed=True)
    messages: List[ConversationMessage] = Field(default_factory=list)

    def summarize(self) -> "ConversationSummary":
        return ConversationSummary(**self.model_dump(exclude={"messages"}))

    @property
    def last_message_preview(self) -> str:
        if self.messages:
            return self.messages[-1].content
        return self.last_message

    def preview(self, length: int = 120) -> str:
        text = self.last_message_preview or ""
        text = " ".join(text.split())
        return text[:length] + ("…" if len(text) > length else "")


class ConversationListPage(BaseModel):
    """Paginated result set for list/search (lazy loading friendly)."""

    items: List[ConversationSummary] = Field(default_factory=list)
    total: int = 0
    page: int = 1
    page_size: int = 20
    has_more: bool = False


class ConversationCreateRequest(BaseModel):
    first_message: Optional[str] = None
    conversation_type: ConversationType = ConversationType.CHAT
    course_id: Optional[str] = None
    course_title: Optional[str] = None
    lesson_id: Optional[str] = None
    topic: Optional[str] = None


class ConversationUpdateRequest(BaseModel):
    title: Optional[str] = None
    favorite: Optional[bool] = None
    pinned: Optional[bool] = None
    archived: Optional[bool] = None
    conversation_type: Optional[ConversationType] = None
    course_id: Optional[str] = None
    course_title: Optional[str] = None
    lesson_id: Optional[str] = None
    topic: Optional[str] = None
    progress: Optional[float] = None
    assessment_id: Optional[str] = None
    assessment_score: Optional[str] = None
    tags: Optional[List[str]] = None
