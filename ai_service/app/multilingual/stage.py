"""LanguageContextStage — resolves and injects the response language.

Runs near the top of the pipeline so the language is known before the cache
lookup, intent analysis and engine execution.

1. It extracts any explicit ``language`` the client sent (Feature 2 & 3).
2. It loads the user's remembered preference (Feature 6 — conversation memory).
3. Otherwise it auto-detects the language from the query text (Feature 1).
4. It persists the resolved preference so future conversations continue in the
   same language until the user changes it.
5. It writes ``language`` / ``language_label`` / ``language_block`` into
   ``context.memory`` where SimplePromptBuilder picks them up, and mirrors the
   resolved code into ``context.metadata`` for engines & API metadata.

Note: imports of ``app.chat`` modules are deferred to method bodies to avoid a
circular import when ``app.multilingual.*`` is imported before ``app.chat``
(exactly as bootstrap + pipeline stage modules chain through app.chat.router).
"""
import logging
from typing import Optional, Tuple

from app.multilingual.dependencies import (
    get_language_detector,
    get_language_preference_store,
)
from app.multilingual.detector import LanguageDetector
from app.multilingual.languages import is_concrete_code, language_label
from app.multilingual.preferences import LanguagePreferenceStore
from app.multilingual.prompts import (
    RESOLUTION_SOURCE_DETECTED,
    RESOLUTION_SOURCE_MANUAL,
    RESOLUTION_SOURCE_STORED,
    SWITCH_THRESHOLD,
    build_language_block,
)

logger = logging.getLogger("app.chat.pipeline.language_stage")

GUEST_PREFIX = "guest:"


class LanguageContextStage:
    """Resolves the response language for the current request."""

    @property
    def name(self) -> str:
        return "ResolveLanguage"

    def __init__(
        self,
        detector: Optional[LanguageDetector] = None,
        store: Optional[LanguagePreferenceStore] = None,
    ):
        self._detector = detector or get_language_detector()
        self._store = store or get_language_preference_store()

    async def execute(self, context) -> "ExecutionContext":
        from app.chat.context.execution_context import ExecutionContext

        new_memory = dict(context.memory) if context.memory else {}

        query = context.metadata.get("query") or ""
        explicit = context.metadata.get("language")
        pref_key = self._preference_key(context)

        stored = None
        if pref_key:
            try:
                stored = await self._store.get(pref_key)
            except Exception as e:  # pragma: no cover - defensive
                logger.warning("Failed to load language preference: %s", e)

        code, source = await self._resolve(explicit, stored, query, pref_key)

        new_memory["language"] = code
        new_memory["language_label"] = language_label(code)
        new_memory["language_block"] = build_language_block(code, source)
        new_memory["language_source"] = source

        # Mirror into metadata so engines / API metadata can reuse it.
        context.metadata["language"] = code
        context.metadata["language_label"] = new_memory["language_label"]
        context.metadata["language_source"] = source

        return context.with_memory(new_memory)

    # ------------------------------------------------------------------ helpers

    @staticmethod
    def _preference_key(context) -> Optional[str]:
        """Stable store key for the tracked identity (user or device)."""
        if context.session_user:
            return context.session_user
        client_id = context.metadata.get("client_id")
        if client_id:
            return f"{GUEST_PREFIX}{client_id}"
        return None

    async def _resolve(
        self,
        explicit: Optional[str],
        stored: Optional[str],
        query: str,
        pref_key: Optional[str],
    ) -> Tuple[str, str]:
        """Return (code, resolution_source) for the request.

        Order of precedence:
          1. Explicit concrete language in the request (manual selection).
          2. Stored concrete preference (remembered language) — unless the user
             clearly typed in a different script this message (Feature 1),
             in which case the detected language wins and is remembered instead.
          3. Auto-detect from the query; the result is remembered for the user.
        """
        if explicit and is_concrete_code(explicit):
            code = explicit
            source = RESOLUTION_SOURCE_MANUAL
            if pref_key and stored != code:
                await self._safe_set(pref_key, code)
            return code, source

        detected_code, confidence = self._detector.detect(query)

        if stored and is_concrete_code(stored):
            if confidence >= SWITCH_THRESHOLD and detected_code != stored:
                # e.g. the user switched from English to Telugu script.
                if pref_key:
                    await self._safe_set(pref_key, detected_code)
                return detected_code, RESOLUTION_SOURCE_DETECTED
            return stored, RESOLUTION_SOURCE_STORED

        # Auto / no stored preference -> remember the detection (Feature 6).
        if pref_key and stored != detected_code:
            await self._safe_set(pref_key, detected_code)
        return detected_code, RESOLUTION_SOURCE_DETECTED

    async def _safe_set(self, pref_key: str, code: str) -> None:
        try:
            await self._store.set(pref_key, code)
        except Exception as e:  # pragma: no cover - defensive
            logger.warning("Failed to persist language preference: %s", e)