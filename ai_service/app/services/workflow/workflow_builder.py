import uuid
from typing import Callable, Any, List
from app.services.workflow.workflow_engine import WorkflowEngine
from app.services.workflow.workflow_step import WorkflowStep
from app.services.workflow.workflow_context import WorkflowContext

class FunctionStep(WorkflowStep):
    """
    A generic step that wraps a callable.
    """
    def __init__(self, name: str, func: Callable, depends_on: List[str] = None, timeout: int = 0, retries: int = 0):
        super().__init__(name, depends_on, timeout, retries)
        self.func = func
        
    async def execute(self, context: WorkflowContext) -> Any:
        if asyncio.iscoroutinefunction(self.func):
            return await self.func(context)
        return self.func(context)

import asyncio # Needed for FunctionStep check

class WorkflowBuilder:
    """
    Fluent builder for workflows.
    """
    def __init__(self, workflow_id: str = None):
        self.workflow_id = workflow_id or str(uuid.uuid4())
        self.engine = WorkflowEngine(self.workflow_id)
        
    def add_step(self, step: WorkflowStep) -> 'WorkflowBuilder':
        self.engine.add_step(step)
        return self
        
    def add_function_step(
        self, 
        name: str, 
        func: Callable, 
        depends_on: List[str] = None, 
        timeout: int = 0, 
        retries: int = 0
    ) -> 'WorkflowBuilder':
        step = FunctionStep(name, func, depends_on, timeout, retries)
        self.engine.add_step(step)
        return self
        
    def build(self) -> WorkflowEngine:
        self.engine.validate()
        return self.engine
