from abc import ABC, abstractmethod
from typing import Dict, Any

class IToolExecutor(ABC):
    @abstractmethod
    async def execute(self, tool_name: str, arguments: Dict[str, Any], permissions: Dict[str, bool]) -> Dict[str, Any]:
        """
        Public facade for the Enterprise Tool Framework.
        """
        pass
