class GuardrailException(Exception):
    """Base exception for all guardrail-related errors."""
    pass

class InputValidationError(GuardrailException):
    """Raised when an input fails basic validation."""
    pass

class PolicyViolationError(GuardrailException):
    """Raised when a security or compliance policy is violated."""
    pass

class InfrastructureFailureError(GuardrailException):
    """Raised when an external adapter or service fails."""
    pass

class TimeoutFailureError(GuardrailException):
    """Raised when a policy execution times out."""
    pass

class ConfigurationError(GuardrailException):
    """Raised when the guardrails configuration is invalid."""
    pass
