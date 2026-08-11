from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class ToolParameterProperty(BaseModel):
    """
    Represents a property within a tool's parameter schema.
    
    Purpose:
        Defines an individual argument parameter constraint in a provider-agnostic way.
    """
    type: str = Field(..., description="The data type of the property (e.g., 'string', 'integer')")
    description: str = Field(..., description="A description of the property")
    enum: Optional[List[str]] = Field(None, description="Allowed values for this property if it is an enum")
    
    model_config = {
        "frozen": True
    }

class ToolParameters(BaseModel):
    """
    Represents the parameters accepted by a tool.
    
    Purpose:
        Defines the root object schema for the tool arguments.
    """
    type: str = Field(default="object", description="The type of the parameters object, usually 'object'")
    properties: Dict[str, ToolParameterProperty] = Field(default_factory=dict, description="The properties of the parameters object")
    required: List[str] = Field(default_factory=list, description="A list of required property names")
    
    model_config = {
        "frozen": True
    }

class ToolDefinition(BaseModel):
    """
    Represents a provider-agnostic definition of a tool's capabilities and schema.
    
    Purpose:
        Provides the structural blueprint of a tool so that Providers can translate it to LLM-specific schemas,
        and Service layers can evaluate capabilities (caching, routing).
        
    Immutability:
        Frozen. Represents the static capabilities of a tool.
        
    Expected lifecycle:
        Generated on startup or registry query. Passed to Provider translators.
        
    Usage:
        Consumed by registry listings, LLM system prompt builders, and agent routers.
    """
    name: str = Field(..., description="The name of the tool")
    description: str = Field(..., description="A clear description of what the tool does")
    parameters: ToolParameters = Field(..., description="The schema of the parameters the tool accepts")
    
    version: str = Field(default="1.0.0", description="The version of the tool interface")
    category: Optional[str] = Field(default=None, description="Optional logical grouping category")
    tags: List[str] = Field(default_factory=list, description="Searchable tags for multi-agent discovery")
    requires_authentication: bool = Field(default=False, description="Whether the tool requires user authentication")
    cacheable: bool = Field(default=False, description="Whether the tool output is safe to cache")
    default_timeout: Optional[int] = Field(default=None, description="Default timeout in seconds for this tool")
    
    model_config = {
        "frozen": True
    }
