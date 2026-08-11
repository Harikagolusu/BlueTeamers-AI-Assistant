import pytest
from app.chat.exceptions.chat_exceptions import (
    ValidationError,
    AuthorizationError,
    RoutingError,
    EngineUnavailable
)

def test_exception_serialization():
    err = ValidationError("Invalid input", trace_id="12345")
    
    serialized = err.to_dict()
    assert serialized["error"]["code"] == "ERR_VALIDATION_400"
    assert serialized["error"]["message"] == "Invalid input"
    assert serialized["error"]["trace_id"] == "12345"

def test_engine_unavailable_exception():
    err = EngineUnavailable("No such engine", trace_id="abc")
    serialized = err.to_dict()
    assert serialized["error"]["code"] == "ERR_ENGINE_503"
    assert serialized["error"]["message"] == "No such engine"
