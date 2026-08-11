from typing import Dict, Any, Callable, Awaitable
from app.mcp.transport.interfaces import IMCPTransport

class StdioTransport(IMCPTransport):
    def __init__(self, command: str, args: list[str]):
        self.command = command
        self.args = args
        self._callback = None
        
    async def connect(self) -> None:
        pass
        
    async def disconnect(self) -> None:
        pass
        
    async def send_message(self, message: Dict[str, Any]) -> None:
        pass
        
    def on_message(self, callback: Callable[[Dict[str, Any]], Awaitable[None]]) -> None:
        self._callback = callback
