import logging
from typing import Dict, List, Optional, Any
from app.services.workflow.workflow_step import WorkflowStep

logger = logging.getLogger(__name__)

class WorkflowEngine:
    """
    Defines a workflow containing multiple steps and their dependencies.
    """
    def __init__(self, workflow_id: str):
        self.workflow_id = workflow_id
        self.steps: Dict[str, WorkflowStep] = {}
        
    def add_step(self, step: WorkflowStep) -> None:
        if step.name in self.steps:
            raise ValueError(f"Step '{step.name}' already exists in workflow '{self.workflow_id}'")
        self.steps[step.name] = step
        logger.debug(f"Added step '{step.name}' to workflow '{self.workflow_id}'")
        
    def get_independent_steps(self, completed_steps: set) -> List[WorkflowStep]:
        """
        Returns steps whose dependencies are met and haven't been completed yet.
        """
        ready_steps = []
        for name, step in self.steps.items():
            if name in completed_steps:
                continue
            # Check if all dependencies are in completed_steps
            if all(dep in completed_steps for dep in step.depends_on):
                ready_steps.append(step)
        return ready_steps
        
    def validate(self) -> None:
        """
        Validates the workflow graph for missing dependencies or cycles.
        """
        # Validate missing dependencies
        for name, step in self.steps.items():
            for dep in step.depends_on:
                if dep not in self.steps:
                    raise ValueError(f"Step '{name}' depends on non-existent step '{dep}'")
                    
        # Cycle detection
        visited = set()
        stack = set()
        
        def visit(node: str):
            if node in stack:
                raise ValueError(f"Cycle detected involving step '{node}'")
            if node in visited:
                return
            stack.add(node)
            for dep in self.steps[node].depends_on:
                visit(dep)
            stack.remove(node)
            visited.add(node)
            
        for name in self.steps.keys():
            if name not in visited:
                visit(name)
