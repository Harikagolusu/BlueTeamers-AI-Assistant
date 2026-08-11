"""Tests for SessionMemoryManager (Sprint 4 features 6-8, 12, 13)."""
import pytest

from app.adaptive.session_memory import (
    MAX_FACTS,
    MAX_ROLLING_MESSAGES,
    SessionMemoryManager,
)
from app.adaptive.store import SQLiteLearnerStore


@pytest.fixture
def memory(tmp_path):
    return SessionMemoryManager(SQLiteLearnerStore(db_path=str(tmp_path / "memory.db")))


@pytest.mark.asyncio
async def test_rolling_context_capped(memory):
    for i in range(10):
        await memory.record_turn("u1", "conv1", f"q{i}", f"a{i}")
    state = await memory.load("u1", "conv1")
    assert len(state.rolling_messages) <= MAX_ROLLING_MESSAGES


@pytest.mark.asyncio
async def test_facts_deduplicated_and_capped(memory):
    for i in range(12):
        await memory.record_turn("u1", "conv1", f"Explain Wazuh agent {i}", f"ok {i}")
    state = await memory.load("u1", "conv1")
    assert len(state.facts) <= MAX_FACTS
    assert len(state.facts) == len(set(state.facts))


@pytest.mark.asyncio
async def test_summary_accumulates(memory):
    await memory.record_turn("u1", "conv1", "What is Wazuh?", "Wazuh is a SIEM")
    state = await memory.load("u1", "conv1")
    assert "Wazuh" in state.summary


@pytest.mark.asyncio
async def test_investigation_continuity(memory):
    await memory.record_turn("u1", "conv1", "Analyze this windows event", "doing", engine="WINDOWS_EVENT_LOG")
    state = await memory.load("u1", "conv1")
    assert state.investigation["active"] is True
    assert state.investigation["engine"] == "WINDOWS_EVENT_LOG"
    assert state.investigation["is_lab"] is False


@pytest.mark.asyncio
async def test_lab_continuity(memory):
    await memory.record_turn("u1", "conv1", "Start the wazuh lab", "ok", engine="WAZUH_LAB")
    state = await memory.load("u1", "conv1")
    assert state.investigation["is_lab"] is True


@pytest.mark.asyncio
async def test_uploaded_files_merge_and_dedupe(memory):
    await memory.record_turn("u1", "conv1", "analyze this", "ok", files=[{"name": "log.txt", "kind": "log"}])
    await memory.record_turn("u1", "conv1", "analyze this", "ok", files=[{"name": "log.txt", "kind": "log"}])
    await memory.record_turn("u1", "conv1", "look at screenshot", "ok", images=["data/img/shot1.png"])
    state = await memory.load("u1", "conv1")
    names = {f["name"] for f in state.uploaded_files}
    assert "log.txt" in names
    assert "shot1.png" in names
    assert len(state.uploaded_files) == 2


@pytest.mark.asyncio
async def test_context_isolation_between_conversations(memory):
    await memory.record_turn("u1", "conv1", "Explain Wazuh", "ok")
    await memory.record_turn("u1", "conv2", "Explain Sigma", "ok")
    s1 = await memory.load("u1", "conv1")
    s2 = await memory.load("u1", "conv2")
    assert "Sigma" not in s1.summary
    assert "Wazuh" not in s2.summary


@pytest.mark.asyncio
async def test_no_conversation_id_does_not_persist(memory):
    await memory.record_turn("u1", None, "Explain Wazuh", "ok")
    state = await memory.load("u1", None)
    assert state.summary == ""
    assert state.rolling_messages == []
