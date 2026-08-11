from typing import Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from app.tools.models.types import ToolMetadata

class ExecutionContext(BaseModel):
    """
    Represents the execution context for a tool request.
    
    Purpose:
        Carries universally useful metadata (correlation ID, user context, session info)
        throughout the execution lifecycle without polluting the main ToolRequest.
        
    Immutability:
        This model is entirely frozen to prevent side effects.
        
    Expected lifecycle:
        Created by the Chat API (or ToolService) and passed down to the Executor and ITool.
        Never mutated during execution.
        
    Usage:
        Accessed by tools for auditing, RBAC decisions, or telemetry correlation.
    """
    correlation_id: UUID = Field(
        default_factory=uuid4, 
        description="A unique identifier for tracking this request across microservices"
    )
    user_id: Optional[str] = Field(
        default=None, 
        description="Optional identifier of the user invoking the tool"
    )
    session_id: Optional[str] = Field(
        default=None, 
        description="Optional identifier for the current chat session"
    )
    tenant_id: Optional[str] = Field(
        default=None, 
        description="Optional identifier for the tenant/organization"
    )
    request_id: Optional[str] = Field(
        default=None, 
        description="Optional specific request trace ID from the API gateway"
    )
    metadata: ToolMetadata = Field(
        default_factory=dict, 
        description="Any additional generic context required for enterprise auditing"
    )
    
    model_config = {
        "frozen": True
    }
