import pytest
from app.tools.domain.exceptions import (
    ToolError,
    ToolExecutionError,
    ToolValidationError,
    ToolRegistrationError,
    ToolNotFoundError,
    ToolTimeoutError,
    ToolAuthorizationError,
    ToolConfigurationError,
    ToolProviderError
)

def test_exception_hierarchy():
    # Ensure all inherit from ToolError
    assert issubclass(ToolExecutionError, ToolError)
    assert issubclass(ToolValidationError, ToolError)
    assert issubclass(ToolRegistrationError, ToolError)
    assert issubclass(ToolNotFoundError, ToolError)
    assert issubclass(ToolTimeoutError, ToolExecutionError)
    assert issubclass(ToolAuthorizationError, ToolError)
    assert issubclass(ToolConfigurationError, ToolError)
    assert issubclass(ToolProviderError, ToolError)

def test_exception_instantiation():
    err = ToolTimeoutError("Execution took too long")
    assert isinstance(err, ToolTimeoutError)
    assert str(err) == "Execution took too long"
