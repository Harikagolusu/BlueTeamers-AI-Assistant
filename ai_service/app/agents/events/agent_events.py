from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime
import uuid

class AgentEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    type: str
    session_id: str
    metadata: Dict[str, Any] = Field(default_factory=dict)

# --- New Rich Agent SDK Events ---
class AgentCreatedEvent(AgentEvent): type: str = "AgentCreated"
class AgentStartedEvent(AgentEvent): type: str = "AgentStarted"
class PlanningStartedEvent(AgentEvent): type: str = "PlanningStarted"
class PlanningCompletedEvent(AgentEvent): type: str = "PlanningCompleted"
class RetrievalStartedEvent(AgentEvent): type: str = "RetrievalStarted"
class RetrievalCompletedEvent(AgentEvent): type: str = "RetrievalCompleted"
class ToolStartedEvent(AgentEvent): 
    type: str = "ToolStarted"
    tool_name: str
class ToolCompletedEvent(AgentEvent): 
    type: str = "ToolCompleted"
    tool_name: str
    result: Any = None
class MemoryReadEvent(AgentEvent): type: str = "MemoryRead"
class MemoryWriteEvent(AgentEvent): type: str = "MemoryWrite"
class LLMStartedEvent(AgentEvent): type: str = "LLMStarted"
class LLMCompletedEvent(AgentEvent): type: str = "LLMCompleted"
class ResponseGeneratedEvent(AgentEvent): type: str = "ResponseGenerated"
class AgentCompletedEvent(AgentEvent): type: str = "AgentCompleted"
class AgentFailedEvent(AgentEvent): 
    type: str = "AgentFailed"
    error: str

# --- Legacy/Executor Events (Kept for backwards compatibility with AgentExecutor) ---
class ExecutionStartedEvent(AgentEvent):
    type: str = "ExecutionStarted"
    plan_id: str

class StepStartedEvent(AgentEvent):
    type: str = "StepStarted"
    step_id: str

class StepCompletedEvent(AgentEvent):
    type: str = "StepCompleted"
    step_id: str
    output: Any = None

class StepFailedEvent(AgentEvent):
    type: str = "StepFailed"
    step_id: str
    error: str

class CheckpointCreatedEvent(AgentEvent):
    type: str = "CheckpointCreated"
    checkpoint_id: str

class RecoveryTriggeredEvent(AgentEvent):
    type: str = "RecoveryTriggered"
    step_id: str
    action: str

class ExecutionCompletedEvent(AgentEvent):
    type: str = "ExecutionCompleted"
    success: bool
    final_output: Optional[str] = None

# --- MCP Events ---
class MCPConnectedEvent(AgentEvent):
    type: str = "MCPConnected"
    server_name: str

class MCPDisconnectedEvent(AgentEvent):
    type: str = "MCPDisconnected"
    server_name: str

class MCPToolInvokedEvent(AgentEvent):
    type: str = "MCPToolInvoked"
    tool_name: str
    provider_id: str

class MCPToolCompletedEvent(AgentEvent):
    type: str = "MCPToolCompleted"
    tool_name: str
    result: Any

class MCPToolFailedEvent(AgentEvent):
    type: str = "MCPToolFailed"
    tool_name: str
    error: str

class MCPResourceReadEvent(AgentEvent):
    type: str = "MCPResourceRead"
    uri: str

class MCPPromptFetchedEvent(AgentEvent):
    type: str = "MCPPromptFetched"
    prompt_name: str

class CatalogUpdatedEvent(AgentEvent):
    type: str = "CatalogUpdated"

class ToolRegisteredEvent(AgentEvent):
    type: str = "ToolRegistered"
    tool_name: str
    provider_id: str

class ToolRemovedEvent(AgentEvent):
    type: str = "ToolRemoved"
    tool_name: str
    provider_id: str

class ToolHealthChangedEvent(AgentEvent):
    type: str = "ToolHealthChanged"
    tool_name: str
    health_status: str

# Multi-Agent Orchestration Events
class AgentRegisteredEvent(AgentEvent):
    type: str = "AgentRegistered"
    agent_id: str

class AgentDiscoveredEvent(AgentEvent):
    type: str = "AgentDiscovered"
    agent_id: str
    capability: str

class TaskDelegatedEvent(AgentEvent):
    type: str = "TaskDelegated"
    task_id: str
    agent_id: str

class AgentExecutionStartedEvent(AgentEvent):
    type: str = "AgentExecutionStarted"
    task_id: str
    agent_id: str

class TaskStartedEvent(AgentEvent):
    type: str = "TaskStarted"
    task_id: str

class TaskCompletedEvent(AgentEvent):
    type: str = "TaskCompleted"
    task_id: str
    result: Any = None

class TaskFailedEvent(AgentEvent):
    type: str = "TaskFailed"
    task_id: str
    error: str

class ConsensusStartedEvent(AgentEvent):
    type: str = "ConsensusStarted"
    task_id: str

class ConsensusCompletedEvent(AgentEvent):
    type: str = "ConsensusCompleted"
    task_id: str
    winning_agent_id: Optional[str] = None

class AggregationCompletedEvent(AgentEvent):
    type: str = "AggregationCompleted"
    plan_id: str

class CoordinationCompletedEvent(AgentEvent):
    type: str = "CoordinationCompleted"
    plan_id: str
    success: bool

# Marketplace & Plugin Events
class PluginDiscoveredEvent(AgentEvent):
    type: str = "PluginDiscovered"
    plugin_id: str

class PluginLoadedEvent(AgentEvent):
    type: str = "PluginLoaded"
    plugin_id: str

class PluginUnloadedEvent(AgentEvent):
    type: str = "PluginUnloaded"
    plugin_id: str

class PluginReloadedEvent(AgentEvent):
    type: str = "PluginReloaded"
    plugin_id: str

class SkillRegisteredEvent(AgentEvent):
    type: str = "SkillRegistered"
    skill_id: str

class SkillRemovedEvent(AgentEvent):
    type: str = "SkillRemoved"
    skill_id: str

class MarketplaceUpdatedEvent(AgentEvent):
    type: str = "MarketplaceUpdated"

class HealthCheckCompletedEvent(AgentEvent):
    type: str = "HealthCheckCompleted"
    report: Dict[str, Any]

class UsageMetricsCollectedEvent(AgentEvent):
    type: str = "UsageMetricsCollected"
    metrics: Dict[str, Any]

# --- Assessment Agent Events ---
class AssessmentStartedEvent(AgentEvent):
    type: str = "AssessmentStarted"
    topic: str = ""
    difficulty: str = ""

class AssessmentQuestionGeneratedEvent(AgentEvent):
    type: str = "AssessmentQuestionGenerated"
    question_id: str = ""
    question_type: str = ""

class AssessmentAnsweredEvent(AgentEvent):
    type: str = "AssessmentAnswered"
    question_id: str = ""
    correct: bool = False
    partial: bool = False

class AssessmentCompletedEvent(AgentEvent):
    type: str = "AssessmentCompleted"
    score: int = 0
    total: int = 0

class AssessmentPassedEvent(AgentEvent):
    type: str = "AssessmentPassed"
    score: int = 0
    total: int = 0

class AssessmentFailedEvent(AgentEvent):
    type: str = "AssessmentFailed"
    score: int = 0
    total: int = 0

class LearningProgressUpdatedEvent(AgentEvent):
    type: str = "LearningProgressUpdated"
    topics_completed: list = []
    average_score: float = 0.0

class QuizSkippedEvent(AgentEvent):
    type: str = "QuizSkipped"
    reason: str = ""
