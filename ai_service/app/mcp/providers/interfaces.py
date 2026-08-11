from abc import ABC, abstractmethod
from typing import Dict, Any, List

class IToolProvider(ABC):
    @abstractmethod
    async def execute_tool(self, tool_name: str, arguments: Dict[str, Any], permissions: List[str] = None) -> Dict[str, Any]:
        pass
        
    @abstractmethod
    def supports(self, capability: str) -> bool:
        pass
        
    @abstractmethod
    def provider_type(self) -> str:
        pass

class IMCPToolProvider(IToolProvider):
    pass
