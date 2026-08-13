"""Tests for the freemium access service (Sprint 5)."""
import pytest

from app.freemium.models import AccessLevel, FreemiumLimitExceeded
from app.freemium.service import FreemiumService
from app.freemium.store import FreemiumStore
from app.platform.models import Purchase


class _FakePlatformRepo:
    def __init__(self, purchases=None, raises=False):
        self._purchases = purchases or []
        self._raises = raises

    async def get_purchases(self, token):
        if self._raises:
            raise RuntimeError("django down")
        return self._purchases


@pytest.fixture
def store(tmp_path):
    return FreemiumStore(db_path=str(tmp_path / "freemium.db"))


def _service(store, purchases=None, raises=False, limit=5, enabled=True):
    service = FreemiumService(store, _FakePlatformRepo(purchases, raises))
    service._premium_cache.clear()
    return service


@pytest.mark.asyncio
async def test_premium_user_has_unlimited_status(store):
    repo_purchases = [Purchase(course_slug="soc", status="paid", amount=499, created_at="x")]
    service = _service(store, repo_purchases)
    status = await service.get_access_status("user-1", "token")
    assert status.is_premium is True
    assert status.access_level == AccessLevel.PREMIUM
    assert status.can_send() is True


@pytest.mark.asyncio
async def test_free_user_gets_daily_limit(store):
    service = _service(store, purchases=[])
    status = await service.get_access_status("user-1", "token")
    assert status.is_premium is False
    assert status.access_level == AccessLevel.FREE
    assert status.limit == 5
    assert status.used == 0
    assert status.remaining == 5


@pytest.mark.asyncio
async def test_free_user_consumes_slots(store):
    service = _service(store, purchases=[])
    for i in range(1, 4):
        decision = await service.check_and_consume("user-1", "token")
        assert decision.allowed is True
        assert decision.status.used == i
        assert decision.status.remaining == 5 - i


@pytest.mark.asyncio
async def test_free_user_blocked_after_limit(store):
    service = _service(store, purchases=[])
    for _ in range(5):
        await service.check_and_consume("user-1", "token")
    with pytest.raises(FreemiumLimitExceeded):
        await service.check_and_consume("user-1", "token")


@pytest.mark.asyncio
async def test_premium_user_never_limited(store):
    repo_purchases = [Purchase(course_slug="soc", status="paid", amount=499, created_at="x")]
    service = _service(store, repo_purchases)
    for _ in range(20):
        decision = await service.check_and_consume("user-1", "token")
        assert decision.allowed is True


@pytest.mark.asyncio
async def test_django_down_fails_open_to_free(store):
    service = _service(store, raises=True)
    status = await service.get_access_status("user-1", "token")
    assert status.is_premium is False
    assert status.access_level == AccessLevel.FREE


@pytest.mark.asyncio
async def test_disabled_freemium_grants_premium_style_access(store, monkeypatch):
    from app.freemium import service as service_module

    service = _service(store, purchases=[])
    monkeypatch.setattr(service_module.settings, "FREEMIUM_ENABLED", False)
    status = await service.get_access_status("user-1", "token")
    assert status.enabled is False
    assert status.can_send() is True


@pytest.mark.asyncio
async def test_configurable_limit(store, monkeypatch):
    from app.freemium import service as service_module

    service = _service(store, purchases=[])
    monkeypatch.setattr(service_module.settings, "FREEMIUM_FREE_MESSAGE_LIMIT", 3)
    status = await service.get_access_status("user-1", "token")
    assert status.limit == 3


@pytest.mark.asyncio
async def test_guest_usage_carried_over_on_login(store):
    """A guest who used messages should not get a fresh allowance after login:
    their used count is folded into the authenticated user's quota."""
    service = _service(store, purchases=[])
    for _ in range(3):
        await store.increment("guest:device-abc")

    status = await service.get_access_status("user-1", "token", client_id="device-abc")
    assert status.access_level == AccessLevel.FREE
    assert status.used == 3
    assert status.remaining == 2


@pytest.mark.asyncio
async def test_guest_usage_carried_over_blocks_at_limit(store):
    service = _service(store, purchases=[])
    for _ in range(5):
        await store.increment("guest:device-abc")

    with pytest.raises(FreemiumLimitExceeded):
        await service.check_and_consume("user-1", "token", client_id="device-abc")
