from typing import Optional
from app.mcp.interfaces.i_mcp_transport import IMCPTransport

class StdioTransport(IMCPTransport):
    def __init__(self, command: str, args: list[str]):
        self.command = command
        self.args = args
        self._process = None

    async def connect(self) -> None:
        # In a real implementation, start subprocess and hook up stdin/stdout
        pass

    async def disconnect(self) -> None:
        # Terminate subprocess
        pass

    async def send(self, message: str) -> None:
        # Write to stdin
        pass

    async def receive(self) -> Optional[str]:
        # Read from stdout
        return None
