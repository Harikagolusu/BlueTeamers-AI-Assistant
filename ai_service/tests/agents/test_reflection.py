from app.models.chat.chat_models import ExecutionResult
from app.agents.reflection.reflection_service import ReflectionService

def test_reflection_evaluates_success():
    result = ExecutionResult.success(engine="TEST", message="Valid output")
    assert ReflectionService.evaluate_step(result) is True

def test_reflection_evaluates_failure():
    result = ExecutionResult.failed("TEST", [{"error": "fail"}])
    assert ReflectionService.evaluate_step(result) is False

def test_reflection_evaluates_empty_as_failure():
    result = ExecutionResult.success(engine="TEST", message="   ")
    assert ReflectionService.evaluate_step(result) is False
