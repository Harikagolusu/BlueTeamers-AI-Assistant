class StreamingException(Exception):
    """Base exception for the streaming module"""
    pass

class ProviderStreamException(StreamingException):
    """Raised when the underlying provider stream fails"""
    pass

class StreamCancellationException(StreamingException):
    """Raised when the client disconnects before completion"""
    pass
