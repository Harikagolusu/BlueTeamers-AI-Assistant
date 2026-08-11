import pytest
from app.chat.context.execution_context import ExecutionContext
from app.chat.orchestrator import ChatOrchestrator
from app.chat.interfaces.i_execution_stage import IExecutionStage
from app.models.chat.chat_models import ExecutionResult

class MockStage(IExecutionStage):
    @property
    def name(self):
        return "Mock"

    async def execute(self, context: ExecutionContext) -> ExecutionContext:
        result = ExecutionResult.success(engine="MOCK", message="mock result")
        return context.copy(update={"metadata": {**context.metadata, "execution_result": result}})

@pytest.mark.asyncio
async def test_orchestrator_pipeline_execution():
    orchestrator = ChatOrchestrator(stages=[MockStage()])
    ctx = ExecutionContext()
    
    result = await orchestrator.execute_pipeline(ctx)
    
    assert result is not None
    assert result.status == "SUCCESS"
    assert result.engine_name == "MOCK"
    assert result.message == "mock result"

class CancellationStage(IExecutionStage):
    @property
    def name(self):
        return "Cancel"

    async def execute(self, context: ExecutionContext) -> ExecutionContext:
        return context.request_cancellation()

@pytest.mark.asyncio
async def test_orchestrator_cancellation():
    orchestrator = ChatOrchestrator(stages=[CancellationStage(), MockStage()])
    ctx = ExecutionContext()
    
    result = await orchestrator.execute_pipeline(ctx)
    
    # Because it was cancelled on stage 1, stage 2 (MockStage) never ran.
    # Therefore, no result is produced and orchestrator returns fallback failure.
    assert result.status == "FAILED"
    assert result.engine_name == "Orchestrator"
