"""ConversationService: business logic for Recent Conversations & Favorites.

Owns CRUD, auto-titling, metadata updates, favorite/pin/rename/delete, paginated
listing, search, and resume. Emits lifecycle events via ConversationEventPublisher.
"""
import datetime
import logging
from typing import Any, Dict, List, Optional

from app.conversations.events import ConversationEventPublisher
from app.conversations.models import (
    Conversation,
    ConversationCreateRequest,
    ConversationListPage,
    ConversationMessage,
    ConversationType,
    ConversationUpdateRequest,
    MessageRole,
)
from app.conversations.store import SQLiteConversationStore
from app.conversations.title import (
    generate_title,
    is_greeting_message,
    is_placeholder_title,
    is_greeting_title,
)

logger = logging.getLogger("app.conversations.service")


def _now() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)


class ConversationService:
    def __init__(
        self,
        store: SQLiteConversationStore,
        events: Optional[ConversationEventPublisher] = None,
        max_title_len: int = 60,
        default_page_size: int = 20,
    ):
        self.store = store
        self.events = events or ConversationEventPublisher()
        self.max_title_len = max_title_len
        self.default_page_size = default_page_size

    # ------------------------------------------------------------------ create/record
    async def create(
        self, user_id: str, request: Optional[ConversationCreateRequest] = None
    ) -> Conversation:
        request = request or ConversationCreateRequest()
        conversation_id = _new_id()
        now = _now()
        convo = Conversation(
            conversation_id=conversation_id,
            user_id=user_id,
            title=self._auto_title(request.first_message, request.course_title),
            created_at=now,
            updated_at=now,
            conversation_type=request.conversation_type,
            course_id=request.course_id,
            course_title=request.course_title,
            lesson_id=request.lesson_id,
            topic=request.topic,
        )
        await self.store.create(convo)
        self.events.created(conversation_id, user_id, convo.title)
        return convo

    async def record_turn(
        self,
        user_id: str,
        conversation_id: Optional[str],
        user_message: str,
        ai_message: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Conversation:
        """Append one user+assistant turn. Creates the conversation if absent."""
        meta = metadata or {}
        convo = None
        if conversation_id:
            convo = await self.store.get(conversation_id, user_id)

        is_new = convo is None
        if convo is None:
            convo = Conversation(
                conversation_id=conversation_id or _new_id(),
                user_id=user_id,
                title=self._auto_title(user_message, meta.get("course_title"), meta.get("topic")),
                created_at=_now(),
                updated_at=_now(),
                conversation_type=_coerce_type(meta.get("conversation_type")),
                course_id=meta.get("course_id"),
                course_title=meta.get("course_title"),
                lesson_id=meta.get("lesson_id"),
                topic=meta.get("topic") or _extract_topic(user_message),
                progress=meta.get("progress"),
                assessment_id=meta.get("assessment_id"),
                assessment_score=meta.get("assessment_score"),
            )

        convo.messages.append(ConversationMessage.turn(MessageRole.USER, user_message, **meta))
        if ai_message:
            convo.messages.append(ConversationMessage.turn(MessageRole.ASSISTANT, ai_message))
        convo.message_count = len(convo.messages)
        convo.last_message = ai_message or user_message
        convo.updated_at = _now()

        # Title policy (smart titles):
        #   - A brand-new conversation is titled from its first user message.
        #     Greeting-only openers ("Hi", "Hello") get the "New Chat"
        #     placeholder instead of a useless "About Hi".
        #   - A conversation still carrying a placeholder title (or a legacy
        #     greeting title like "About Hi") is re-titled the moment the first
        #     meaningful question arrives. Manual renames are never overwritten.
        if is_new:
            convo.title = self._auto_title(
                user_message, convo.course_title, meta.get("topic")
            )
        elif (
            is_placeholder_title(convo.title) or is_greeting_title(convo.title)
        ) and not is_greeting_message(user_message):
            convo.title = self._auto_title(
                user_message, convo.course_title, meta.get("topic")
            )

        if meta.get("course_id"):
            convo.course_id = meta["course_id"]
        if meta.get("course_title"):
            convo.course_title = meta["course_title"]
        if meta.get("lesson_id"):
            convo.lesson_id = meta["lesson_id"]
        if meta.get("topic"):
            convo.topic = meta["topic"]
        if meta.get("progress") is not None:
            convo.progress = meta["progress"]
        if meta.get("assessment_id"):
            convo.assessment_id = meta["assessment_id"]
        if meta.get("assessment_score"):
            convo.assessment_score = meta["assessment_score"]
        if meta.get("conversation_type"):
            convo.conversation_type = _coerce_type(meta["conversation_type"])
        if meta.get("tags"):
            convo.tags = _merge(convo.tags, meta["tags"])

        if is_new:
            await self.store.create(convo)
            self.events.created(convo.conversation_id, user_id, convo.title)
        else:
            await self.store.update(convo)
        self.events.updated(convo.conversation_id, user_id, convo.message_count)
        return convo

    # ------------------------------------------------------------------ reads
    async def get(self, user_id: str, conversation_id: str) -> Optional[Conversation]:
        return await self.store.get(conversation_id, user_id)

    async def open(self, user_id: str, conversation_id: str) -> Optional[Conversation]:
        convo = await self.store.get(conversation_id, user_id)
        if convo:
            self.events.opened(conversation_id, user_id)
        return convo

    async def list(
        self,
        user_id: str,
        *,
        filter: Optional[str] = None,
        search: Optional[str] = None,
        page: int = 1,
        page_size: Optional[int] = None,
        days: Optional[int] = None,
    ) -> ConversationListPage:
        page_size = page_size or self.default_page_size
        conv_type, favorite_only = _parse_filter(filter)
        items, total = await self.store.list(
            user_id,
            conversation_type=conv_type,
            favorite_only=favorite_only,
            search=search or None,
            page=page,
            page_size=page_size,
            days=days,
        )
        return ConversationListPage(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            has_more=(page * page_size) < total,
        )

    async def search(
        self,
        user_id: str,
        query: str,
        page: int = 1,
        page_size: Optional[int] = None,
    ) -> ConversationListPage:
        return await self.list(user_id, search=query, page=page, page_size=page_size)

    # ------------------------------------------------------------------ updates
    async def rename(self, user_id: str, conversation_id: str, title: str) -> Optional[Conversation]:
        title = (title or "").strip()
        if not title:
            raise ValueError("Title cannot be empty")
        convo = await self.store.get(conversation_id, user_id)
        if not convo:
            return None
        convo.title = title[: self.max_title_len]
        convo.updated_at = _now()
        await self.store.update(convo)
        self.events.renamed(conversation_id, user_id, convo.title)
        return convo

    async def update(
        self, user_id: str, conversation_id: str, request: ConversationUpdateRequest
    ) -> Optional[Conversation]:
        convo = await self.store.get(conversation_id, user_id)
        if not convo:
            return None
        data = request.model_dump(exclude_unset=True)

        if "title" in data and data["title"] is not None:
            title = str(data["title"]).strip()
            if not title:
                raise ValueError("Title cannot be empty")
            convo.title = title[: self.max_title_len]
            self.events.renamed(conversation_id, user_id, convo.title)

        if "favorite" in data:
            convo.favorite = bool(data["favorite"])
            if convo.favorite:
                self.events.favorited(conversation_id, user_id)
            else:
                self.events.unfavorited(conversation_id, user_id)
        if "pinned" in data:
            convo.pinned = bool(data["pinned"])
        if "archived" in data:
            convo.archived = bool(data["archived"])
        if "conversation_type" in data and data["conversation_type"] is not None:
            convo.conversation_type = _coerce_type(data["conversation_type"])
        for attr in (
            "course_id", "course_title", "lesson_id", "topic", "assessment_id",
            "assessment_score", "progress",
        ):
            if attr in data and data[attr] is not None:
                setattr(convo, attr, data[attr])
        if "tags" in data and data["tags"] is not None:
            convo.tags = list(dict.fromkeys(t for t in data["tags"] if t))

        convo.updated_at = _now()
        await self.store.update(convo)
        return convo

    async def set_favorite(
        self, user_id: str, conversation_id: str, favorite: bool
    ) -> Optional[Conversation]:
        return await self.update(
            user_id,
            conversation_id,
            ConversationUpdateRequest(favorite=favorite),
        )

    async def delete(self, user_id: str, conversation_id: str) -> bool:
        ok = await self.store.delete(conversation_id, user_id)
        if ok:
            self.events.deleted(conversation_id, user_id)
        return ok

    # ------------------------------------------------------------------ helpers
    def _auto_title(self, first_message, course_title=None, topic=None) -> str:
        return generate_title(
            first_message or topic or "",
            course_title=course_title,
            max_len=self.max_title_len,
        )


def _new_id() -> str:
    import uuid
    return str(uuid.uuid4())


def _coerce_type(value: Any) -> ConversationType:
    if isinstance(value, ConversationType):
        return value
    try:
        return ConversationType(str(value).lower())
    except ValueError:
        return ConversationType.CHAT


def _extract_topic(message: str) -> str:
    text = (message or "").strip()
    words = [w for w in text.split() if len(w) > 3]
    return " ".join(words[:4])[:60] if words else (text[:60] or "general")


def _merge(existing: List[str], incoming: Any) -> List[str]:
    out = list(existing)
    for tag in (incoming if isinstance(incoming, (list, tuple)) else [incoming]):
        t = str(tag).strip()
        if t and t not in out:
            out.append(t)
    return out


def _parse_filter(filter: Optional[str]):
    """Map UI filter names to (ConversationType|None, favorite_only|None)."""
    if not filter:
        return None, None
    f = filter.lower().strip()
    if f == "favorites":
        return None, True
    if f == "all":
        return None, None
    if f in ("recent", "all_conversations", "all conversations"):
        return None, None
    try:
        return ConversationType(f), None
    except ValueError:
        return None, None

