import asyncio
from unittest.mock import AsyncMock
from app.chat.engines.general_engine import GeneralExecutionEngine
from app.chat.context.execution_context import ExecutionContext
from app.models.chat.chat_models import ExecutionResult

def build(mock_llm):
    # This simulates build_stress_pipeline capturing mock_llm
    class Factory:
        def create(self):
            return GeneralExecutionEngine(mock_llm, AsyncMock())
    return Factory()

async def test():
    mocks = {"llm": AsyncMock()}
    
    # build pipeline
    factory = build(mocks["llm"])
    
    # test modifies mock AFTER pipeline is built
    mocks["llm"].generate.return_value = "General OK"
    
    # execute
    engine = factory.create()
    
    ctx = ExecutionContext()
    
    try:
        res = await engine.execute(ctx)
        print(f"Success: {res.message}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test())
