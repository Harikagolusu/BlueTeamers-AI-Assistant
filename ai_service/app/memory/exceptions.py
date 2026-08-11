class MemoryException(Exception):
    """Base exception for memory module"""
    pass

class SessionNotFound(MemoryException):
    """Raised when a requested session does not exist"""
    pass

class MemoryLimitExceeded(MemoryException):
    """Raised when session limits are exceeded"""
    pass
