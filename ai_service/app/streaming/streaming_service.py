import json
import logging
import asyncio
import time
from typing import AsyncGenerator, Union, Optional
from app.rag.service import RAGService
from app.rag.schemas import RAGRequest, RAGResponse
from app.memory.memory_service import MemoryService
from app.cache.cache_service import CacheService
from app.memory.models import MessageRole
from app.streaming.interfaces import BaseStreamingService
from app.streaming.models import StreamEvent, StreamEventType, TokenEvent, CompletionEvent, ErrorEvent
from app.streaming.exceptions import StreamCancellationException
from app.observability.service import ObservabilityService
from app.core.config import settings

logger = logging.getLogger("app.streaming.service")

class StreamingService(BaseStreamingService):
    def __init__(self, rag_service: RAGService, memory_service: MemoryService, cache_service: Optional[CacheService] = None, obs: Optional[ObservabilityService] = None):
        self.rag_service = rag_service
        self.memory_service = memory_service
        self.cache_service = cache_service
        self.obs = obs

    def _format_sse(self, event: StreamEvent) -> str:
        # Convert pydantic model to json string inside SSE format
        # Pydantic v2 model_dump_json
        return f"data: {event.model_dump_json()}\n\n"

    async def stream_chat(self, request: RAGRequest, conversation_id: Optional[str] = None) -> AsyncGenerator[str, None]:
        full_response_text = ""
        start_time = time.time()
        
        if self.obs:
            self.obs.increment_gauge("streaming_connections_active", 1.0, {"endpoint": "/stream"})
        
        try:
            # 1. Cache Lookup
            if self.cache_service and self.cache_service.enabled:
                cached_res = await self.cache_service.get_cached_response(request)
                if cached_res:
                    logger.info(f"Replaying cached stream for request: {request.request_id}")
                    chunk_size = 30
                    answer = cached_res.answer
                    for i in range(0, len(answer), chunk_size):
                        chunk = answer[i:i+chunk_size]
                        event = StreamEvent(
                            event=StreamEventType.TOKEN,
                            data=TokenEvent(content=chunk)
                        )
                        yield self._format_sse(event)
                        # Small deterministic yield sleep to simulate typing
                        delay = settings.STREAMING_CACHE_DELAY_MS / 1000.0
                        await asyncio.sleep(delay)
                    
                    event = StreamEvent(
                        event=StreamEventType.COMPLETION,
                        data=CompletionEvent(
                            citations=cached_res.citations,
                            metrics=cached_res.metrics
                        )
                    )
                    yield self._format_sse(event)
                    return # DO NOT persist memory on cache hit

            # 2. Start RAG Stream
            # RAG Engine yields `str` tokens, and as the last item, a `RAGResponse` object with metadata.
            logger.info(f"StreamingService starting stream for request: {request.request_id}")
            
            async for chunk in self.rag_service.stream_answer(request):
                if isinstance(chunk, str):
                    full_response_text += chunk
                    event = StreamEvent(
                        event=StreamEventType.TOKEN,
                        data=TokenEvent(content=chunk)
                    )
                    sse_payload = self._format_sse(event)
                    if self.obs:
                        self.obs.increment_counter("streaming_throughput_bytes", float(len(sse_payload.encode('utf-8'))))
                    yield sse_payload
                    
                elif isinstance(chunk, RAGResponse):
                    # It's the final metadata package
                    event = StreamEvent(
                        event=StreamEventType.COMPLETION,
                        data=CompletionEvent(
                            citations=chunk.citations,
                            metrics=chunk.metrics
                        )
                    )
                    sse_payload = self._format_sse(event)
                    if self.obs:
                        self.obs.increment_counter("streaming_throughput_bytes", float(len(sse_payload.encode('utf-8'))))
                    yield sse_payload
                    
                    if self.cache_service:
                        await self.cache_service.set_cached_response(request, chunk)

            # 3. Persist Memory Post-Stream
            if conversation_id and full_response_text:
                await self.memory_service.append_message(
                    session_id=conversation_id,
                    role=MessageRole.USER,
                    content=request.query
                )
                await self.memory_service.append_message(
                    session_id=conversation_id,
                    role=MessageRole.ASSISTANT,
                    content=full_response_text
                )
                
            logger.info(f"StreamingService completed successfully for request: {request.request_id}")

        except asyncio.CancelledError:
            logger.warning(f"Client disconnected. Stream cancelled for request: {request.request_id}")
            # Do NOT persist partial messages
            raise StreamCancellationException("Client disconnected")
            
        except Exception as e:
            logger.error(f"Stream failed for request: {request.request_id} - Error: {str(e)}")
            if self.obs:
                self.obs.increment_counter("streaming_errors_total", 1.0)
            event = StreamEvent(
                event=StreamEventType.ERROR,
                data=ErrorEvent(detail="An internal streaming error occurred.")
            )
            yield self._format_sse(event)
            # Do not persist on failure
            raise e
        finally:
            if self.obs:
                duration = time.time() - start_time
                self.obs.decrement_gauge("streaming_connections_active", 1.0, {"endpoint": "/stream"})
                self.obs.observe_histogram("streaming_duration_seconds", duration)
            
    async def health_check(self) -> dict:
        return {
            "status": "healthy",
            "module": "streaming"
        }
