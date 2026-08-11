from typing import Type
from app.tools.interfaces.tool import ITool
from app.tools.discovery.interfaces.discovery_interfaces import IMetadataResolver
from app.tools.discovery.metadata.models import ToolMetadata
from app.tools.discovery.exceptions.exceptions import InvalidMetadataError

class MetadataResolver(IMetadataResolver):
    """
    Normalizes cls.__tool_metadata__ into a ToolMetadata instance.
    """
    def resolve(self, tool_class: Type[ITool]) -> ToolMetadata:
        if not hasattr(tool_class, '__tool_metadata__') or not tool_class.__tool_metadata__:
            raise InvalidMetadataError(f"Class {tool_class.__name__} is missing __tool_metadata__.")
            
        metadata = tool_class.__tool_metadata__
        
        if not isinstance(metadata, ToolMetadata):
            raise InvalidMetadataError(f"Class {tool_class.__name__} has invalid metadata type. Expected ToolMetadata.")
            
        return metadata
