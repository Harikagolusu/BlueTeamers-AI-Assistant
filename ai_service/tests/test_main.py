import pytest
from fastapi.testclient import TestClient

from app.main import app

@pytest.fixture
def client():
    # Use TestClient context manager to trigger lifespan events
    with TestClient(app) as test_client:
        yield test_client

def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "service" in data
    assert "version" in data
    assert data["status"] == "online"

def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "components" in data

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
