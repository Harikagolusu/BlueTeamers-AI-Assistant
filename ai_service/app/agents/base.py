from abc import abstractmethod
from typing import List, Dict, Any
import time

from app.agents.base_interfaces import IAgent
from app.agents.context import AgentContext
from app.agents.models.agent_models import AgentResult, AgentState
from app.shared.models.communication import AgentRequest, AgentResponse
from app.agents.manifests.models import AgentManifest
from app.agents.events.event_bus import agent_event_bus
from app.agents.events.agent_events import (
    AgentStartedEvent, PlanningStartedEvent, PlanningCompletedEvent,
    RetrievalStartedEvent, RetrievalCompletedEvent, LLMStartedEvent, LLMCompletedEvent,
    MemoryWriteEvent, ResponseGeneratedEvent, AgentCompletedEvent, AgentFailedEvent
)

class BaseAgent(IAgent):
    """
    Abstract base class enforcing the 13-step Agent Lifecycle.
    """
    def __init__(self, manifest: AgentManifest):
        self.manifest = manifest
        self.state = AgentState.IDLE
        self._events_to_publish: List[Any] = []

    def _transition_state(self, new_state: AgentState):
        valid_transitions = {
            AgentState.IDLE: [AgentState.PLANNING, AgentState.CANCELLED, AgentState.FAILED],
            AgentState.PLANNING: [AgentState.RETRIEVING, AgentState.CANCELLED, AgentState.FAILED],
            AgentState.RETRIEVING: [AgentState.EXECUTING, AgentState.CANCELLED, AgentState.FAILED],
            AgentState.EXECUTING: [AgentState.WAITING, AgentState.COMPLETED, AgentState.CANCELLED, AgentState.FAILED],
            AgentState.WAITING: [AgentState.EXECUTING, AgentState.COMPLETED, AgentState.CANCELLED, AgentState.FAILED],
            AgentState.COMPLETED: [],
            AgentState.FAILED: [],
            AgentState.CANCELLED: []
        }
        
        if new_state not in valid_transitions.get(self.state, []):
            raise ValueError(f"Invalid state transition: Cannot move from {self.state.value} to {new_state.value}")
        self.state = new_state

    async def execute(self, context: AgentContext) -> AgentResult:
        self.state = AgentState.IDLE
        start_time = time.time()
        self._context = context
        
        session_id = context.conversation.session_id
        
        try:
            self._publish_immediate(AgentStartedEvent(session_id=session_id))
            
            await self.initialize()
            await self.validate()
            await self.prepare_context()
            
            self._transition_state(AgentState.PLANNING)
            self._publish_immediate(PlanningStartedEvent(session_id=session_id))
            await self.plan()
            self._publish_immediate(PlanningCompletedEvent(session_id=session_id))
            
            self._transition_state(AgentState.RETRIEVING)
            self._publish_immediate(RetrievalStartedEvent(session_id=session_id))
            await self.retrieve()
            self._publish_immediate(RetrievalCompletedEvent(session_id=session_id))
            
            self._transition_state(AgentState.EXECUTING)
            tools = await self.select_tools()
            await self.execute_tools(tools)
            
            self._publish_immediate(LLMStartedEvent(session_id=session_id))
            result = await self.reason()
            self._publish_immediate(LLMCompletedEvent(session_id=session_id))
            
            final_response = await self.post_process(result)
            
            self._publish_immediate(MemoryWriteEvent(session_id=session_id))
            await self.update_memory(final_response)
            
            self._publish_immediate(ResponseGeneratedEvent(session_id=session_id))
            self._transition_state(AgentState.COMPLETED)
            self._publish_immediate(AgentCompletedEvent(session_id=session_id))
            
            execution_time = time.time() - start_time
            return AgentResult(
                success=True,
                response=final_response,
                execution_time=execution_time,
                events=self._events_to_publish
            )
            
        except Exception as e:
            self._transition_state(AgentState.FAILED)
            self._publish_immediate(AgentFailedEvent(session_id=session_id, error=str(e)))
            return AgentResult(
                success=False,
                response="",
                errors=[str(e)],
                execution_time=time.time() - start_time
            )
        finally:
            await self.publish_events()
            await self.cleanup()

    async def handle_request(self, request: AgentRequest, context: AgentContext) -> AgentResponse:
        """
        New standardized execution pipeline using AgentRequest and AgentResponse.
        Defaults to wrapping the legacy execute() method for backward compatibility.
        """
        # Call legacy execute
        legacy_result = await self.execute(context)
        
        return AgentResponse(
            request_id=request.request_id,
            success=legacy_result.success,
            data=legacy_result.response,
            errors=legacy_result.errors if hasattr(legacy_result, 'errors') else None
        )

    def _publish_immediate(self, event: Any):
        agent_event_bus.publish(event)
        self._events_to_publish.append(event.model_dump() if hasattr(event, "model_dump") else event.dict())

    # --- Lifecycle Hooks ---
    async def initialize(self) -> None: pass
    async def validate(self) -> None: pass
    async def prepare_context(self) -> None: pass
    async def plan(self) -> None: pass
    async def retrieve(self) -> None: pass
    async def select_tools(self) -> List[Any]: return []
    async def execute_tools(self, tools: List[Any]) -> None: pass
    
    @abstractmethod
    async def reason(self) -> Any: 
        """Core LLM reasoning step."""
        pass
        
    async def post_process(self, result: Any) -> str: return str(result)
    async def update_memory(self, final_response: str) -> None: pass
    async def publish_events(self) -> None: pass
    async def cleanup(self) -> None: pass
