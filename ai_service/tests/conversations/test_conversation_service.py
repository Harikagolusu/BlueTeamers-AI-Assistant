"""Tests for the ConversationService (Recent Conversations & Favorites)."""
import pytest

from app.conversations.events import ConversationEventPublisher
from app.conversations.models import ConversationType, ConversationUpdateRequest
from app.conversations.service import ConversationService
from app.conversations.store import SQLiteConversationStore


@pytest.fixture
def service(tmp_path):
    db = str(tmp_path / "test_conversations.db")
    store = SQLiteConversationStore(db_path=db)
    return ConversationService(store=store, events=ConversationEventPublisher(), max_title_len=60)


@pytest.mark.asyncio
async def test_create_conversation(service):
    convo = await service.create("user1")
    assert convo.conversation_id
    assert convo.user_id == "user1"
    assert convo.title == "New Conversation"


@pytest.mark.asyncio
async def test_record_turn_creates_and_auto_titles(service):
    convo = await service.record_turn(
        "user1", None, "What is Retrieval Augmented Generation?", "RAG is..."
    )
    assert "RAG" in convo.title or "Retrieval" in convo.title
    assert convo.message_count == 2
    assert convo.last_message == "RAG is..."
    assert convo.conversation_type == ConversationType.CHAT


@pytest.mark.asyncio
async def test_record_turn_appends_to_existing(service):
    convo = await service.record_turn("user1", None, "Explain SIEM", "SIEM is...")
    cid = convo.conversation_id
    convo2 = await service.record_turn("user1", cid, "How does SIEM work?", "It works by...")
    assert convo2.conversation_id == cid
    assert convo2.message_count == 4
    assert convo2.last_message == "It works by..."


@pytest.mark.asyncio
async def test_open_loads_full_history(service):
    convo = await service.record_turn("user1", None, "Explain SIEM", "SIEM is...")
    loaded = await service.open("user1", convo.conversation_id)
    assert loaded is not None
    assert len(loaded.messages) == 2
    assert loaded.messages[0].role.value == "user"
    assert loaded.messages[1].role.value == "assistant"


@pytest.mark.asyncio
async def test_rename(service):
    convo = await service.record_turn("user1", None, "Explain SIEM", "SIEM is...")
    renamed = await service.rename("user1", convo.conversation_id, "My SIEM Notes")
    assert renamed.title == "My SIEM Notes"


@pytest.mark.asyncio
async def test_rename_empty_raises(service):
    convo = await service.record_turn("user1", None, "Explain SIEM", "SIEM is...")
    with pytest.raises(ValueError):
        await service.rename("user1", convo.conversation_id, "   ")


@pytest.mark.asyncio
async def test_favorite_and_unfavorite(service):
    convo = await service.record_turn("user1", None, "Explain SIEM", "SIEM is...")
    fav = await service.set_favorite("user1", convo.conversation_id, True)
    assert fav.favorite is True
    unfav = await service.set_favorite("user1", convo.conversation_id, False)
    assert unfav.favorite is False


@pytest.mark.asyncio
async def test_delete(service):
    convo = await service.record_turn("user1", None, "Explain SIEM", "SIEM is...")
    ok = await service.delete("user1", convo.conversation_id)
    assert ok is True
    loaded = await service.get("user1", convo.conversation_id)
    assert loaded is None

@pytest.mark.asyncio
async def test_list_sorted_by_recent(service):
    c1 = await service.record_turn("user1", None, "Explain SIEM", "SIEM is...")
    c2 = await service.record_turn("user1", None, "Explain RAG", "RAG is...")
    page = await service.list("user1")
    assert page.total == 2
    assert page.items[0].conversation_id == c2.conversation_id
    assert page.items[1].conversation_id == c1.conversation_id


