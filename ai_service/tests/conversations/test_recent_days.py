"""Tests for the Sprint 4 recent-conversations window (Feature 9)."""
import datetime

import pytest

from app.conversations.events import ConversationEventPublisher
from app.conversations.service import ConversationService
from app.conversations.store import SQLiteConversationStore


@pytest.fixture
def service(tmp_path):
    store = SQLiteConversationStore(db_path=str(tmp_path / "recent.db"))
    return ConversationService(store=store, events=ConversationEventPublisher())


async def _age(service, user_id, convo, days):
    convo.updated_at = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=days)
    await service.store.update(convo)


@pytest.mark.asyncio
async def test_recent_days_filter_excludes_old(service):
    fresh = await service.record_turn("user1", None, "Explain Wazuh", "ok")
    old = await service.record_turn("user1", None, "Explain Sigma", "ok")
    await _age(service, "user1", old, 30)

    page = await service.list("user1", days=7)
    assert page.total == 1
    assert page.items[0].conversation_id == fresh.conversation_id


@pytest.mark.asyncio
async def test_no_days_returns_all(service):
    await service.record_turn("user1", None, "Explain Wazuh", "ok")
    old = await service.record_turn("user1", None, "Explain Sigma", "ok")
    await _age(service, "user1", old, 30)

    page = await service.list("user1")
    assert page.total == 2


@pytest.mark.asyncio
async def test_days_combines_with_type_filter(service):
    await service.record_turn(
        "user1", None, "Explain Wazuh", "ok",
        metadata={"conversation_type": "learning"},
    )
    old = await service.record_turn(
        "user1", None, "Analyze this alert", "ok",
        metadata={"conversation_type": "investigation"},
    )
    await _age(service, "user1", old, 30)

    page = await service.list("user1", filter="learning", days=7)
    assert page.total == 1
