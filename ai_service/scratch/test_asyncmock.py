import asyncio
from unittest.mock import AsyncMock

async def test():
    llm = AsyncMock()
    llm.generate.return_value = "General OK"
    
    # Simulate GeneralExecutionEngine
    response = await llm.generate("prompt")
    print(f"Response: {repr(response)}")
    print(f"Type: {type(response)}")

if __name__ == "__main__":
    asyncio.run(test())
