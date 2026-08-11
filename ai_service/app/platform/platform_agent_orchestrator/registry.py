from typing import Dict, Any

class PlatformAgentOrchestratorRegistry:
    def __init__(self):
        self.tools = {}
        
    def register_tool(self, tool_name: str, tool_instance: Any):
        self.tools[tool_name] = tool_instance
        
    def get_tool(self, tool_name: str) -> Any:
        return self.tools.get(tool_name)
