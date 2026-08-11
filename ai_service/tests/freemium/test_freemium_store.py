"""Tests for the freemium usage store (Sprint 5)."""
import pytest

from app.freemium.store import FreemiumStore


@pytest.fixture
def store(tmp_path):
    return FreemiumStore(db_path=str(tmp_path / "freemium.db"))


@pytest.mark.asyncio
async def test_load_returns_zero_for_fresh_user(store):
    state = await store.load("user-1")
    assert state.used == 0
    assert state.reset  # reset key present


@pytest.mark.asyncio
async def test_increment_counts_and_persists(store):
    assert await store.increment("user-1") == 1
    assert await store.increment("user-1") == 2
    state = await store.load("user-1")
    assert state.used == 2


@pytest.mark.asyncio
async def test_users_are_isolated(store):
    await store.increment("user-1")
    state = await store.load("user-2")
    assert state.used == 0


@pytest.mark.asyncio
async def test_reset_clears_usage(store):
    await store.increment("user-1")
    await store.reset("user-1")
    state = await store.load("user-1")
    assert state.used == 0


@pytest.mark.asyncio
async def test_new_day_window_is_separate(store, monkeypatch):
    import datetime

    from app.freemium import store as store_module

    now = datetime.datetime(2026, 8, 7, 10, 0, 0, tzinfo=datetime.timezone.utc)
    monkeypatch.setattr(store_module, "_utc_now", lambda: now)
    await store.increment("user-1")

    later = datetime.datetime(2026, 8, 8, 9, 0, 0, tzinfo=datetime.timezone.utc)
    monkeypatch.setattr(store_module, "_utc_now", lambda: later)
    state = await store.load("user-1")
    assert state.used == 0
