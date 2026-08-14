from app.chat.interfaces.i_execution_stage import IExecutionStage
from app.chat.context.execution_context import ExecutionContext
from app.models.chat.chat_models import ExecutionResult
from app.cache.interfaces import ICacheService
from app.multilingual.languages import is_concrete_code

class CacheStage(IExecutionStage):
    """Checks semantic cache. If hit, populates execution_result directly."""
    
    def __init__(self, cache_service: ICacheService):
        self._cache = cache_service

    @property
    def name(self) -> str:
        return "Cache"

    @staticmethod
    def _key_for(query: str, language: str, scope: str = "") -> str:
        """Namespace cached responses by explicit response language so a cached
        English answer is never served to a request answered in, say, Telugu.

        ``scope`` is the caller identity (authenticated user or guest client
        id). Personalized responses (name, enrollments, progress) must never be
        served to a different caller, so the scope participates in the key.
        """
        key = query
        if is_concrete_code(language):
            key = f"lang:{language}|{query}"
        if scope:
            key = f"scope:{scope}|{key}"
        return key

    async def execute(self, context: ExecutionContext) -> ExecutionContext:
        # Never overwrite a result produced upstream (e.g. a guardrail block).
        if "execution_result" in context.metadata:
            return context

        query = context.metadata.get("query", "")
        if not query:
            return context

        # Identity scope: authenticated user id, else the guest client id, else
        # anonymous. Cache hits must never cross identities.
        scope = context.session_user or (context.metadata.get("client_id") or "") or "anon"
        key = self._key_for(query, context.metadata.get("language", ""), scope=scope)
        cached_response = await self._cache.get(key)
        if cached_response:
            result = ExecutionResult.success(
                engine="CACHE",
                message=cached_response,
                metadata={"cache_hit": True}
            )
            new_metadata = {**context.metadata, "execution_result": result}
            return context.model_copy(update={"metadata": new_metadata})

        return context
