from typing import Any, Optional, Dict
from pydantic import BaseModel, Field, ConfigDict
from app.agents.context import AgentContext

class ToolContext(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True)
    """
    Context passed to tools during execution for deep integration.
    """
    agent_id: Optional[str] = None
    runtime_manager: Any = None
    user_id: Optional[str] = None
    memory_service: Any = None
    cancellation_token: Optional[Any] = None
    logger: Any = None
    metrics: Any = None
    correlation_id: Optional[str] = None
    
    agent_context: Optional[AgentContext] = None
