import pytest
from app.tools.discovery.resolver.metadata_resolver import MetadataResolver
from app.tools.discovery.metadata.models import ToolMetadata
from app.tools.discovery.decorators.tool_decorator import tool
from app.tools.discovery.exceptions.exceptions import InvalidMetadataError
from app.tools.domain.base_tool import BaseTool

def test_metadata_resolver_success():
    @tool(name="test_tool", description="A test tool")
    class TestTool(BaseTool):
        async def execute(self, req): pass
        
    resolver = MetadataResolver()
    metadata = resolver.resolve(TestTool)
    
    assert metadata.name == "test_tool"
    assert metadata.description == "A test tool"

def test_metadata_resolver_missing_metadata():
    class NoMetadataTool(BaseTool):
        # BaseTool's __init__ will fail, but we're testing the class-level resolver
        async def execute(self, req): pass
        
    resolver = MetadataResolver()
    with pytest.raises(InvalidMetadataError) as exc:
        resolver.resolve(NoMetadataTool)
    assert "missing __tool_metadata__" in str(exc.value)

def test_metadata_resolver_invalid_type():
    class InvalidTool(BaseTool):
        __tool_metadata__ = {"name": "not a model"}
        async def execute(self, req): pass
        
    resolver = MetadataResolver()
    with pytest.raises(InvalidMetadataError) as exc:
        resolver.resolve(InvalidTool)
    assert "invalid metadata type" in str(exc.value)
