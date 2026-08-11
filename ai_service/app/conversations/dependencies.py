"""Dependency injection for the conversations subsystem."""
from app.core.config import settings
from app.conversations.events import ConversationEventPublisher
from app.conversations.service import ConversationService
from app.conversations.store import SQLiteConversationStore

# Singleton store + service (durable SQLite-backed, restart-safe).
_store_instance = SQLiteConversationStore(db_path=settings.CONVERSATIONS_DB_PATH)
_service_instance = ConversationService(
    store=_store_instance,
    events=ConversationEventPublisher(),
    max_title_len=settings.CONVERSATION_TITLE_MAX_LEN,
    default_page_size=settings.CONVERSATIONS_PAGE_SIZE,
)


def get_conversation_store() -> SQLiteConversationStore:
    return _store_instance


def get_conversation_service() -> ConversationService:
    return _service_instance
