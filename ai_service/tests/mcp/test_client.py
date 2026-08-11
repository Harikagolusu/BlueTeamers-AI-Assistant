import pytest
import asyncio
from typing import Optional
from app.mcp.client.mcp_client import MCPClient
from app.mcp.interfaces.i_mcp_transport import IMCPTransport

class DummyTransport(IMCPTransport):
    def __init__(self):
        self.sent_messages = []
        self.receive_queue = asyncio.Queue()

    async def connect(self) -> None:
        pass

    async def disconnect(self) -> None:
        pass

    async def send(self, message: str) -> None:
        self.sent_messages.append(message)

    async def receive(self) -> Optional[str]:
        return await self.receive_queue.get()

@pytest.mark.asyncio
async def test_mcp_client_initialize():
    transport = DummyTransport()
    client = MCPClient(transport, "test_server")
    await client.connect()
    
    # Simulate server response
    async def mock_response():
        # wait a bit to ensure client is awaiting
        await asyncio.sleep(0.01)
        req = transport.sent_messages[0]
        import json
        req_id = json.loads(req)["id"]
        resp = json.dumps({"jsonrpc": "2.0", "id": req_id, "result": {"capabilities": {}}})
        await transport.receive_queue.put(resp)

    asyncio.create_task(mock_response())
    
    session = await client.initialize_session()
    assert session.server_name == "test_server"
    assert session.state == "active"
    
    await client.disconnect()
