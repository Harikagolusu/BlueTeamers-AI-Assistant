import asyncio
from unittest.mock import AsyncMock, MagicMock
from app.chat.engines.general_engine import GeneralExecutionEngine
from app.chat.context.execution_context import ExecutionContext

async def debug_test():
    mock_llm = AsyncMock()
    # Pydantic V2 is strict. Let's see if setting return_value to string works.
    mock_llm.generate.return_value = "General OK"
    
    mock_prompt_builder = MagicMock()
    mock_prompt_builder.build_prompt.return_value = "prompt"
    
    engine = GeneralExecutionEngine(mock_llm, mock_prompt_builder)
    
    context = ExecutionContext(metadata={"query": "test"})
    result = await engine.execute(context)
    print(f"Result: {result.message}")

if __name__ == "__main__":
    asyncio.run(debug_test())
