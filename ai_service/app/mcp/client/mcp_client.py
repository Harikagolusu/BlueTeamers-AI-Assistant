import json
import logging
import asyncio
from typing import Dict, Any
from app.mcp.interfaces.i_mcp_client import IMCPClient
from app.mcp.interfaces.i_mcp_transport import IMCPTransport
from app.mcp.models import MCPSession, MCPResponse, MCPRequest, MCPError, SessionState

logger = logging.getLogger(__name__)

class MCPClient(IMCPClient):
    def __init__(self, transport: IMCPTransport, server_name: str):
        self._transport = transport
        self._server_name = server_name
        self._session = None
        self._pending_requests: Dict[str, asyncio.Future] = {}
        self._listen_task = None

    async def connect(self) -> None:
        await self._transport.connect()
        self._listen_task = asyncio.create_task(self._listen_loop())

    async def disconnect(self) -> None:
        if self._listen_task:
            self._listen_task.cancel()
        await self._transport.disconnect()
        if self._session:
            self._session.state = SessionState.CLOSED

    async def _listen_loop(self):
        try:
            while True:
                message_str = await self._transport.receive()
                if not message_str:
                    continue
                    
                try:
                    data = json.loads(message_str)
                    if "id" in data and "method" not in data: # It's a response
                        response = MCPResponse(**data)
                        if response.id in self._pending_requests:
                            self._pending_requests[response.id].set_result(response)
                    else:
                        # Handle server requests/notifications if needed
                        pass
                except json.JSONDecodeError:
                    logger.error(f"Failed to parse JSON RPC message: {message_str}")
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error(f"Error in listen loop: {e}")

    async def _send_request(self, method: str, params: Dict[str, Any] = None) -> MCPResponse:
        request = MCPRequest(method=method, params=params or {})
        future = asyncio.Future()
        self._pending_requests[request.id] = future
        
        await self._transport.send(request.model_dump_json())
        
        try:
            response = await asyncio.wait_for(future, timeout=30.0)
            if self._session:
                self._session.update_activity()
            return response
        except asyncio.TimeoutError:
            del self._pending_requests[request.id]
            return MCPResponse(
                id=request.id,
                error=MCPError(code=-32000, message="Request timeout")
            )

    async def initialize_session(self) -> MCPSession:
        response = await self._send_request("initialize", {"capabilities": {}})
        if response.is_error:
            raise Exception(f"Failed to initialize MCP session: {response.error.message}")
            
        self._session = MCPSession(
            server_name=self._server_name,
            state=SessionState.ACTIVE,
            metadata=response.result
        )
        return self._session

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> MCPResponse:
        return await self._send_request("tools/call", {
            "name": tool_name,
            "arguments": arguments
        })

    async def read_resource(self, uri: str) -> MCPResponse:
        return await self._send_request("resources/read", {"uri": uri})

    async def fetch_prompt(self, name: str, arguments: Dict[str, str]) -> MCPResponse:
        return await self._send_request("prompts/get", {
            "name": name,
            "arguments": arguments
        })
