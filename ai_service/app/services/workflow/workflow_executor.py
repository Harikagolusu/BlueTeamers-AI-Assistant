import asyncio
import logging
import time
from typing import Dict, List, Set, Any
from app.services.workflow.workflow_engine import WorkflowEngine
from app.services.workflow.workflow_context import WorkflowContext
from app.services.workflow.workflow_state import WorkflowState
from app.services.workflow.workflow_result import WorkflowResult

logger = logging.getLogger(__name__)

class WorkflowExecutor:
    """
    Executes a WorkflowEngine asynchronously, supporting parallel steps and dependency tracking.
    """
    def __init__(self, engine: WorkflowEngine):
        self.engine = engine
        
    async def execute(self, context: WorkflowContext) -> WorkflowResult:
        start_time = time.time()
        logger.info(f"Starting execution of workflow '{self.engine.workflow_id}' for session '{context.session_id}'")
        
        try:
            self.engine.validate()
        except Exception as e:
            logger.error(f"Workflow validation failed: {e}")
            return WorkflowResult(
                workflow_id=self.engine.workflow_id,
                success=False,
                state=WorkflowState.FAILED,
                errors=[str(e)]
            )
            
        completed_steps: Set[str] = set()
        in_progress_tasks: Dict[str, asyncio.Task] = {}
        errors: List[str] = []
        
        while len(completed_steps) < len(self.engine.steps):
            # Check for newly ready steps
            ready_steps = self.engine.get_independent_steps(completed_steps)
            for step in ready_steps:
                if step.name not in in_progress_tasks:
                    logger.debug(f"Scheduling step '{step.name}'")
                    # Schedule step execution
                    task = asyncio.create_task(self._run_step(step, context))
                    in_progress_tasks[step.name] = task
                    
            if not in_progress_tasks:
                if len(completed_steps) < len(self.engine.steps):
                    msg = "Deadlock detected: No tasks in progress and uncompleted steps remain."
                    logger.error(msg)
                    errors.append(msg)
                    break
                    
            # Wait for at least one task to complete
            done, pending = await asyncio.wait(
                in_progress_tasks.values(), 
                return_when=asyncio.FIRST_COMPLETED
            )
            
            # Process completed tasks
            for task in done:
                # Find the step name corresponding to this task
                step_name = next(name for name, t in in_progress_tasks.items() if t == task)
                del in_progress_tasks[step_name]
                
                try:
                    result = task.result()
                    context.set_step_output(step_name, result)
                    completed_steps.add(step_name)
                    logger.debug(f"Step '{step_name}' completed.")
                except Exception as e:
                    logger.error(f"Step '{step_name}' failed with exception: {e}")
                    errors.append(f"Step '{step_name}' failed: {e}")
                    # Fast fail workflow if a step fails
                    for pending_task in pending:
                        pending_task.cancel()
                    
                    return WorkflowResult(
                        workflow_id=self.engine.workflow_id,
                        success=False,
                        state=WorkflowState.FAILED,
                        errors=errors,
                        execution_time=time.time() - start_time
                    )
                    
        success = len(errors) == 0
        state = WorkflowState.COMPLETED if success else WorkflowState.FAILED
        
        logger.info(f"Workflow '{self.engine.workflow_id}' completed with status: {state.value}")
        return WorkflowResult(
            workflow_id=self.engine.workflow_id,
            success=success,
            state=state,
            output=context.step_outputs, # Return all step outputs as the final output
            errors=errors,
            execution_time=time.time() - start_time
        )
        
    async def _run_step(self, step, context: WorkflowContext) -> Any:
        return await step.run_with_retry(context)
