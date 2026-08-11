class DjangoAPIException(Exception):
    """Base exception for all Django API related errors."""
    pass

class DjangoUnavailableException(DjangoAPIException):
    """Raised when the Django API is down or unreachable (e.g. 502, 503, ConnectTimeout)."""
    pass

class UnauthorizedException(DjangoAPIException):
    """Raised when the provided JWT token is rejected by Django (401, 403)."""
    pass

class NotFoundException(DjangoAPIException):
    """Raised when the requested resource does not exist in Django (404)."""
    pass

class ValidationException(DjangoAPIException):
    """Raised when Django rejects a payload due to validation errors (400, 422)."""
    pass

class PlatformUnavailable(DjangoUnavailableException):
    """Raised when the platform backend is completely unavailable."""
    pass

class PlatformAuthenticationFailed(UnauthorizedException):
    """Raised when platform authentication fails."""
    pass

class PlatformEndpointMissing(NotFoundException):
    """Raised when a specific platform endpoint or resource is missing."""
    pass

