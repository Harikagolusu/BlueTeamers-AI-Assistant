from pydantic import BaseModel, Field
from typing import Any, Optional, Dict
import uuid

class ToolContext(BaseModel):
    """
    Enterprise tool context providing deep traceability and execution environment details.
    """
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    execution_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: Optional[str] = None
    tenant_id: Optional[str] = None
    
    # Internal Framework References
    logger: Optional[Any] = Field(None, exclude=True, description="Injected logger instance")
    metrics_collector: Optional[Any] = Field(None, exclude=True, description="Injected metrics collector")
    provider_info: Dict[str, Any] = Field(default_factory=dict, description="LLM that triggered this tool")
    cancellation_token: Optional[Any] = Field(None, exclude=True, description="Async cancellation primitive")
    
    model_config = {"arbitrary_types_allowed": True}
