from app.tools.discovery.interfaces.discovery_interfaces import IToolFilter
from app.tools.discovery.metadata.models import ToolMetadata
from app.tools.discovery.metadata.enums import ToolState
from app.tools.discovery.config.config import DiscoveryConfig

class ToolFilter(IToolFilter):
    """
    Applies feature flags and visibility rules to determine if a tool should be loaded.
    """
    def __init__(self, config: DiscoveryConfig):
        self._config = config
        
    def should_include(self, metadata: ToolMetadata) -> bool:
        if metadata.state == ToolState.DISABLED:
            return False
            
        if metadata.state == ToolState.EXPERIMENTAL and not self._config.include_experimental:
            return False
            
        if metadata.state == ToolState.DEPRECATED and not self._config.allow_deprecated:
            return False
            
        return True
