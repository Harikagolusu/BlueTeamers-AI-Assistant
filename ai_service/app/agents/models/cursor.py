from pydantic import BaseModel, Field
from typing import List, Set, Dict, Optional
from app.planning.models.plan import ExecutionPlan

class ExecutionCursor(BaseModel):
    """Tracks the state of execution through the ExecutionPlan DAG."""
    plan_id: str
    current_node: Optional[str] = None
    ready_queue: List[str] = Field(default_factory=list)
    blocked_nodes: Set[str] = Field(default_factory=set)
    completed_nodes: Set[str] = Field(default_factory=set)
    failed_nodes: Set[str] = Field(default_factory=set)

    @classmethod
    def initialize(cls, plan: ExecutionPlan) -> "ExecutionCursor":
        blocked = set()
        ready = []
        for step in plan.steps:
            if not step.dependencies:
                ready.append(step.step_id)
            else:
                blocked.add(step.step_id)
                
        return cls(
            plan_id=plan.plan_id,
            ready_queue=ready,
            blocked_nodes=blocked
        )

    def mark_completed(self, step_id: str, plan: ExecutionPlan):
        self.completed_nodes.add(step_id)
        if self.current_node == step_id:
            self.current_node = None
            
        # Re-evaluate blocked nodes
        new_ready = []
        for blocked_id in list(self.blocked_nodes):
            step = next((s for s in plan.steps if s.step_id == blocked_id), None)
            if step and all(dep in self.completed_nodes for dep in step.dependencies):
                new_ready.append(blocked_id)
                
        for ready_id in new_ready:
            self.blocked_nodes.remove(ready_id)
            if ready_id not in self.ready_queue:
                self.ready_queue.append(ready_id)

    def mark_failed(self, step_id: str):
        self.failed_nodes.add(step_id)
        if self.current_node == step_id:
            self.current_node = None
