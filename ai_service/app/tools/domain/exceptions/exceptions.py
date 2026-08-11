class ToolError(Exception):
    """
    Base exception for all tool-related errors.
    
    When it should be raised: Never directly. Subclasses should be raised.
    Who should catch it: The ToolExecutor or outer API boundaries to normalize errors.
    """
    pass

class ToolExecutionError(ToolError):
    """
    Raised when a tool encounters an error during execution (e.g., network failure, timeout).
    
    When it should be raised: By the Executor or the concrete tool when execution fails.
    Who should catch it: The ToolExecutor (to convert to a failed ToolResponse).
    """
    pass

class ToolValidationError(ToolError):
    """
    Raised when tool arguments fail validation against the expected schema.
    
    When it should be raised: Pre-execution, if the ToolRequest arguments are malformed.
    Who should catch it: ToolExecutor or ToolService.
    """
    pass

class ToolRegistrationError(ToolError):
    """
    Raised when there is an issue registering a tool (e.g., duplicate name).
    
    When it should be raised: At application startup during registry initialization.
    Who should catch it: Fast-fails the application boot.
    """
    pass

class ToolNotFoundError(ToolError):
    """
    Raised when attempting to access or execute a tool that is not registered.
    
    When it should be raised: By the Registry or Executor if lookup fails.
    Who should catch it: ToolExecutor.
    """
    pass

class ToolTimeoutError(ToolExecutionError):
    """
    Raised when a tool execution exceeds the configured timeout threshold.
    
    When it should be raised: By the ToolExecutor's asyncio.wait_for block.
    Who should catch it: ToolExecutor.
    """
    pass

class ToolAuthorizationError(ToolError):
    """
    Raised when the execution context lacks the required permissions to invoke the tool.
    
    When it should be raised: Pre-execution by the ToolService or Guardrails.
    Who should catch it: ToolService (to convert to a blocked ToolResponse).
    """
    pass

class ToolConfigurationError(ToolError):
    """
    Raised when a concrete tool is misconfigured (e.g., missing API keys).
    
    When it should be raised: During tool instantiation at startup.
    Who should catch it: Fast-fails the application boot.
    """
    pass

class ToolProviderError(ToolError):
    """
    Raised when a provider adapter fails to translate a schema.
    
    When it should be raised: During definition translation.
    Who should catch it: The component requesting the schema.
    """
    pass
