class ToolDiscoveryError(Exception):
    """Base exception for all tool discovery errors."""
    pass

class ToolLoadingError(ToolDiscoveryError):
    """Raised when a module fails to import dynamically."""
    pass

class ToolScanningError(ToolDiscoveryError):
    """Raised when scanning a loaded module fails."""
    pass

class ToolValidationError(ToolDiscoveryError):
    """Raised when a tool fails schema or duplicate validation."""
    pass

class DuplicateToolError(ToolValidationError):
    """Raised when a tool with the same name is discovered multiple times."""
    pass

class InvalidMetadataError(ToolDiscoveryError):
    """Raised when a tool has malformed or missing metadata."""
    pass

class ToolRegistrationError(ToolDiscoveryError):
    """Raised when the registration service fails to register the tool."""
    pass
