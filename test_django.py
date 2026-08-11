import asyncio
import httpx

async def test_django():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://127.0.0.1:8000/api/courses/")
            print("Django status:", response.status_code)
            print("Response:", response.text[:200])
    except Exception as e:
        print("Django Error:", e)

async def test_fastapi():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://127.0.0.1:8001/api/health")
            print("FastAPI status:", response.status_code)
            print("Response:", response.text[:200])
    except Exception as e:
        print("FastAPI Error:", e)

async def test_fastapi_chat():
    try:
        async with httpx.AsyncClient() as client:
            payload = {
                "query": "Suggest SOC courses",
                "stream": False,
                "user_id": "demo_user"
            }
            response = await client.post("http://127.0.0.1:8001/api/chat/", json=payload, timeout=20.0)
            print("FastAPI Chat status:", response.status_code)
            print("Chat Response:", response.text[:300])
    except Exception as e:
        print("FastAPI Chat Error:", e)

if __name__ == "__main__":
    asyncio.run(test_django())
    asyncio.run(test_fastapi())
    asyncio.run(test_fastapi_chat())
