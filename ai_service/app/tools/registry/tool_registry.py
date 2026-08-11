from typing import Tuple, Dict, Mapping, List, Optional
import threading
import re
from types import MappingProxyType
from app.tools.interfaces.registry import IToolRegistry
from app.tools.interfaces.tool import ITool
from app.tools.domain.exceptions import ToolRegistrationError, ToolNotFoundError

class ToolRegistry(IToolRegistry):
    """
    Production-ready Tool Registry.
    Provides O(1) lookups, duplicate protection, and a thread-safe freeze mechanism.
    Maintains backward compatibility with legacy registry interfaces.
    """
    def __init__(self):
        self._tools: Dict[str, ITool] = {}
        self._frozen_tools: Mapping[str, ITool] = None
        self._frozen: bool = False
        self._lock = threading.RLock()
        self._name_pattern = re.compile(r"^[a-z0-9_]+$")
        
    def register_tool(self, tool: ITool) -> None:
        """Registers a tool if the registry is not frozen and the name is valid and unique."""
        if tool is None:
            raise ToolRegistrationError("Cannot register None as a tool.")
        if not isinstance(tool, ITool):
            raise ToolRegistrationError("Tool must implement ITool interface.")
            
        with self._lock:
            if self._frozen:
                raise ToolRegistrationError("Cannot register tool: Registry is frozen.")
            if not tool.name or not self._name_pattern.match(tool.name):
                raise ToolRegistrationError(f"Invalid tool name '{tool.name}'. Must be lowercase, alphanumeric, and underscores only.")
            if tool.name in self._tools:
                raise ToolRegistrationError(f"Tool with name '{tool.name}' is already registered.")
            self._tools[tool.name] = tool
            
    def get_tool(self, name: str) -> ITool:
        """Retrieves a tool by name. O(1) lookup. Read-only (lock free) for performance."""
        lookup_dict = self._frozen_tools if self._frozen else self._tools
        tool = lookup_dict.get(name)
        if not tool:
            raise ToolNotFoundError(f"Tool '{name}' not found in registry.")
        return tool
        
    def get_registered_tools(self) -> Tuple[ITool, ...]:
        """Retrieves an immutable snapshot of all registered tools."""
        lookup_dict = self._frozen_tools if self._frozen else self._tools
        return tuple(lookup_dict.values())
        
    def unregister_tool(self, name: str) -> None:
        """Unregisters a tool. Thread-safe and respects freeze state."""
        with self._lock:
            if self._frozen:
                raise ToolRegistrationError("Cannot unregister tool: Registry is frozen.")
            if name in self._tools:
                del self._tools[name]
            else:
                raise ToolNotFoundError(f"Tool '{name}' not found in registry.")

    def filter_by_capability(self, capability: str) -> List[ITool]:
        """Filters tools by a specific capability."""
        lookup_dict = self._frozen_tools if self._frozen else self._tools
        return [
            tool for tool in lookup_dict.values()
            if hasattr(tool, 'metadata') and capability in getattr(tool.metadata, 'capabilities', [])
        ]

    def filter_by_tag(self, tag: str) -> List[ITool]:
        """Filters tools by a specific tag."""
        lookup_dict = self._frozen_tools if self._frozen else self._tools
        return [
            tool for tool in lookup_dict.values()
            if hasattr(tool, 'metadata') and tag in getattr(tool.metadata, 'tags', [])
        ]
        
    def freeze(self) -> None:
        """Freezes the registry, making the internal storage immutable."""
        with self._lock:
            if not self._frozen:
                self._frozen_tools = MappingProxyType(self._tools)
                self._frozen = True
            
    @property
    def is_frozen(self) -> bool:
        return self._frozen
        
    @property
    def tool_count(self) -> int:
        lookup_dict = self._frozen_tools if self._frozen else self._tools
        return len(lookup_dict)

    # Backward compatibility aliases
    def register(self, tool: ITool) -> None:
        self.register_tool(tool)

    def get(self, name: str) -> Optional[ITool]:
        try:
            return self.get_tool(name)
        except ToolNotFoundError:
            return None

    def list_all(self) -> List[ITool]:
        return list(self.get_registered_tools())

    def unregister(self, name: str) -> None:
        try:
            self.unregister_tool(name)
        except ToolNotFoundError:
            pass
