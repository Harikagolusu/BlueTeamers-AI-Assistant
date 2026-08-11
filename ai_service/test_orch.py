import asyncio
from app.chat.bootstrap import get_chat_service
from app.models.chat.chat_models import ChatRequest

async def test_orchestrator():
    chat_service = get_chat_service()
    req = ChatRequest(message="What is threat intelligence?", stream=False)
    res = await chat_service.process_request(req)
    print("Response:")
    print(res.message)

asyncio.run(test_orchestrator())
