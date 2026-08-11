import httpx
import asyncio

async def test():
    async with httpx.AsyncClient() as client:
        resp = await client.post('http://localhost:8000/api/v1/chat', json={"query": "Hello", "stream": False}, timeout=60.0)
        print("Status: " + str(resp.status_code))
        print(resp.text)
        
        # Test stream
        async with client.stream('POST', 'http://localhost:8000/api/v1/chat', json={"query": "Give me a long answer.", "stream": True}, timeout=60.0) as r:
            print("Stream Status: " + str(r.status_code))
            async for chunk in r.aiter_text():
                print(chunk, end="")

asyncio.run(test())
