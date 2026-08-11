from fastapi import Depends

from app.retrieval.base import BaseRetriever
from app.retrieval.dependencies import get_retrieval_service

from app.context.base import BaseContextBuilder
from app.context.dependencies import get_context_builder

from app.prompt_builder.base import BasePromptBuilder
from app.prompt_builder.dependencies import get_prompt_builder

from app.llm.base import BaseLLMProvider
from app.llm.dependencies import get_llm_provider

from app.rag.validator import ResponseValidator
from app.rag.engine import RAGEngine
from app.rag.base import BaseRAGEngine
from app.rag.service import RAGService
from app.rag.health import RAGHealthService

def get_response_validator() -> ResponseValidator:
    return ResponseValidator()

from app.observability.service import ObservabilityService
from app.observability.dependencies import get_observability_service

def get_rag_engine(
    retrieval: BaseRetriever = Depends(get_retrieval_service),
    context: BaseContextBuilder = Depends(get_context_builder),
    prompt: BasePromptBuilder = Depends(get_prompt_builder),
    llm: BaseLLMProvider = Depends(get_llm_provider),
    validator: ResponseValidator = Depends(get_response_validator),
    obs: ObservabilityService = Depends(get_observability_service)
) -> BaseRAGEngine:
    return RAGEngine(retrieval, context, prompt, llm, validator, obs)

def get_rag_service(engine: BaseRAGEngine = Depends(get_rag_engine)) -> RAGService:
    return RAGService(engine)

def get_rag_health_service(
    retrieval: BaseRetriever = Depends(get_retrieval_service),
    context: BaseContextBuilder = Depends(get_context_builder),
    prompt: BasePromptBuilder = Depends(get_prompt_builder),
    llm: BaseLLMProvider = Depends(get_llm_provider),
    validator: ResponseValidator = Depends(get_response_validator)
) -> RAGHealthService:
    return RAGHealthService(retrieval, context, prompt, llm, validator)
