import uuid
from typing import Optional
from datetime import datetime, timezone
from app.chat.interfaces.i_execution_engine import IExecutionEngine
from app.chat.context.execution_context import ExecutionContext
from app.models.chat.chat_models import ExecutionResult
from app.chat.engines.registry import ExecutionEngineFactory
from app.chat.engines.course_sources import build_course_sources
from app.planning.models.context import PlanningContext
from app.planning.models.plan import ExecutionPlan
from app.planning.interfaces.i_engine_resolver import IExecutionEngineResolver

from app.agents.models.agent_models import AgentState, StepExecution, AgentResult
from app.agents.models.session import AgentSession
from app.agents.events.event_bus import agent_event_bus
from app.agents.events.agent_events import (
    ExecutionStartedEvent, ExecutionCompletedEvent, StepStartedEvent,
    StepCompletedEvent, StepFailedEvent
)
from app.agents.interfaces.i_scheduler import IScheduler
from app.agents.lifecycle.checkpoint import CheckpointManager
from app.agents.reflection.reflection_service import ReflectionService
from app.agents.recovery.recovery_policy import RecoveryPolicy, RecoveryAction

class AgentExecutor(IExecutionEngine):
    """
    The master Agent orchestrator. Implements IExecutionEngine so it plugs cleanly 
    into the existing Pipeline, but internally acts as a stateful agent walking a plan.
    """
    def __init__(
        self, 
        engine_factory: ExecutionEngineFactory, 
        resolver: IExecutionEngineResolver,
        scheduler: IScheduler
    ):
        self._engine_factory = engine_factory
        self._resolver = resolver
        self._scheduler = scheduler

    @property
    def name(self) -> str:
        return "AGENT"

    async def execute(self, context: ExecutionContext) -> ExecutionResult:
        planning_context: PlanningContext = context.metadata.get("planning")
        if not planning_context or not planning_context.plan:
            return ExecutionResult.failed("AGENT", [{"error": "No ExecutionPlan found in context."}])
            
        plan: ExecutionPlan = planning_context.plan
        session = AgentSession.create(plan, runtime_context=context.metadata)
        
        agent_event_bus.publish(ExecutionStartedEvent(
            session_id=session.session_id,
            plan_id=plan.plan_id
        ))
        
        session.state = AgentState.EXECUTING
        session.journal.metrics.start_time = datetime.now(timezone.utc)
        session.journal.record("ExecutionStarted", {"plan_id": plan.plan_id})
        CheckpointManager.create_checkpoint(session, "START_EXECUTION")
        
        final_message = ""
        agent_errors = []
        
        while True:
            step = self._scheduler.get_next_step(session.plan, session.cursor)
            if not step:
                # No steps ready. Are we done or blocked?
                if session.cursor.blocked_nodes:
                    session.state = AgentState.FAILED
                    agent_errors.append("Deadlock: nodes are blocked but nothing is ready.")
                    break
                else:
                    session.state = AgentState.COMPLETED
                    break
                    
            agent_event_bus.publish(StepStartedEvent(session_id=session.session_id, step_id=step.step_id))
            session.journal.record("StepStarted", {"step_id": step.step_id})
            CheckpointManager.create_checkpoint(session, f"BEFORE_STEP_{step.step_id}")
            
            step_execution = StepExecution(step_id=step.step_id)
            session.history.append(step_execution)
            session.journal.metrics.steps_executed += 1
            
            # Execute the step with retries/recovery
            success = await self._execute_step_with_recovery(step, session, context)
            
            step_execution.completed_at = datetime.now(timezone.utc)
            step_execution.success = success
            
            if success:
                session.cursor.mark_completed(step.step_id, session.plan)
                output = session.memory.step_outputs.get(step.step_id)
                agent_event_bus.publish(StepCompletedEvent(
                    session_id=session.session_id, 
                    step_id=step.step_id,
                    output=output
                ))
                session.journal.record("StepCompleted", {"step_id": step.step_id, "output": output})
                CheckpointManager.create_checkpoint(session, f"AFTER_STEP_{step.step_id}")
            else:
                session.cursor.mark_failed(step.step_id)
                session.journal.metrics.failed_steps += 1
                agent_event_bus.publish(StepFailedEvent(
                    session_id=session.session_id, 
                    step_id=step.step_id,
                    error="Step execution failed."
                ))
                session.journal.record("StepFailed", {"step_id": step.step_id, "error": "Step execution failed."})
                CheckpointManager.create_checkpoint(session, f"AFTER_FAILURE_{step.step_id}")
                session.state = AgentState.FAILED
                agent_errors.append(f"Step {step.step_id} failed fatally.")
                break
                
        session.journal.metrics.end_time = datetime.now(timezone.utc)
        agent_event_bus.publish(ExecutionCompletedEvent(
            session_id=session.session_id,
            success=(session.state == AgentState.COMPLETED)
        ))
        session.journal.record("ExecutionCompleted", {"success": session.state == AgentState.COMPLETED})
        
        # Format output
        if session.state == AgentState.COMPLETED:
            # Output of the last step is usually the final response
            last_step_id = session.history[-1].step_id if session.history else None
            final_message = session.memory.step_outputs.get(last_step_id, "Plan completed successfully.")
            documents = session.memory.variables.get("documents", [])
            return ExecutionResult.success(
                engine="AGENT", 
                message=final_message,
                metadata={"course_sources": build_course_sources(documents)},
                citations=session.memory.variables.get("citations", []),
                documents=documents,
                tool_outputs=session.memory.variables.get("tool_outputs", [])
            )
        else:
            return ExecutionResult.failed("AGENT", [{"error": e} for e in agent_errors])

    async def _execute_step_with_recovery(self, step, session: AgentSession, context: ExecutionContext) -> bool:
        engine_name = self._resolver.resolve(step.required_capability)
        engine = self._engine_factory.create_engine(engine_name)
        
        retries = 0
        while True:
            last_exception = None
            try:
                # Inject accumulated step outputs into context metadata for the engine to consume
                # We also FORCE streaming_mode to False so the engine returns the actual text, not a generator.
                enriched_metadata = {**context.metadata, "previous_step_outputs": session.memory.step_outputs}
                step_context = context.model_copy(update={
                    "metadata": enriched_metadata,
                    "streaming_mode": False
                })
                
                # We execute the underlying engine.
                result = await engine.execute(step_context)
                
                # Reflection
                is_success = ReflectionService.evaluate_step(result)
                if is_success:
                    session.memory.step_outputs[step.step_id] = result.message
                    if result.citations:
                        session.memory.variables.setdefault("citations", []).extend(result.citations)
                    if result.documents:
                        session.memory.variables.setdefault("documents", []).extend(result.documents)
                    if result.tool_outputs:
                        session.memory.variables.setdefault("tool_outputs", []).extend(result.tool_outputs)
                    return True
                    
                error_msg = f"Reflection rejected output: {result.message}"
            except Exception as e:
                error_msg = str(e)
                last_exception = e
                
            # Recovery
            action = RecoveryPolicy.determine_action(session, step, retries)
            session.journal.record("RecoveryTriggered", {"step_id": step.step_id, "action": action.value})
            
            if action == RecoveryAction.RETRY_STEP:
                retries += 1
                session.journal.metrics.retry_count += 1
                session.journal.metrics.recovery_count += 1
                continue
            elif action == RecoveryAction.SKIP_STEP:
                session.journal.metrics.skipped_steps += 1
                session.journal.metrics.recovery_count += 1
                return True
            else:
                if last_exception:
                    raise last_exception
                return False
