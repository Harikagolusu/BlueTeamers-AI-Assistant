import httpx
import asyncio

async def test():
    async with httpx.AsyncClient() as client:
        # Test stream
        async with client.stream('POST', 'http://localhost:8000/api/v1/chat/stream', json={"query": "Hi", "stream": True}, timeout=60.0) as r:
            print("Stream Status: " + str(r.status_code))
            async for chunk in r.aiter_text():
                print(chunk, end="")

asyncio.run(test())
