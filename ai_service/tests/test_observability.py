import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.observability.registry import MetricsRegistry

client = TestClient(app)

def test_metrics_endpoint():
    """Test that the /metrics endpoint returns prometheus metrics."""
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "api_requests_total" in response.text
    assert "ai_llm_requests_total" in response.text

def test_health_endpoint_includes_observability():
    """Test that the aggregated health endpoint includes observability status.
    The detailed payload is restricted to callers bearing the internal token."""
    from app.core.config import settings
    settings.INTERNAL_ADMIN_TOKEN = "test-internal-token"
    headers = {"X-Internal-Token": "test-internal-token"}
    response = client.get("/health", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "observability" in data["components"]
    assert data["components"]["observability"]["metrics"] == "healthy"
    assert data["components"]["observability"]["tracing"] == "healthy"

def test_health_endpoint_anonymous_does_not_leak_components():
    """Unauthenticated health probes return only a liveness marker."""
    from app.core.config import settings
    settings.INTERNAL_ADMIN_TOKEN = "test-internal-token"
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_tracing_middleware():
    """Test that the tracing middleware injects X-Trace-ID."""
    response = client.get("/health")
    assert "X-Trace-ID" in response.headers
    trace_id = response.headers["X-Trace-ID"]
    assert len(trace_id) == 32  # 32 char hex

def test_tracing_middleware_with_traceparent():
    """Test that the tracing middleware respects incoming W3C traceparent headers."""
    test_trace_id = "4bf92f3577b34da6a3ce929d0e0e4736"
    test_parent_span_id = "00f067aa0ba902b7"
    headers = {
        "traceparent": f"00-{test_trace_id}-{test_parent_span_id}-01"
    }
    response = client.get("/health", headers=headers)
    assert response.headers.get("X-Trace-ID") == test_trace_id
