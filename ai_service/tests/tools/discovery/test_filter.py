from app.tools.discovery.filters.tool_filter import ToolFilter
from app.tools.discovery.config.config import DiscoveryConfig
from app.tools.discovery.metadata.models import ToolMetadata
from app.tools.discovery.metadata.enums import ToolState

def test_filter_active_tool():
    config = DiscoveryConfig()
    tool_filter = ToolFilter(config)
    metadata = ToolMetadata(name="t", description="d", state=ToolState.ACTIVE)
    assert tool_filter.should_include(metadata) is True

def test_filter_disabled_tool():
    config = DiscoveryConfig()
    tool_filter = ToolFilter(config)
    metadata = ToolMetadata(name="t", description="d", state=ToolState.DISABLED)
    assert tool_filter.should_include(metadata) is False

def test_filter_experimental_excluded():
    config = DiscoveryConfig(include_experimental=False)
    tool_filter = ToolFilter(config)
    metadata = ToolMetadata(name="t", description="d", state=ToolState.EXPERIMENTAL)
    assert tool_filter.should_include(metadata) is False

def test_filter_experimental_included():
    config = DiscoveryConfig(include_experimental=True)
    tool_filter = ToolFilter(config)
    metadata = ToolMetadata(name="t", description="d", state=ToolState.EXPERIMENTAL)
    assert tool_filter.should_include(metadata) is True

def test_filter_deprecated_excluded():
    config = DiscoveryConfig(allow_deprecated=False)
    tool_filter = ToolFilter(config)
    metadata = ToolMetadata(name="t", description="d", state=ToolState.DEPRECATED)
    assert tool_filter.should_include(metadata) is False
