import pytest
import asyncio
from unittest.mock import AsyncMock
from app.rag.schemas import RAGRequest, RAGResponse, PipelineMetrics
from app.cache.cache_store import InMemoryCacheStore
from app.cache.cache_service import CacheService
from app.streaming.streaming_service import StreamingService
from app.streaming.models import StreamEventType

def get_test_request(query="test"):
    return RAGRequest(query=query, request_id=None)

def get_test_response(answer="response"):
    return RAGResponse(query="test", answer=answer, citations=[], metrics=PipelineMetrics())

@pytest.mark.asyncio
async def test_cache_miss_and_hit():
    store = InMemoryCacheStore(max_size=10)
    service = CacheService(store=store, enabled=True, ttl=3600)
    
    req = get_test_request()
    res = get_test_response()
    
    # Miss
    assert await service.get_cached_response(req) is None
    
    # Set
    await service.set_cached_response(req, res)
    
    # Hit
    cached = await service.get_cached_response(req)
    assert cached is not None
    assert cached.answer == res.answer

@pytest.mark.asyncio
async def test_cache_disabled():
    store = InMemoryCacheStore(max_size=10)
    service = CacheService(store=store, enabled=False, ttl=3600)
    
    req = get_test_request()
    res = get_test_response()
    
    await service.set_cached_response(req, res)
    assert await service.get_cached_response(req) is None

@pytest.mark.asyncio
async def test_ttl_expiration():
    store = InMemoryCacheStore(max_size=10)
    service = CacheService(store=store, enabled=True, ttl=1) # 1 sec TTL
    
    req = get_test_request()
    res = get_test_response()
    
    await service.set_cached_response(req, res)
    assert await service.get_cached_response(req) is not None
    
    await asyncio.sleep(1.1)
    
    assert await service.get_cached_response(req) is None

@pytest.mark.asyncio
async def test_lru_eviction():
    store = InMemoryCacheStore(max_size=2)
    service = CacheService(store=store, enabled=True, ttl=3600)
    
    req1 = get_test_request("q1")
    req2 = get_test_request("q2")
    req3 = get_test_request("q3")
    
    res = get_test_response()
    
    await service.set_cached_response(req1, res)
    await service.set_cached_response(req2, res)
    assert await service.get_cached_response(req1) is not None # req1 becomes most recently used
    
    await service.set_cached_response(req3, res) # Should evict req2
    
    assert await service.get_cached_response(req1) is not None
    assert await service.get_cached_response(req3) is not None
    assert await service.get_cached_response(req2) is None

@pytest.mark.asyncio
async def test_concurrent_access():
    store = InMemoryCacheStore(max_size=100)
    service = CacheService(store=store, enabled=True, ttl=3600)
    
    res = get_test_response()
    
    async def worker(i):
        # Mixed reads and writes
        await service.set_cached_response(get_test_request(f"q{i}"), res)
        await service.get_cached_response(get_test_request(f"q{i}"))
        
    tasks = [worker(i) for i in range(500)]
    await asyncio.gather(*tasks)
    
    # Just ensuring it doesn't crash with ConcurrentModificationError or similar
    assert len(store._cache) == 100 # capped by max_size

@pytest.mark.asyncio
async def test_health_check():
    from app.cache.health import CacheHealthService
    store = InMemoryCacheStore(max_size=10)
    service = CacheService(store=store, enabled=True, ttl=3600)
    health = CacheHealthService(service)
    
    status = await health.check_health()
    assert status["status"] == "healthy"
    
@pytest.mark.asyncio
async def test_streaming_cache_replay():
    store = InMemoryCacheStore(max_size=10)
    cache_service = CacheService(store=store, enabled=True, ttl=3600)
    
    # Pre-populate cache
    req = get_test_request()
    res = get_test_response("This is a very long response that will be broken down into chunks of 30 characters.")
    await cache_service.set_cached_response(req, res)
    
    rag_mock = AsyncMock()
    mem_mock = AsyncMock()
    
    streaming_service = StreamingService(rag_service=rag_mock, memory_service=mem_mock, cache_service=cache_service)
    
    events = []
    async for chunk in streaming_service.stream_chat(req):
        events.append(chunk)
        
    # RAG should NOT be called
    rag_mock.stream_answer.assert_not_called()
    mem_mock.append_message.assert_not_called() # Memory is NOT mutated on replay
    
    assert len(events) > 1 # Token events + 1 completion
    assert "completion" in events[-1]

