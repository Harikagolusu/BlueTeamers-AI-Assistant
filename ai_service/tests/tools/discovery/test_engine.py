import pytest
from unittest.mock import Mock, patch
from app.tools.discovery.engine.discovery_engine import DiscoveryEngine
from app.tools.discovery.config.config import DiscoveryConfig
from app.tools.discovery.metadata.models import ToolMetadata

class MockTool:
    def __init__(self):
        self.name = "mock_tool"

def test_discovery_engine_pipeline():
    config = DiscoveryConfig()
    mock_loader = Mock()
    mock_loader.load_packages.return_value = ["mock_module"]
    
    mock_scanner = Mock()
    mock_scanner.scan_classes.return_value = [MockTool]
    
    mock_resolver = Mock()
    mock_resolver.resolve.return_value = ToolMetadata(name="mock_tool", description="desc")
    
    mock_validator = Mock()
    mock_filter = Mock()
    mock_filter.should_include.return_value = True
    
    mock_registration = Mock()
    
    engine = DiscoveryEngine(
        config=config,
        loader=mock_loader,
        scanner=mock_scanner,
        resolver=mock_resolver,
        validator=mock_validator,
        filter_svc=mock_filter,
        registration=mock_registration,
        di_resolver=lambda cls: cls()
    )
    
    report = engine.discover_and_register()
    
    assert report.loaded_tools == 1
    assert report.registered_tools == 1
    assert report.failed_tools == 0
    
    mock_registration.register.assert_called_once()