@pytest.mark.asyncio
async def test_list_favorites_filter(service):
    c1 = await service.record_turn("user1", None, "Explain SIEM", "SIEM is...")
    c2 = await service.record_turn("user1", None, "Explain RAG", "RAG is...")
    await service.set_favorite("user1", c1.conversation_id, True)
    page = await service.list("user1", filter="favorites")
    assert page.total == 1
    assert page.items[0].conversation_id == c1.conversation_id


@pytest.mark.asyncio
async def test_search(service):
    await service.record_turn("user1", None, "Explain SIEM correlation", "SIEM is...")
    await service.record_turn("user1", None, "What is RAG?", "RAG is...")
    page = await service.search("user1", "SIEM")
    assert page.total == 1


@pytest.mark.asyncio
async def test_search_messages_content(service):
    await service.record_turn("user1", None, "Question", "The answer mentions vector databases")
    page = await service.search("user1", "vector databases")
    assert page.total == 1


@pytest.mark.asyncio
async def test_user_isolation(service):
    await service.record_turn("user1", None, "Explain SIEM", "SIEM is...")
    await service.record_turn("user2", None, "Explain RAG", "RAG is...")
    p1 = await service.list("user1")
    p2 = await service.list("user2")
    assert p1.total == 1
    assert p2.total == 1
    c1 = (await service.list("user1")).items[0]
    assert await service.get("user2", c1.conversation_id) is None


@pytest.mark.asyncio
async def test_pagination(service):
    for i in range(5):
        await service.record_turn("user1", None, f"Question {i}", f"Answer {i}")
    page = await service.list("user1", page=1, page_size=2)
    assert len(page.items) == 2
    assert page.total == 5
    assert page.has_more is True
    page2 = await service.list("user1", page=3, page_size=2)
    assert len(page2.items) == 1
    assert page2.has_more is False


@pytest.mark.asyncio
async def test_update_metadata(service):
    convo = await service.record_turn("user1", None, "Explain SIEM", "SIEM is...")
    updated = await service.update("user1", convo.conversation_id, ConversationUpdateRequest(
        conversation_type=ConversationType.ASSESSMENT,
        course_id="siem-fundamentals",
        course_title="SIEM Fundamentals",
        assessment_score="8/10",
        pinned=True,
        tags=["siem", "quiz"],
    ))
    assert updated.conversation_type == ConversationType.ASSESSMENT
    assert updated.course_id == "siem-fundamentals"
    assert updated.assessment_score == "8/10"
    assert updated.pinned is True
    assert "siem" in updated.tags


@pytest.mark.asyncio
async def test_auto_title_from_course(service):
    convo = await service.record_turn(
        "user1", None, "What is this?", "It is...",
        metadata={"course_title": "AWS Cloud Practitioner"},
    )
    assert "AWS Cloud Practitioner" in convo.title


@pytest.mark.asyncio
async def test_no_duplicate_conversations(service):
    c1 = await service.record_turn("user1", None, "Explain SIEM", "SIEM is...")
    c2 = await service.record_turn("user1", c1.conversation_id, "More SIEM?", "Yes...")
    assert c1.conversation_id == c2.conversation_id
    page = await service.list("user1")
    assert page.total == 1


# --- Title generation unit tests ---

def test_title_rag():
    from app.conversations.title import generate_title
    assert "RAG" in generate_title("What is Retrieval Augmented Generation?")


def test_title_python():
    from app.conversations.title import generate_title
    assert "Python" in generate_title("How do I learn Python?")


def test_title_strips_question_words():
    from app.conversations.title import generate_title
    title = generate_title("Can you explain how DNS resolution works?")
    assert "dns" in title.lower() or "Dns" in title


def test_title_empty_message():
    from app.conversations.title import generate_title
    assert generate_title("") == "New Conversation"


def test_title_course_override():
    from app.conversations.title import generate_title
    assert "AWS Cloud Practitioner" in generate_title("What is this?", course_title="AWS Cloud Practitioner")


def test_title_clipped():
    from app.conversations.title import generate_title
    long_msg = "Explain " + "very " * 50 + "long topic"
    title = generate_title(long_msg, max_len=30)
    assert len(title) <= 30
