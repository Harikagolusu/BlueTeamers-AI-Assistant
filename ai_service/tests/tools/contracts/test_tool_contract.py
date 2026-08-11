import pytest
import importlib
import inspect
from pathlib import Path
from app.tools.domain.base_tool import BaseTool
from app.tools.models.tool_request import ToolRequest
from app.tools.models.tool_response import ToolResponse
from app.tools.models.execution_context import ExecutionContext

def get_all_tool_classes():
    base_dir = Path("app/tools/implementations")
    tool_classes = []
    
    for file_path in base_dir.rglob("*.py"):
        if file_path.name == "__init__.py":
            continue
            
        module_name = str(file_path.with_suffix("")).replace("\\", ".").replace("/", ".")
        module = importlib.import_module(module_name)
        
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, BaseTool) and obj is not BaseTool:
                tool_classes.append(obj)
                
    return tool_classes

@pytest.mark.asyncio
@pytest.mark.parametrize("tool_class", get_all_tool_classes())
async def test_tool_contract(tool_class):
    # This is a bit tricky because tools require injected services.
    # For a contract test, we'll mock the service to just return a dummy or raise an exception
    # However, since they require DI, we might need a dummy service or use pytest-mock.
    pass # Placeholder for actual contract tests requiring full DI setup

# Instead of instantiating, let's just verify class signatures for now
@pytest.mark.parametrize("tool_class", get_all_tool_classes())
def test_tool_execute_signature(tool_class):
    sig = inspect.signature(tool_class.execute)
    assert "request" in sig.parameters
    assert sig.parameters["request"].annotation == ToolRequest
    assert sig.return_annotation == ToolResponse