@pytest.mark.asyncio
async def test_cache_clear():
    store = InMemoryCacheStore(max_size=10)
    service = CacheService(store=store, enabled=True, ttl=3600)
    req = get_test_request("clear_me")
    await service.set_cached_response(req, get_test_response())
    
    assert await service.get_cached_response(req) is not None
    await service.clear()
    assert await service.get_cached_response(req) is None

@pytest.mark.asyncio
async def test_cache_delete():
    store = InMemoryCacheStore(max_size=10)
    service = CacheService(store=store, enabled=True, ttl=3600)
    req = get_test_request("delete_me")
    await service.set_cached_response(req, get_test_response())
    
    assert await service.get_cached_response(req) is not None
    await service.delete(req)
    assert await service.get_cached_response(req) is None

@pytest.mark.asyncio
async def test_deterministic_key_generation():
    store = InMemoryCacheStore(max_size=10)
    service = CacheService(store=store, enabled=True, ttl=3600, cache_version="v1", model_name="auto", prompt_template_version="v1")
    
    req1 = RAGRequest(query="test query", top_k=5)
    req2 = RAGRequest(query="test query", top_k=5)
    req3 = RAGRequest(query="test query", top_k=10)
    
    key1 = service.generate_key(req1)
    key2 = service.generate_key(req2)
    key3 = service.generate_key(req3)
    
    assert key1 == key2
    assert key1 != key3
    
    service_v2 = CacheService(store=store, enabled=True, ttl=3600, cache_version="v2", model_name="auto", prompt_template_version="v1")
    key1_v2 = service_v2.generate_key(req1)
    assert key1 != key1_v2

@pytest.mark.asyncio
async def test_serialization_deserialization():
    store = InMemoryCacheStore(max_size=10)
    service = CacheService(store=store, enabled=True, ttl=3600)
    
    req = get_test_request("serialize")
    res = get_test_response("test answer")
    res.metrics.total_latency_ms = 42.0
    
    await service.set_cached_response(req, res)
    cached = await service.get_cached_response(req)
    
    assert cached is not None
    assert cached.answer == "test answer"
    assert cached.metrics.total_latency_ms == 42.0

@pytest.mark.asyncio
async def test_concurrent_cache_hits():
    store = InMemoryCacheStore(max_size=10)
    service = CacheService(store=store, enabled=True, ttl=3600)
    
    req = get_test_request("concurrent_hits")
    res = get_test_response("concurrent")
    await service.set_cached_response(req, res)
    
    async def worker():
        return await service.get_cached_response(req)
        
    tasks = [worker() for _ in range(100)]
    results = await asyncio.gather(*tasks)
    
    assert all(r is not None and r.answer == "concurrent" for r in results)
    
    metrics = await service.get_metrics()
    assert metrics["cache_hits"] >= 100

@pytest.mark.asyncio
async def test_streaming_cache_disabled():
    store = InMemoryCacheStore(max_size=10)
    cache_service = CacheService(store=store, enabled=False, ttl=3600)
    
    req = get_test_request()
    res = get_test_response("Cached response that shouldn't be used")
    await cache_service.set_cached_response(req, res)
    
    rag_mock = AsyncMock()
    # mock stream_answer to return one chunk
    async def mock_stream_answer(req):
        yield "Live response"
        yield get_test_response("Live response")
    rag_mock.stream_answer = mock_stream_answer
    
    mem_mock = AsyncMock()
    streaming_service = StreamingService(rag_service=rag_mock, memory_service=mem_mock, cache_service=cache_service)
    
    events = []
    async for chunk in streaming_service.stream_chat(req):
        events.append(chunk)
        
    # RAG should be called because cache is disabled
    assert len(events) > 0
    assert "Live response" in str(events)
