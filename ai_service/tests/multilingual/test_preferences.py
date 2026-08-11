"""Tests for the per-user language preference store (Sprint 7 — Feature 6)."""
import pytest

from app.multilingual.preferences import LanguagePreferenceStore


@pytest.fixture()
def store(tmp_path) -> LanguagePreferenceStore:
    return LanguagePreferenceStore(db_path=str(tmp_path / "langs.db"))


@pytest.mark.asyncio
async def test_get_missing_returns_none(store):
    assert await store.get("user-1") is None


@pytest.mark.asyncio
async def test_set_and_get(store):
    await store.set("user-1", "te")
    assert await store.get("user-1") == "te"


@pytest.mark.asyncio
async def test_upsert_overwrites(store):
    await store.set("user-1", "te")
    await store.set("user-1", "en")
    assert await store.get("user-1") == "en"


@pytest.mark.asyncio
async def test_users_are_isolated(store):
    await store.set("user-1", "te")
    await store.set("user-2", "hi")
    assert await store.get("user-1") == "te"
    assert await store.get("user-2") == "hi"


@pytest.mark.asyncio
async def test_clear(store):
    await store.set("user-1", "te")
    await store.clear("user-1")
    assert await store.get("user-1") is None


@pytest.mark.asyncio
async def test_invalid_code_raises(store):
    with pytest.raises(ValueError):
        await store.set("user-1", "not-a-language")


@pytest.mark.asyncio
async def test_auto_code_is_supported(store):
    await store.set("user-1", "auto")
    assert await store.get("user-1") == "auto"
