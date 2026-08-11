"""Conversation lifecycle events published onto the shared agent event bus.

These events allow other subsystems (observability, analytics, audit) to react to
conversation lifecycle changes without coupling to the conversation service.
"""
from typing import Any, Dict, Optional

from app.agents.events.agent_events import AgentEvent
from app.agents.events.event_bus import agent_event_bus


class ConversationCreatedEvent(AgentEvent):
    type: str = "ConversationCreated"
    conversation_id: Optional[str] = None
    title: str = ""


class ConversationOpenedEvent(AgentEvent):
    type: str = "ConversationOpened"
    conversation_id: Optional[str] = None


class ConversationUpdatedEvent(AgentEvent):
    type: str = "ConversationUpdated"
    conversation_id: Optional[str] = None
    message_count: int = 0


class ConversationDeletedEvent(AgentEvent):
    type: str = "ConversationDeleted"
    conversation_id: Optional[str] = None


class ConversationFavoritedEvent(AgentEvent):
    type: str = "ConversationFavorited"
    conversation_id: Optional[str] = None


class ConversationUnfavoritedEvent(AgentEvent):
    type: str = "ConversationUnfavorited"
    conversation_id: Optional[str] = None


class ConversationRenamedEvent(AgentEvent):
    type: str = "ConversationRenamed"
    conversation_id: Optional[str] = None
    title: str = ""


class ConversationEventPublisher:
    """Publishes conversation lifecycle events onto the shared agent event bus."""

    def __init__(self, bus=None):
        self._bus = bus or agent_event_bus

    def _publish(self, event: AgentEvent) -> None:
        try:
            self._bus.publish(event)
        except Exception:  # never break the request on an event-bus failure
            pass

    def created(self, conversation_id: str, user_id: str, title: str) -> None:
        self._publish(
            ConversationCreatedEvent(
                session_id=user_id or "anonymous",
                conversation_id=conversation_id,
                title=title,
            )
        )

    def opened(self, conversation_id: str, user_id: str) -> None:
        self._publish(
            ConversationOpenedEvent(
                session_id=user_id or "anonymous",
                conversation_id=conversation_id,
            )
        )

    def updated(self, conversation_id: str, user_id: str, message_count: int) -> None:
        self._publish(
            ConversationUpdatedEvent(
                session_id=user_id or "anonymous",
                conversation_id=conversation_id,
                message_count=message_count,
            )
        )

    def deleted(self, conversation_id: str, user_id: str) -> None:
        self._publish(
            ConversationDeletedEvent(
                session_id=user_id or "anonymous",
                conversation_id=conversation_id,
            )
        )

    def favorited(self, conversation_id: str, user_id: str) -> None:
        self._publish(
            ConversationFavoritedEvent(
                session_id=user_id or "anonymous",
                conversation_id=conversation_id,
            )
        )

    def unfavorited(self, conversation_id: str, user_id: str) -> None:
        self._publish(
            ConversationUnfavoritedEvent(
                session_id=user_id or "anonymous",
                conversation_id=conversation_id,
            )
        )

    def renamed(self, conversation_id: str, user_id: str, title: str) -> None:
        self._publish(
            ConversationRenamedEvent(
                session_id=user_id or "anonymous",
                conversation_id=conversation_id,
                title=title,
            )
        )
