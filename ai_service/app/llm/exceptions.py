class LLMException(Exception):
    """Base exception for all LLM-related errors."""
    pass

class ProviderUnavailableException(LLMException):
    """Raised when the LLM provider API is unreachable."""
    pass

class ModelNotFoundException(LLMException):
    """Raised when the requested model is not found by the provider."""
    pass

class LLMTimeoutException(LLMException):
    """Raised when the LLM provider times out during generation."""
    pass

class RateLimitException(LLMException):
    """Raised when the LLM provider rate limits the requests."""
    pass

class ProviderConfigurationException(LLMException):
    """Raised when the provider is misconfigured (e.g. missing API keys)."""
    pass
