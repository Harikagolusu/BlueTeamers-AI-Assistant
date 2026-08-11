import pytest
from app.models.chat.chat_models import ExecutionResult, ExecutionStatus

def test_execution_result_success():
    result = ExecutionResult.success(
        engine="RAG",
        message="Test message",
        metadata={"key": "value"}
    )
    
    assert result.status == ExecutionStatus.SUCCESS
    assert result.engine_name == "RAG"
    assert result.message == "Test message"
    assert result.metadata == {"key": "value"}
    assert result.errors == []

def test_execution_result_failed():
    result = ExecutionResult.failed(
        engine="TOOL",
        errors=[{"error": "Failed to connect"}]
    )
    
    assert result.status == ExecutionStatus.FAILED
    assert result.engine_name == "TOOL"
    assert len(result.errors) == 1
    assert result.errors[0]["error"] == "Failed to connect"
