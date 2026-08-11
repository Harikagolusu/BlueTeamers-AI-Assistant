from typing import Any
from app.models.chat.chat_models import ExecutionResult

from app.agents.reflection.pipeline import (
    ReflectionPipeline, OutputValidationStage, 
    ConstraintValidationStage, PolicyValidationStage
)

class ReflectionService:
    """
    Evaluates the execution result of a step by running it through the reflection pipeline.
    """
    _pipeline = ReflectionPipeline([
        OutputValidationStage(),
        ConstraintValidationStage(),
        PolicyValidationStage()
    ])

    @classmethod
    def evaluate_step(cls, result: ExecutionResult) -> bool:
        return cls._pipeline.evaluate(result)
