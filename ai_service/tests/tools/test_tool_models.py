import pytest
from uuid import UUID
from pydantic import ValidationError
from app.tools.models import (
    ExecutionContext,
    ToolRequest,
    ToolResponse,
    ToolDefinition,
    ToolParameters,
    ToolParameterProperty
)

def test_execution_context_default_uuid():
    context = ExecutionContext()
    assert isinstance(context.correlation_id, UUID)
    assert context.user_id is None
    assert context.session_id is None

def test_execution_context_serialization():
    context = ExecutionContext(user_id="user123", metadata={"role": "admin"})
    dumped = context.model_dump()
    assert dumped["user_id"] == "user123"
    assert dumped["metadata"] == {"role": "admin"}
    
    # Round trip
    context2 = ExecutionContext.model_validate(dumped)
    assert context2.correlation_id == context.correlation_id
    assert context2.user_id == context.user_id

def test_execution_context_immutability():
    context = ExecutionContext()
    with pytest.raises(ValidationError):
        context.user_id = "new_user"

def test_tool_request_construction():
    context = ExecutionContext()
    request = ToolRequest(tool_name="test_tool", arguments={"arg1": "value1"}, context=context)
    assert request.tool_name == "test_tool"
    assert request.arguments == {"arg1": "value1"}
    assert request.context == context

def test_tool_request_immutability():
    request = ToolRequest(tool_name="test_tool", arguments={})
    with pytest.raises(ValidationError):
        request.tool_name = "other_tool"

def test_tool_response_construction():
    response = ToolResponse(success=True, result={"data": "test"}, metadata={"cache_hit": True})
    assert response.success is True
    assert response.result == {"data": "test"}
    assert response.error is None
    assert response.metadata["cache_hit"] is True

def test_tool_response_error():
    response = ToolResponse(success=False, error="Timeout")
    assert response.success is False
    assert response.error == "Timeout"
    assert response.result is None

def test_tool_definition_construction():
    prop = ToolParameterProperty(type="string", description="A string param", enum=["a", "b"])
    params = ToolParameters(properties={"param1": prop}, required=["param1"])
    
    definition = ToolDefinition(
        name="test_tool",
        description="A test tool",
        parameters=params,
        category="testing",
        tags=["test", "demo"]
    )
    
    assert definition.name == "test_tool"
    assert definition.version == "1.0.0"
    assert definition.category == "testing"
    assert "test" in definition.tags
    assert not definition.requires_authentication
