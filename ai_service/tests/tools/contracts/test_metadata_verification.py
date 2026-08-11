import pytest
from tests.tools.contracts.test_tool_contract import get_all_tool_classes
from app.tools.discovery.metadata.models import ToolMetadata

@pytest.mark.parametrize("tool_class", get_all_tool_classes())
def test_tool_metadata_verification(tool_class):
    metadata = getattr(tool_class, "__tool_metadata__", None)
    assert metadata is not None, f"Tool {tool_class.__name__} is missing @tool metadata"
    assert isinstance(metadata, ToolMetadata)
    
    # Verify required fields
    assert metadata.name, f"Tool {tool_class.__name__} missing name"
    assert metadata.description, f"Tool {tool_class.__name__} missing description"
    assert metadata.category is not None, f"Tool {tool_class.__name__} missing category"
    assert metadata.version, f"Tool {tool_class.__name__} missing version"
    assert metadata.state is not None, f"Tool {tool_class.__name__} missing state"
