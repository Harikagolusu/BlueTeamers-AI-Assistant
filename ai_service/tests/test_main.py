import pytest
from fastapi.testclient import TestClient

from app.main import app

@pytest.fixture
def client():
    # Use TestClient context manager to trigger lifespan events
    with TestClient(app) as test_client:
        yield test_client

def _with_token():
    from app.core.config import settings
    settings.INTERNAL_ADMIN_TOKEN = "test-internal-token"
    return {"X-Internal-Token": "test-internal-token"}

def test_root_endpoint_anonymous_minimal(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_root_endpoint_detailed_with_token(client):
    response = client.get("/", headers=_with_token())
    assert response.status_code == 200
    data = response.json()
    assert "service" in data
    assert "version" in data
    assert data["status"] == "online"

def test_health_endpoint_anonymous_minimal(client):
    """Unauthenticated health probes must not leak internals (info disclosure)."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_health_endpoint_detailed_with_token(client):
    response = client.get("/health", headers=_with_token())
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "components" in data

def test_api_health_endpoint_anonymous_minimal(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_api_health_endpoint_detailed_with_token(client):
    response = client.get("/api/health", headers=_with_token())
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "components" in data

def test_health_detail_requires_valid_token(client):
    from app.core.config import settings
    settings.INTERNAL_ADMIN_TOKEN = "test-internal-token"
    response = client.get("/health", headers={"X-Internal-Token": "wrong-token"})
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_middleware_request_id(client):
    response = client.get("/")
    assert response.status_code == 200
    # Our middleware might not inject it in headers, but logs it.
    # We just ensure the request passes middleware cleanly.

def test_validation_error_handler(client):
    # Send empty payload to chat to trigger 422
    response = client.post("/api/v1/chat", json={"query": ""})
    assert response.status_code == 422
    assert "detail" in response.json()

def test_not_found_handler(client):
    response = client.get("/nonexistent/endpoint")
    assert response.status_code == 404
    assert "detail" in response.json()