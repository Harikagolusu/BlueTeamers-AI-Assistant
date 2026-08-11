import inspect
from typing import List, Type, Any
from app.tools.interfaces.tool import ITool
from app.tools.discovery.interfaces.discovery_interfaces import IClassScanner
from app.tools.discovery.exceptions.exceptions import ToolScanningError

class ClassScanner(IClassScanner):
    """
    Inspects loaded modules to locate subclasses of ITool with __tool_metadata__.
    """
    def scan_classes(self, modules: List[Any]) -> List[Type[ITool]]:
        discovered_classes = set()
        
        for module in modules:
            try:
                # getmembers safe against missing attributes
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    # Must be a subclass of ITool
                    if issubclass(obj, ITool) and obj is not ITool:
                        # Must have the metadata injected by decorator
                        if hasattr(obj, '__tool_metadata__') and obj.__tool_metadata__ is not None:
                            # Avoid duplicate classes from different import paths
                            discovered_classes.add(obj)
            except Exception as e:
                raise ToolScanningError(f"Failed to scan module {module.__name__}: {e}")
                
        return list(discovered_classes)
