from pydantic import BaseModel, Field

class ToolCapabilities(BaseModel):
    requires_network: bool = Field(default=False, description="Requires external network access")
    requires_authentication: bool = Field(default=False, description="Requires authenticated context")
    cacheable: bool = Field(default=True, description="Output can be safely cached")
    deterministic: bool = Field(default=True, description="Always produces the same output for same input")
    side_effects: bool = Field(default=False, description="Mutates state outside of the tool")
    supports_streaming: bool = Field(default=False, description="Can stream results")
    supports_batch: bool = Field(default=False, description="Can accept batch inputs")
    supports_progress: bool = Field(default=False, description="Reports progress during execution")
    supports_cancellation: bool = Field(default=True, description="Can be safely cancelled")
    supports_mcp: bool = Field(default=False, description="Compatible with Model Context Protocol")
    estimated_latency: str = Field(default="low", description="Expected execution time (low, medium, high)")
    resource_usage: str = Field(default="low", description="Expected CPU/Memory footprint (low, medium, high)")

    model_config = {"frozen": True}
