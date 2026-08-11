import time
import logging

from app.rag.base import BaseRAGEngine
from app.rag.schemas import RAGRequest, RAGResponse, RAGContext, SourceCitation, PipelineMetrics
from app.rag.validator import ResponseValidator
from app.rag.exceptions import (
    RetrievalFailure, ContextFailure, PromptFailure, 
    GenerationFailure, EmptyContextException, OrchestrationFailure
)

from app.retrieval.base import BaseRetriever
from app.retrieval.schemas import RetrievalRequest

from app.context.base import BaseContextBuilder
from app.context.schemas import ContextRequest

from app.prompt_builder.base import BasePromptBuilder
from app.prompt_builder.schemas import PromptRequest

from app.llm.base import BaseLLMProvider
from app.llm.schemas import LLMRequest
from app.observability.service import ObservabilityService
from typing import Optional

logger = logging.getLogger("app.rag.engine")

class RAGEngine(BaseRAGEngine):
    """
    The orchestrator.
    Stateless workflow engine coordinating the pipeline sequence.
    """
    def __init__(
        self,
        retrieval: BaseRetriever,
        context: BaseContextBuilder,
        prompt: BasePromptBuilder,
        llm: BaseLLMProvider,
        validator: ResponseValidator,
        obs: Optional[ObservabilityService] = None
    ):
        self.retrieval = retrieval
        self.context = context
        self.prompt = prompt
        self.llm = llm
        self.validator = validator
        self.obs = obs

    def _llm_labels(self, **extra) -> dict:
        """Prometheus-style label set derived from the active LLM provider config."""
        labels = {
            "provider": getattr(self.llm, "provider_name", "unknown"),
            "model": getattr(self.llm, "model", "default"),
        }
        labels.update(extra)
        return labels

    def generate_answer(self, request: RAGRequest) -> RAGResponse:
        start_total = time.time()
        
        # Initialize Internal RAGContext
        # Note: request.request_id is guaranteed by RAGService at this point.
        req_id_str = str(request.request_id) if request.request_id else "unknown"
        
        rag_ctx = RAGContext(
            request_id=req_id_str,
            original_request=request
        )
        
        logger.info(f"RAGEngine [Req: {req_id_str}] - Starting Pipeline for query: <hidden>")

        # 1. Retrieval Stage
        t0 = time.time()
        try:
            ret_req = RetrievalRequest(
                query=request.query,
                top_k=request.top_k,
                metadata_filters=request.metadata_filters
            )
            rag_ctx.retrieval_response = self.retrieval.retrieve(ret_req)
        except Exception as e:
            raise RetrievalFailure(f"Retrieval stage failed: {str(e)}")
        finally:
            rag_ctx.metrics.retrieval_latency_ms = (time.time() - t0) * 1000

        if not rag_ctx.retrieval_response.results:
            # We could return a canned response or throw. 
            # The design specifies throwing EmptyContextException on empty.
            raise EmptyContextException("No context retrieved for the given query.")

        # 2. Context Builder Stage
        t0 = time.time()
        try:
            ctx_req = ContextRequest(chunks=rag_ctx.retrieval_response.results)
            ctx_res = self.context.build_context(ctx_req)
            rag_ctx.context_document = ctx_res.document
        except Exception as e:
            raise ContextFailure(f"Context building failed: {str(e)}")
        finally:
            rag_ctx.metrics.context_latency_ms = (time.time() - t0) * 1000
            
        # Extract citations
        for c in rag_ctx.context_document.chunks:
            citation = SourceCitation(
                course=c.metadata.get("course_slug", "unknown"),
                lesson=c.metadata.get("lesson_id", "unknown"),
                chunk_id=c.id,
                similarity_score=c.score,
                source_title=c.metadata.get("lesson_title", "unknown")
            )
            rag_ctx.citations.append(citation)

        # 3. Prompt Builder Stage
        t0 = time.time()
        try:
            prompt_req = PromptRequest(
                query=request.query,
                context=rag_ctx.context_document,
                template_name=request.template_name
            )
            prompt_res = self.prompt.build_prompt(prompt_req)
            rag_ctx.prompt_payload = prompt_res.payload
        except Exception as e:
            raise PromptFailure(f"Prompt building failed: {str(e)}")
        finally:
            rag_ctx.metrics.prompt_latency_ms = (time.time() - t0) * 1000

        # 4. LLM Generation Stage
        t0 = time.time()
        try:
            llm_req = LLMRequest(
                system_prompt=rag_ctx.prompt_payload.system,
                prompt=rag_ctx.prompt_payload.user,
                temperature=0.0 # Deterministic answers
            )
            rag_ctx.llm_response = self.llm.generate(llm_req)
        except Exception as e:
            raise GenerationFailure(f"LLM Generation failed: {str(e)}")
        finally:
            rag_ctx.metrics.generation_latency_ms = (time.time() - t0) * 1000

        # 5. Validation Stage
        t0 = time.time()
        try:
            self.validator.validate(rag_ctx.llm_response, rag_ctx.context_document)
        # ValidationFailure is thrown directly by validator, pass it through.
        finally:
            rag_ctx.metrics.validation_latency_ms = (time.time() - t0) * 1000

        # Calculate Total
        rag_ctx.metrics.total_latency_ms = (time.time() - start_total) * 1000
        
        logger.info(
            f"RAGEngine [Req: {req_id_str}] - Pipeline Complete in {rag_ctx.metrics.total_latency_ms:.2f}ms"
        )
        
        if self.obs:
            self.obs.increment_counter("ai_llm_requests_total", 1.0, self._llm_labels(status="success"))
            self.obs.observe_histogram("ai_retrieval_duration_seconds", rag_ctx.metrics.retrieval_latency_ms / 1000.0, {"vector_store": "faiss"})
            self.obs.observe_histogram("ai_prompt_generation_seconds", rag_ctx.metrics.prompt_latency_ms / 1000.0)
            self.obs.observe_histogram("ai_context_building_seconds", rag_ctx.metrics.context_latency_ms / 1000.0)
            
            # New Detailed Metrics
            num_docs = len(rag_ctx.retrieval_response.results) if rag_ctx.retrieval_response else 0
            self.obs.observe_histogram("ai_retrieved_documents_count", float(num_docs), {"vector_store": "faiss"})
            
            context_size = sum(len(c.text.encode('utf-8')) for c in rag_ctx.context_document.chunks) if rag_ctx.context_document else 0
            self.obs.observe_histogram("ai_context_size_bytes", float(context_size))
            
            prompt_size = len(rag_ctx.prompt_payload.user.encode('utf-8')) + len(rag_ctx.prompt_payload.system.encode('utf-8')) if rag_ctx.prompt_payload else 0
            self.obs.observe_histogram("ai_prompt_size_bytes", float(prompt_size))
            
            self.obs.observe_histogram("ai_llm_provider_response_seconds", rag_ctx.metrics.generation_latency_ms / 1000.0, self._llm_labels())
            
            if rag_ctx.llm_response and rag_ctx.llm_response.usage:
                prompt_tokens = rag_ctx.llm_response.usage.get("prompt_tokens", 0)
                completion_tokens = rag_ctx.llm_response.usage.get("completion_tokens", 0)
                if prompt_tokens > 0:
                    self.obs.increment_counter("ai_llm_token_usage_total", float(prompt_tokens), self._llm_labels(type="prompt"))
                if completion_tokens > 0:
                    self.obs.increment_counter("ai_llm_token_usage_total", float(completion_tokens), self._llm_labels(type="completion"))

        return RAGResponse(
            query=request.query,
            answer=rag_ctx.llm_response.text,
            citations=rag_ctx.citations,
            metrics=rag_ctx.metrics
        )

    async def stream_answer(self, request: RAGRequest):
        from typing import Union
        start_total = time.time()
        
        req_id_str = str(request.request_id) if request.request_id else "unknown"
        rag_ctx = RAGContext(request_id=req_id_str, original_request=request)
        
        logger.info(f"RAGEngine [Req: {req_id_str}] - Starting Stream Pipeline")

        # 1. Retrieval Stage
        t0 = time.time()
        try:
            ret_req = RetrievalRequest(
                query=request.query,
                top_k=request.top_k,
                metadata_filters=request.metadata_filters
            )
            rag_ctx.retrieval_response = self.retrieval.retrieve(ret_req)
        except Exception as e:
            raise RetrievalFailure(f"Retrieval stage failed: {str(e)}")
        finally:
            rag_ctx.metrics.retrieval_latency_ms = (time.time() - t0) * 1000

        if not rag_ctx.retrieval_response.results:
            raise EmptyContextException("No context retrieved for the given query.")

        # 2. Context Builder Stage
        t0 = time.time()
        try:
            ctx_req = ContextRequest(chunks=rag_ctx.retrieval_response.results)
            ctx_res = self.context.build_context(ctx_req)
            rag_ctx.context_document = ctx_res.document
        except Exception as e:
            raise ContextFailure(f"Context building failed: {str(e)}")
        finally:
            rag_ctx.metrics.context_latency_ms = (time.time() - t0) * 1000
            
        for c in rag_ctx.context_document.chunks:
            citation = SourceCitation(
                course=c.metadata.get("course_slug", "unknown"),
                lesson=c.metadata.get("lesson_id", "unknown"),
                chunk_id=c.id,
                similarity_score=c.score,
                source_title=c.metadata.get("lesson_title", "unknown")
            )
            rag_ctx.citations.append(citation)

        # 3. Prompt Builder Stage
        t0 = time.time()
        try:
            prompt_req = PromptRequest(
                query=request.query,
                context=rag_ctx.context_document,
                template_name=request.template_name
            )
            prompt_res = self.prompt.build_prompt(prompt_req)
            rag_ctx.prompt_payload = prompt_res.payload
        except Exception as e:
            raise PromptFailure(f"Prompt building failed: {str(e)}")
        finally:
            rag_ctx.metrics.prompt_latency_ms = (time.time() - t0) * 1000

        # 4. LLM Generation Stage (Streaming)
        t0 = time.time()
        llm_req = LLMRequest(
            system_prompt=rag_ctx.prompt_payload.system,
            prompt=rag_ctx.prompt_payload.user,
            temperature=0.0
        )
        
        full_text = ""
        try:
            async for chunk in self.llm.stream_generate(llm_req):
                full_text += chunk
                yield chunk
        except Exception as e:
            raise GenerationFailure(f"LLM Stream Generation failed: {str(e)}")
        finally:
            rag_ctx.metrics.generation_latency_ms = (time.time() - t0) * 1000

        # We cannot easily run `self.validator.validate` on a stream piece-meal,
        # but we can validate the final aggregated text if we wish. 
        # For simplicity, we bypass text validation on stream or validate at end.
        rag_ctx.metrics.validation_latency_ms = 0.0

        rag_ctx.metrics.total_latency_ms = (time.time() - start_total) * 1000
        logger.info(f"RAGEngine [Req: {req_id_str}] - Stream Complete in {rag_ctx.metrics.total_latency_ms:.2f}ms")

        if self.obs:
            self.obs.increment_counter("ai_llm_requests_total", 1.0, self._llm_labels(status="success"))
            self.obs.observe_histogram("ai_retrieval_duration_seconds", rag_ctx.metrics.retrieval_latency_ms / 1000.0, {"vector_store": "faiss"})
            self.obs.observe_histogram("ai_prompt_generation_seconds", rag_ctx.metrics.prompt_latency_ms / 1000.0)
            self.obs.observe_histogram("ai_context_building_seconds", rag_ctx.metrics.context_latency_ms / 1000.0)
            
            # New Detailed Metrics
            num_docs = len(rag_ctx.retrieval_response.results) if rag_ctx.retrieval_response else 0
            self.obs.observe_histogram("ai_retrieved_documents_count", float(num_docs), {"vector_store": "faiss"})
            
            context_size = sum(len(c.text.encode('utf-8')) for c in rag_ctx.context_document.chunks) if rag_ctx.context_document else 0
            self.obs.observe_histogram("ai_context_size_bytes", float(context_size))
            
            prompt_size = len(rag_ctx.prompt_payload.user.encode('utf-8')) + len(rag_ctx.prompt_payload.system.encode('utf-8')) if rag_ctx.prompt_payload else 0
            self.obs.observe_histogram("ai_prompt_size_bytes", float(prompt_size))
            
            # For streaming, generation latency is time to complete the stream in the orchestrator
            self.obs.observe_histogram("ai_llm_provider_response_seconds", rag_ctx.metrics.generation_latency_ms / 1000.0, self._llm_labels())

        # Yield the final RAGResponse object (which is the project's existing response abstraction)
        yield RAGResponse(
            query=request.query,
            answer=full_text,
            citations=rag_ctx.citations,
            metrics=rag_ctx.metrics
        )
