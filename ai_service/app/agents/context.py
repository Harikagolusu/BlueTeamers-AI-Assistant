from typing import Optional, Any, List, Dict
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

# Logical Groupings to avoid a God Object Context

class ExecutionContext(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    execution_id: str
    cancellation_token: Optional[Any] = None
    timeout_ms: Optional[int] = None

class UserContext(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    user_id: str
    roles: List[str] = Field(default_factory=list)
    preferences: Dict[str, Any] = Field(default_factory=dict)

class ConversationContext(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    session_id: str
    previous_turns: int = 0
    metadata: Dict[str, Any] = Field(default_factory=dict)

class KnowledgeContext(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    retrieved_documents: List[Any] = Field(default_factory=list)
    relevant_vectors: List[Any] = Field(default_factory=list)

class RuntimeContext(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    runtime_manager: Any = None
    prompt_builder: Any = None
    # Use Any or lazy imports if circular dependencies arise

class SecurityContext(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    auth_token: Optional[str] = None
    permissions: List[str] = Field(default_factory=list)

class AgentContext(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True)
    """
    Unified state wrapper passed into agent executions. 
    Delegates to logical sub-contexts.
    """
    execution: ExecutionContext
    user: UserContext
    conversation: ConversationContext
    knowledge: KnowledgeContext = Field(default_factory=KnowledgeContext)
    runtime: RuntimeContext = Field(default_factory=RuntimeContext)
    security: SecurityContext = Field(default_factory=SecurityContext)
