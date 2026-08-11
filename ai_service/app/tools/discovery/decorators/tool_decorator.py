from typing import List, Optional, Type
from app.tools.discovery.metadata.enums import ToolCategory, ToolState
from app.tools.discovery.metadata.models import ToolMetadata

def tool(
    name: str,
    description: str,
    category: ToolCategory = ToolCategory.CUSTOM,
    version: str = "1.0.0",
    aliases: Optional[List[str]] = None,
    permissions: Optional[List[str]] = None,
    state: ToolState = ToolState.ACTIVE,
    timeout: Optional[int] = 30
):
    """
    Decorator to annotate a class as an auto-discoverable tool.
    Injects a ToolMetadata instance into the class.
    
    Args:
        name: Unique identifier for the tool.
        description: LLM-facing description of the tool.
        category: Logical grouping.
        version: Semantic version.
        aliases: Alternative names for the tool.
        permissions: Required permissions to execute.
        state: Lifecycle state (e.g., ACTIVE, EXPERIMENTAL).
        timeout: Execution timeout in seconds.
    """
    def decorator(cls: Type) -> Type:
        metadata = ToolMetadata(
            name=name,
            description=description,
            category=category,
            version=version,
            aliases=aliases or [],
            permissions=permissions or [],
            state=state,
            timeout=timeout
        )
        cls.__tool_metadata__ = metadata
        return cls
    return decorator
