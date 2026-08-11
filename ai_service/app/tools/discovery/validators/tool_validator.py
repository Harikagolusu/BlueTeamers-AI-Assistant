from typing import Set
from app.tools.discovery.interfaces.discovery_interfaces import IToolValidator
from app.tools.discovery.metadata.models import ToolMetadata
from app.tools.discovery.exceptions.exceptions import ToolValidationError, DuplicateToolError

class ToolValidator(IToolValidator):
    """
    Checks the extracted metadata against the global state and rejects violations.
    """
    def validate(self, metadata: ToolMetadata, existing_names: set) -> None:
        if metadata.name in existing_names:
            raise DuplicateToolError(f"Duplicate tool name discovered: {metadata.name}")
            
        for alias in metadata.aliases:
            if alias in existing_names:
                raise DuplicateToolError(f"Duplicate alias name discovered: {alias} (belongs to {metadata.name})")
                
        if not metadata.name.isidentifier():
            # In registry we enforced alphanumeric + underscores
            if not all(c.isalnum() or c == '_' for c in metadata.name):
                raise ToolValidationError(f"Invalid tool name '{metadata.name}'. Must be alphanumeric/underscores.")
                
        if metadata.timeout is not None and metadata.timeout <= 0:
            raise ToolValidationError(f"Timeout for '{metadata.name}' must be > 0.")
