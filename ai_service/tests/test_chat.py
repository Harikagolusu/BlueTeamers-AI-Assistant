import pytest
import uuid
from unittest.mock import MagicMock, AsyncMock
from fastapi.testclient import TestClient
from fastapi import FastAPI

from app.chat.router import router
from app.chat.dependencies import get_chat_health_service
from app.chat.bootstrap import get_chat_service
from app.models.chat.chat_models import ChatResponse as DomainChatResponse
from app.rag.schemas import SourceCitation, PipelineMetrics
from app.rag.exceptions import EmptyContextException, GenerationFailure
from app.freemium.dependencies import get_freemium_service_singleton
from app.freemium.service import FreemiumService
from app.freemium.store import FreemiumStore

# Setup test app
app = FastAPI()
app.include_router(router)

@pytest.fixture
def mock_chat_service():
    mock = AsyncMock()
    mock.process_request.return_value = DomainChatResponse(
        conversation_id="test-session",
        message="test answer",
        metadata={"citations": [], "metrics": PipelineMetrics()}
    )
    return mock

@pytest.fixture
def mock_health_service():
    mock = MagicMock()
    mock.check_health.return_value = {"status": "healthy"}
    return mock

@pytest.fixture
def client(mock_chat_service, mock_health_service):
    app.dependency_overrides[get_chat_service] = lambda: mock_chat_service
    app.dependency_overrides[get_chat_health_service] = lambda: mock_health_service
    # Use an isolated, empty freemium store so the persistent dev DB (data/
    # freemium.db) doesn't leave earlier runs over the daily free limit.
    store = FreemiumStore(db_path=":memory:")
    app.dependency_overrides[get_freemium_service_singleton] = lambda: FreemiumService(store=store)
    yield TestClient(app)
    app.dependency_overrides.clear()

def test_chat_success(client, mock_chat_service):
    response = client.post(
        "/api/v1/chat",
        json={"query": "test query", "client_id": "test-client-1"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["answer"] == "test answer"
    assert "request_id" in data
    mock_chat_service.process_request.assert_called_once()

def test_chat_validation_failure(client):
    response = client.post(
        "/api/v1/chat",
        json={"query": ""}
    )
    assert response.status_code == 422 # FastAPI Pydantic validation

def test_chat_empty_context(client, mock_chat_service):
    mock_chat_service.process_request.side_effect = EmptyContextException("Empty")
    response = client.post(
        "/api/v1/chat",
        json={"query": "test query", "client_id": "test-client-1"}
    )
    assert response.status_code == 404
    assert "No relevant context" in response.json()["detail"]

def test_chat_generation_failure(client, mock_chat_service):
    mock_chat_service.process_request.side_effect = GenerationFailure("Fail")
    response = client.post(
        "/api/v1/chat",
        json={"query": "test query", "client_id": "test-client-1"}
    )
    assert response.status_code == 502
    assert "AI generation service unavailable" in response.json()["detail"]

def test_chat_requires_identity(client):
    response = client.post(
        "/api/v1/chat",
        json={"query": "test query"}
    )
    assert response.status_code == 401

def test_chat_health(client):
    response = client.get("/api/v1/chat/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_chat_stream_success(client, mock_chat_service):
    async def mock_generator():
        yield "data: test\n\n"
    mock_chat_service.process_request.return_value = mock_generator()
    
    response = client.post(
        "/api/v1/chat/stream",
        json={"query": "test query", "client_id": "test-client-1"}
    )
    assert response.status_code == 200
