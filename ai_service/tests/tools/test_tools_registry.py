import pytest
from app.tools.registry.tool_registry import ToolRegistry
from app.tools.registry.registry_factory import RegistryFactory
from app.tools.interfaces.tool import ITool
from app.tools.models.tool_request import ToolRequest
from app.tools.models.tool_response import ToolResponse
from app.tools.domain.exceptions import ToolRegistrationError, ToolNotFoundError

class MockTool(ITool):
    def __init__(self, name="mock_tool"):
        self._name = name
    @property
    def name(self) -> str: return self._name
    @property
    def description(self) -> str: return "Mock tool"
    async def initialize(self): pass
    async def shutdown(self): pass
    async def execute(self, request: ToolRequest) -> ToolResponse:
        return ToolResponse(success=True)

def test_registry_register_and_get():
    registry = ToolRegistry()
    tool = MockTool()
    registry.register_tool(tool)
    
    retrieved = registry.get_tool("mock_tool")
    assert retrieved is tool

def test_registry_duplicate_registration():
    registry = ToolRegistry()
    registry.register_tool(MockTool())
    with pytest.raises(ToolRegistrationError):
        registry.register_tool(MockTool())

def test_registry_missing_tool():
    registry = ToolRegistry()
    with pytest.raises(ToolNotFoundError):
        registry.get_tool("nonexistent")

def test_registry_freeze_double():
    registry = ToolRegistry()
    registry.freeze()
    assert registry.is_frozen is True
    # Calling freeze again should be a no-op, shouldn't raise exception
    registry.freeze()
    assert registry.is_frozen is True

def test_registry_snapshot_immutability():
    registry = ToolRegistry()
    registry.register_tool(MockTool("tool1"))
    registry.freeze()
    
    snapshot = registry.get_registered_tools()
    assert isinstance(snapshot, tuple)
    assert len(snapshot) == 1
    assert snapshot[0].name == "tool1"
    
    assert registry.tool_count == 1
    
def test_registry_register_none():
    registry = ToolRegistry()
    with pytest.raises(ToolRegistrationError, match="Cannot register None"):
        registry.register_tool(None)

def test_registry_register_invalid_type():
    registry = ToolRegistry()
    class BadTool:
        name = "bad"
    with pytest.raises(ToolRegistrationError, match="Tool must implement ITool"):
        registry.register_tool(BadTool())

def test_registry_invalid_name():
    registry = ToolRegistry()
    with pytest.raises(ToolRegistrationError, match="Invalid tool name"):
        registry.register_tool(MockTool("Invalid Name!"))
    with pytest.raises(ToolRegistrationError, match="Invalid tool name"):
        registry.register_tool(MockTool(""))

def test_registry_factory_singleton():
    RegistryFactory.reset()
    reg1 = RegistryFactory.create_registry([MockTool()])
    reg2 = RegistryFactory.create_registry()
    
    assert reg1 is reg2
    assert reg1.is_frozen is True
    assert reg1.get_tool("mock_tool") is not None

def test_config_validation():
    from pydantic import ValidationError
    from app.tools.config import ToolConfig
    
    with pytest.raises(ValidationError):
        ToolConfig(TOOL_GLOBAL_EXECUTION_TIMEOUT_SEC=0)
        
    with pytest.raises(ValidationError):
        ToolConfig(TOOL_GLOBAL_EXECUTION_TIMEOUT_SEC=1000)
        
    with pytest.raises(ValidationError):
        ToolConfig(TOOL_DEFAULT_CACHE_TTL_SEC=-1)
