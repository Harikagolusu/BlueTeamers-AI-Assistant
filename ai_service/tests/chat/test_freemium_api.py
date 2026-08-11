"""API integration tests for the freemium chat endpoint (Sprint 5)."""
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.routes.chat import router as chat_router
from app.chat.bootstrap import get_chat_service
from app.chat.interfaces.i_chat_service import IChatService
from app.freemium.dependencies import get_freemium_service_singleton
from app.freemium.service import FreemiumService
from app.freemium.store import FreemiumStore
from app.models.chat.chat_models import ChatResponse
from app.platform.models import Purchase


class _FakeChatService(IChatService):
    async def process_request(self, request):
        return ChatResponse(
            conversation_id=request.conversation_id or "conv-1",
            message="Mock answer",
        )


class _FakePlatformRepo:
    def __init__(self, purchases=None):
        self._purchases = purchases or []

    async def get_purchases(self, token):
        return self._purchases


def _make_app(tmp_path, purchases=None, limit=5):
    store = FreemiumStore(db_path=str(tmp_path / "freemium.db"))
    service = FreemiumService(store, _FakePlatformRepo(purchases))
    app = FastAPI()
    app.include_router(chat_router, prefix="/api/v1/chat")
    app.dependency_overrides[get_freemium_service_singleton] = lambda: service
    app.dependency_overrides[get_chat_service] = lambda: _FakeChatService()
    return TestClient(app), service


@pytest.fixture
def resolve_user(monkeypatch):
    """Make any Authorization token resolve to a stable user_id (bypasses RS256)."""
    from app.api.routes import chat as chat_routes

    def _resolve(token):
        if not token:
            return None, None
        return "user-1", "user@example.com"

    monkeypatch.setattr(chat_routes, "resolve_user_identity", _resolve)


def _token_payload(user_id: int = 1, email: str = "user@example.com"):
    import base64
    import json
    import time

    header = base64.urlsafe_b64encode(json.dumps({"alg": "RS256", "typ": "JWT"}).encode()).decode().rstrip("=")
    payload = base64.urlsafe_b64encode(
        json.dumps({"user_id": user_id, "email": email, "exp": int(time.time()) + 3600}).encode()
    ).decode().rstrip("=")
    return f"{header}.{payload}.not-a-real-signature"


@pytest.fixture
def free_client(tmp_path, resolve_user):
    client, _ = _make_app(tmp_path, purchases=[])
    return client


def test_access_endpoint_reports_free_user(free_client):
    res = free_client.get("/api/v1/chat/access", headers={"Authorization": f"Bearer {_token_payload()}"})
    assert res.status_code == 200
    data = res.json()
    assert data["is_premium"] is False
    assert data["limit"] == 5
    assert data["remaining"] == 5


def test_free_user_limited_after_n_messages(free_client):
    headers = {"Authorization": f"Bearer {_token_payload()}"}
    for i in range(5):
        res = free_client.post("/api/v1/chat/", json={"message": f"q{i}", "stream": False}, headers=headers)
        assert res.status_code == 200, res.text
    res = free_client.post("/api/v1/chat/", json={"message": "one too many", "stream": False}, headers=headers)
    assert res.status_code == 429
    data = res.json()
    assert data["detail"]["code"] == "free_ai_limit_reached"
    assert data["detail"]["access"]["remaining"] == 0


def test_premium_user_unlimited(tmp_path, resolve_user):
    purchases = [Purchase(course_slug="soc", status="paid", amount=499, created_at="x")]
    client, _ = _make_app(tmp_path, purchases=purchases)
    headers = {"Authorization": f"Bearer {_token_payload()}"}
    for i in range(12):
        res = client.post("/api/v1/chat/", json={"message": f"q{i}", "stream": False}, headers=headers)
        assert res.status_code == 200, res.text
    res = client.get("/api/v1/chat/access", headers=headers)
    assert res.json()["is_premium"] is True


def test_anonymous_user_not_limited_or_tracked(free_client, resolve_user):
    for i in range(10):
        res = free_client.post("/api/v1/chat/", json={"message": f"q{i}", "stream": False})
        assert res.status_code == 200, res.text


def test_guest_with_client_id_is_limited(free_client, resolve_user):
    for i in range(5):
        res = free_client.post(
            "/api/v1/chat/",
            json={"message": f"q{i}", "stream": False, "client_id": "device-abc"},
        )
        assert res.status_code == 200, res.text
    res = free_client.post(
        "/api/v1/chat/",
        json={"message": "one too many", "stream": False, "client_id": "device-abc"},
    )
    assert res.status_code == 429
    data = res.json()
    assert data["detail"]["code"] == "free_ai_limit_reached"
    assert data["detail"]["access"]["remaining"] == 0
    assert "Login and join" in data["detail"]["message"]


def test_guest_access_endpoint_tracks_usage(free_client, resolve_user):
    client_id = "device-def"
    for i in range(3):
        res = free_client.post(
            "/api/v1/chat/",
            json={"message": f"q{i}", "stream": False, "client_id": client_id},
        )
        assert res.status_code == 200, res.text
    res = free_client.get("/api/v1/chat/access", params={"client_id": client_id})
    assert res.status_code == 200
    data = res.json()
    assert data["access_level"] == "free"
    assert data["limit"] == 5
    assert data["used"] == 3
    assert data["remaining"] == 2


def test_distinct_guests_have_independent_limits(free_client, resolve_user):
    for i in range(5):
        res = free_client.post(
            "/api/v1/chat/",
            json={"message": f"a{i}", "stream": False, "client_id": "guest-a"},
        )
        assert res.status_code == 200, res.text
    assert (
        free_client.post(
            "/api/v1/chat/",
            json={"message": "over", "stream": False, "client_id": "guest-a"},
        ).status_code
        == 429
    )
    # guest-b is untouched.
    assert (
        free_client.post(
            "/api/v1/chat/",
            json={"message": "fresh", "stream": False, "client_id": "guest-b"},
        ).status_code
        == 200
    )
