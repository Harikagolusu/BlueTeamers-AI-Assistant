import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from app.api.routes.chat import router as new_chat_router
from app.models.chat.chat_models import ChatResponse

@pytest.fixture(autouse=True)
def mock_retrieval_dependencies(monkeypatch):
    from unittest.mock import MagicMock
    from app.embeddings import dependencies as emb_dep
    from app.vector_store import dependencies as vs_dep
    from app.retrieval import dependencies as ret_dep
    
    mock_emb = MagicMock()
    mock_vs = MagicMock()
    mock_rerank = MagicMock()
    
    monkeypatch.setattr(emb_dep, "get_embedding_service", lambda *args, **kwargs: mock_emb)
    monkeypatch.setattr(vs_dep, "get_vector_store_service", lambda *args, **kwargs: mock_vs)
    monkeypatch.setattr(ret_dep, "get_reranker", lambda *args, **kwargs: mock_rerank)

@pytest.fixture(autouse=True)
def mock_llm_factory(monkeypatch):
    from app.llm.factory import LLMFactory
    from app.llm.base import BaseLLMProvider
    from app.llm.schemas import LLMRequest, LLMResponse
    
    class MockLLMProvider(BaseLLMProvider):
        async def generate(self, request: LLMRequest) -> LLMResponse:
            return LLMResponse(
                text="Mock Response",
                provider="mock",
                model="mock",
                latency_ms=10.0
            )
        async def stream_generate(self, request: LLMRequest):
            yield "Mock"
            yield " Response"
        async def health_check(self):
            return {"status": "healthy"}
            
    mock_provider = MockLLMProvider()
    monkeypatch.setattr(LLMFactory, "get_provider", lambda: mock_provider)
    return mock_provider

@pytest.fixture
def client():
    test_app = FastAPI()
    test_app.include_router(new_chat_router, prefix="/api/v1/chat")
    with TestClient(test_app) as test_client:
        yield test_client

def test_chat_api_endpoint(client):
    payload = {
        "message": "hello",
        "stream": False
    }
    
    response = client.post("/api/v1/chat/", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert "conversation_id" in data
    assert "message" in data
    assert "BlueTeamers" in data["message"]

def test_chat_api_non_greeting_uses_llm(client):
    payload = {
        "message": "Tell me a fun fact about dinosaurs",
        "stream": False
    }

    response = client.post("/api/v1/chat/", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "conversation_id" in data
    assert "Mock Response" in data["message"]


def test_chat_api_streaming_endpoint(client):
    payload = {
        "message": "explain the water cycle to me",
        "stream": True
    }
    
    response = client.post("/api/v1/chat/", json=payload)
    
    assert response.status_code == 200
    assert response.headers.get("content-type") == "text/event-stream; charset=utf-8"
    
    text = response.text
    assert "Mock" in text

def test_greeting_stream_preserves_newlines(client):
    payload = {
        "message": "hello",
        "stream": True
    }
    
    response = client.post("/api/v1/chat/", json=payload)
    
    assert response.status_code == 200
    # The templated greeting (no LLM) is streamed with newlines intact so the
    # markdown structure (headings, bullets) is not flattened.
    assert "\\n" in response.text


def test_chat_endpoint_uses_authorization_header_as_token(client):
    """Regression: the web client sends the JWT in the Authorization header,
    not in the body. The endpoint must promote it to request.token so
    session_user is set and conversation persistence / memory / adaptive
    learning can record turns."""
    from app.api.dependencies import get_optional_raw_token
    from app.chat.bootstrap import get_chat_service

    captured = {}

    class FakeChatService:
        async def process_request(self, request):
            captured["token"] = request.token
            return ChatResponse(conversation_id="conv-1", message="ok", metadata={})

    client.app.dependency_overrides[get_optional_raw_token] = lambda: "header-jwt"
    client.app.dependency_overrides[get_chat_service] = lambda: FakeChatService()
    try:
        response = client.post(
            "/api/v1/chat/",
            json={"message": "hello", "stream": False, "conversation_id": "conv-1"},
            headers={"Authorization": "Bearer header-jwt"},
        )
        assert response.status_code == 200
        assert captured["token"] == "header-jwt"
    finally:
        client.app.dependency_overrides.clear()


def test_chat_endpoint_keeps_body_token_when_no_header(client):
    from app.api.dependencies import get_optional_raw_token
    from app.chat.bootstrap import get_chat_service

    captured = {}

    class FakeChatService:
        async def process_request(self, request):
            captured["token"] = request.token
            return ChatResponse(conversation_id="conv-1", message="ok", metadata={})

    client.app.dependency_overrides[get_optional_raw_token] = lambda: None
    client.app.dependency_overrides[get_chat_service] = lambda: FakeChatService()
    try:
        response = client.post(
            "/api/v1/chat/",
            json={"message": "hello", "stream": False, "conversation_id": "conv-1", "token": "body-jwt"},
        )
        assert response.status_code == 200
        assert captured["token"] == "body-jwt"
    finally:
        client.app.dependency_overrides.clear()
