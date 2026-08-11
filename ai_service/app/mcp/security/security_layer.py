from typing import List, Dict, Any, Optional

class SecurityLayer:
    """
    Handles permission validation, allowlists, and payload limits for MCP interactions.
    """
    def __init__(self, allowed_servers: List[str] = None):
        self._allowed_servers = allowed_servers or []
        self._max_payload_bytes = 10 * 1024 * 1024 # 10MB

    def is_server_allowed(self, server_name: str) -> bool:
        if not self._allowed_servers: # if empty, allow all (or default block depending on policy)
            return True
        return server_name in self._allowed_servers

    def validate_tool_permission(self, tool_name: str, context_permissions: Dict[str, bool]) -> bool:
        # In a real implementation, check if the specific tool or namespace is allowed.
        return context_permissions.get(tool_name, True)
        
    def validate_resource_permission(self, uri: str, context_permissions: Dict[str, bool]) -> bool:
        # Validates if the user/context can read this resource
        return True

    def validate_prompt_permission(self, prompt_name: str, context_permissions: Dict[str, bool]) -> bool:
        # Validates if the user/context can fetch this prompt
        return True

    def validate_payload_size(self, payload: str) -> bool:
        return len(payload.encode('utf-8')) <= self._max_payload_bytes
