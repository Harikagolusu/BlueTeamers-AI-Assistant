from abc import ABC, abstractmethod
from typing import Any

from app.tools.context import ToolContext

class ITool(ABC):
    """
    Contract for a single executable Tool in the framework.
    """
    @property
    @abstractmethod
    def name(self) -> str:
        pass
        
    @property
    @abstractmethod
    def metadata(self) -> Any:
        """Returns the ToolMetadata object associated with this tool."""
        pass

    @abstractmethod
    async def execute(self, context: ToolContext, **kwargs) -> Any:
        """Asynchronously executes the tool logic."""
        pass
