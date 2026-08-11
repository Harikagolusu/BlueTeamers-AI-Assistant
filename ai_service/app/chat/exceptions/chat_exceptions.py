class BaseChatError(Exception):
    """Base exception for all Chat Integration Framework errors."""
    def __init__(self, message: str, code: str, trace_id: str = None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.trace_id = trace_id
        
    def to_dict(self):
        return {
            "error": {
                "code": self.code,
                "message": self.message,
                "trace_id": self.trace_id
            }
        }

class ValidationError(BaseChatError):
    def __init__(self, message: str, trace_id: str = None):
        super().__init__(message, "ERR_VALIDATION_400", trace_id)

class AuthorizationError(BaseChatError):
    def __init__(self, message: str, trace_id: str = None):
        super().__init__(message, "ERR_AUTHZ_403", trace_id)

class RoutingError(BaseChatError):
    def __init__(self, message: str, trace_id: str = None):
        super().__init__(message, "ERR_ROUTING_404", trace_id)

class EngineUnavailable(BaseChatError):
    def __init__(self, message: str, trace_id: str = None):
        super().__init__(message, "ERR_ENGINE_503", trace_id)

class ProviderFailure(BaseChatError):
    def __init__(self, message: str, trace_id: str = None):
        super().__init__(message, "ERR_PROVIDER_502", trace_id)

class TimeoutError(BaseChatError):
    def __init__(self, message: str, trace_id: str = None):
        super().__init__(message, "ERR_TIMEOUT_504", trace_id)

class RateLimitError(BaseChatError):
    def __init__(self, message: str, trace_id: str = None):
        super().__init__(message, "ERR_RATELIMIT_429", trace_id)

class ToolExecutionError(BaseChatError):
    def __init__(self, message: str, trace_id: str = None):
        super().__init__(message, "ERR_TOOL_500", trace_id)

class RAGFailure(BaseChatError):
    def __init__(self, message: str, trace_id: str = None):
        super().__init__(message, "ERR_RAG_500", trace_id)

class StreamingFailure(BaseChatError):
    def __init__(self, message: str, trace_id: str = None):
        super().__init__(message, "ERR_STREAM_500", trace_id)

class UnknownFailure(BaseChatError):
    def __init__(self, message: str, trace_id: str = None):
        super().__init__(message, "ERR_UNKNOWN_500", trace_id)
