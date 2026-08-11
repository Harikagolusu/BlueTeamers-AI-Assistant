from typing import Optional
from app.agents.models.cursor import ExecutionCursor
from app.planning.models.plan import ExecutionPlan, ExecutionStep
from app.agents.interfaces.i_scheduler import IScheduler

class SequentialScheduler(IScheduler):
    """Yields one step at a time from the cursor's ready queue."""
    
    def get_next_step(self, plan: ExecutionPlan, cursor: ExecutionCursor) -> Optional[ExecutionStep]:
        if cursor.current_node:
            return None # Already executing a node
            
        if not cursor.ready_queue:
            return None # Nothing ready
            
        # Take the first ready node
        next_id = cursor.ready_queue.pop(0)
        cursor.current_node = next_id
        
        return next((s for s in plan.steps if s.step_id == next_id), None)
