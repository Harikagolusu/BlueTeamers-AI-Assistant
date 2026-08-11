from app.retrieval.base import BaseRetriever
from app.context.base import BaseContextBuilder
from app.prompt_builder.base import BasePromptBuilder
from app.llm.base import BaseLLMProvider
from app.rag.validator import ResponseValidator

class RAGHealthService:
    """
    Aggregates health across the 5 underlying dependencies.
    Performs NO orchestration or business logic.
    """
    def __init__(
        self,
        retrieval: BaseRetriever,
        context: BaseContextBuilder,
        prompt: BasePromptBuilder,
        llm: BaseLLMProvider,
        validator: ResponseValidator
    ):
        self.retrieval = retrieval
        self.context = context
        self.prompt = prompt
        self.llm = llm
        self.validator = validator

    async def check_health(self) -> dict:
        import inspect
        try:
            _ret_h = self.retrieval.health_check()
            ret_h = await _ret_h if inspect.isawaitable(_ret_h) else _ret_h
            
            _ctx_h = self.context.health_check()
            ctx_h = await _ctx_h if inspect.isawaitable(_ctx_h) else _ctx_h
            
            _prompt_h = self.prompt.health_check()
            prompt_h = await _prompt_h if inspect.isawaitable(_prompt_h) else _prompt_h
            
            _llm_h = self.llm.health_check()
            llm_h = await _llm_h if inspect.isawaitable(_llm_h) else _llm_h
            
            # Providers report health via "healthy" (bool) or "status" ("healthy")
            ret_ok = getattr(ret_h, "overall_health", False)
            ctx_ok = ctx_h.get("builder_status") == "healthy"
            prompt_ok = getattr(prompt_h, "template_status", "") == "healthy"
            llm_ok = llm_h.get("status") == "healthy" or bool(llm_h.get("healthy", False))
            
            overall = ret_ok and ctx_ok and prompt_ok and llm_ok
            
            return {
                "status": "healthy" if overall else "degraded",
                "retrieval": "healthy" if ret_ok else "unhealthy",
                "context": "healthy" if ctx_ok else "unhealthy",
                "prompt": "healthy" if prompt_ok else "unhealthy",
                "llm": "healthy" if llm_ok else "unhealthy",
                "validator": "healthy"  # Stateless validator is always healthy
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
