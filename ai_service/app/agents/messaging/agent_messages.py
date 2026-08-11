import uuid
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Any, Dict, Optional

class AgentMessage(BaseModel):
    message_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    sender_id: str
    receiver_id: Optional[str] = None
    correlation_id: Optional[str] = None

class TaskRequest(AgentMessage):
    task_id: str
    step_id: str
    input_data: Dict[str, Any] = Field(default_factory=dict)

class TaskResponse(AgentMessage):
    task_id: str
    success: bool
    result_data: Dict[str, Any] = Field(default_factory=dict)
    error: Optional[str] = None

class ProgressUpdate(AgentMessage):
    task_id: str
    progress_percent: float
    status_message: str

class FailureNotification(AgentMessage):
    task_id: str
    error: str
    can_retry: bool = False

class ClarificationRequest(AgentMessage):
    task_id: str
    question: str
