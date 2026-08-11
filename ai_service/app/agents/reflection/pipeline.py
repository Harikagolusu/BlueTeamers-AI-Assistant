from typing import List
from app.models.chat.chat_models import ExecutionResult
from app.agents.reflection.interfaces import IReflectionStage

class ReflectionPipeline:
    """Composes multiple IReflectionStage instances to evaluate execution results."""
    def __init__(self, stages: List[IReflectionStage]):
        self.stages = stages

    def evaluate(self, result: ExecutionResult) -> bool:
        for stage in self.stages:
            if not stage.validate(result):
                return False
        return True

class OutputValidationStage(IReflectionStage):
    """Ensures the output format and status are basically valid."""
    def validate(self, result: ExecutionResult) -> bool:
        if result.status == "FAILED":
            return False
        if not result.message or len(result.message.strip()) == 0:
            return False
        return True

class ConstraintValidationStage(IReflectionStage):
    """Placeholder for checking output constraints (e.g., token limits, schema)."""
    def validate(self, result: ExecutionResult) -> bool:
        return True

class PolicyValidationStage(IReflectionStage):
    """Placeholder for checking against safety or organizational policies."""
    def validate(self, result: ExecutionResult) -> bool:
        return True
