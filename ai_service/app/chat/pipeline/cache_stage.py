from app.chat.interfaces.i_execution_stage import IExecutionStage
from app.chat.context.execution_context import ExecutionContext
from app.models.chat.chat_models import ExecutionResult
from app.cache.interfaces import ICacheService
from app.multilingual.languages import is_concrete_code

import hashlib
import json


def _attachment_digest(images: list, files: list) -> str:
    """Fingerprint attached images/files so a request with attachments is never
    served a cached text-only answer for the same query text.

    Images are large base64 strings; only hash them instead of embedding them
    in the key so we avoid building keys that are megabytes long.
    """
    digest = hashlib.sha256()
    digests = []
    for img in images or []:
        if isinstance(img, str) and img.startswith("data:"):
            _, _, b64 = img.partition(",")
            digests.append(hashlib.sha256(b64.encode("utf-8", "replace")).hexdigest())
    for f in files or []:
        if isinstance(f, dict):
            digests.append(
                hashlib.sha256(
                    json.dumps({"name": f.get("name"), "type": f.get("type"), "content": f.get("content")}, sort_keys=True).encode("utf-8", "replace")
                ).hexdigest()
            )
    if digests:
        digest.update("|".join(digests).encode("utf-8"))
        return digest.hexdigest()[:16]
    return ""

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

        # Requests carrying attachments are content-specific: their answer
        # depends on the uploaded image/file bytes, so they must never be
        # satisfied from a cache written for a bare-text query. Fold an
        # attachment fingerprint into the key so identical bytes hit the cache
        # but different attachments (or none at all) do not.
        images = context.metadata.get("images") or []
        files = context.metadata.get("files") or []
        attachment_fp = _attachment_digest(images, files)

        # Identity scope: authenticated user id, else the guest client id, else
        # anonymous. Cache hits must never cross identities.
        scope = context.session_user or (context.metadata.get("client_id") or "") or "anon"
        key = self._key_for(query, context.metadata.get("language", ""), scope=scope)
        if attachment_fp:
            key = f"att:{attachment_fp}|{key}"
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
