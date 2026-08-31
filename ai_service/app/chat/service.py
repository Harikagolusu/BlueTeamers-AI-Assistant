from typing import AsyncGenerator, List, Optional, Union

from app.chat.interfaces.i_chat_service import IChatService
from app.chat.interfaces.i_chat_orchestrator import IChatOrchestrator
from app.models.chat.chat_models import ChatRequest, ChatResponse
from app.chat.context.execution_context import ExecutionContext
from app.memory.interfaces import IMemoryManager
from app.conversations.service import ConversationService
from app.core.config import settings
import uuid
import logging

from app.security.auth import resolve_user_identity
from app.chat.sanitize import clean_response
from app.guardrails.domain.models.context import GuardrailContext
from app.guardrails.exceptions.guardrail_exceptions import PolicyViolationError


def _tokenize_preserving_newlines(text: str) -> List[str]:
    """Splits text into word tokens while keeping line breaks as tokens.

    Used for the mock-stream fallback so markdown structure (paragraphs,
    bullet lists) survives streaming instead of collapsing into one line.
    """
    tokens: List[str] = []
    for chunk in text.split("\n"):
        if tokens:
            tokens.append("\n")
        for word in chunk.split(" "):
            if word:
                tokens.append(word + " ")
    return tokens


logger = logging.getLogger("app.chat.service")


GUEST_ID_PREFIX = "guest:"


def _resolve_user(token: str, client_id: Optional[str] = None):
    """Extract (session_user, tenant_id) for memory/adaptive scoping.

    Authenticated users are keyed by the stable ``user_id`` claim (never the
    ``email`` claim, which vanishes after token refresh). This keeps
    conversation persistence, short-term memory and adaptive learning keyed
    consistently for the same user before and after a token refresh.

    Guests without a JWT but carrying the persistent browser ``client_id`` are
    scoped under the same namespaced ``guest:`` id the freemium layer uses, so
    the short-term conversation memory window works end-to-end for anonymous
    sessions too. Fully anonymous callers (no token, no client id) have no
    identity and therefore no memory.
    """
    if token:
        user_id, _email = resolve_user_identity(token)
        if user_id:
            return user_id, user_id
    if client_id:
        return f"{GUEST_ID_PREFIX}{client_id}", None
    return None, None


def _get_display_name_for_scope(scope: Optional[str], email_hint: Optional[str] = None) -> tuple:
    """Return (display_name, email) for a quota scope.

    For ``user:<id>`` scopes we look up the Django ``accounts_user`` table to
    fetch the canonical ``full_name`` + ``email`` so logs show e.g.
    ``Harika Demo User <harika@example.com>`` instead of just ``user:1``.
    Guests return ``(None, None)`` — they are already keyed by their
    ``guest:<client_id>`` and have no directory entry. Failures are silent and
    fall back to the JWT email hint if available.
    """
    if not scope or scope.startswith(GUEST_ID_PREFIX) or scope.startswith("ip:"):
        return None, email_hint
    # Authenticated: scope is user:<id> or raw user_id
    raw_id = scope.split(":", 1)[-1] if ":" in scope else scope
    try:
        import pathlib, sqlite3

        # Django DB lives at infosec-backend; try both relative locations.
        candidates = [
            pathlib.Path("infosecdairies/infosec-backend/backend/db.sqlite3"),
            pathlib.Path("../infosecdairies/infosec-backend/backend/db.sqlite3"),
            pathlib.Path("/home/harika/BlueTeamers-AI-Assistant/infosecdairies/infosec-backend/backend/db.sqlite3"),
        ]
        db_path = next((p for p in candidates if p.exists()), None)
        if not db_path:
            return email_hint, email_hint
        conn = sqlite3.connect(str(db_path))
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            "SELECT full_name, email FROM accounts_user WHERE id = ?", (raw_id,)
        ).fetchone()
        conn.close()
        if row:
            return row["full_name"] or email_hint, row["email"] or email_hint
    except Exception:
        pass
    return email_hint, email_hint

# Hard ceiling on streamed answer size. Normal answers land far below this;
# it only stops runaway/looping generations from burning unbounded tokens.
_MAX_STREAM_CHARS = 24_000
# Audit A-07: flush safety valve for streaming segments without newlines —
# keeps very long single-line answers rendering progressively.
_STREAM_FLUSH_CHARS = 512

class ChatService(IChatService):
    """
    Application Layer boundary for Chat processing.
    """
    def __init__(
        self,
        orchestrator: IChatOrchestrator,
        memory_manager: IMemoryManager = None,
        conversation_service: ConversationService = None,
        guardrails_service=None,
    ):
        self._orchestrator = orchestrator
        self._memory_manager = memory_manager
        self._conversations = conversation_service
        # Optional guardrails service used to safety-check streamed output
        # (audit A-03/A-07): OutputGuardrailsStage only sees the streaming
        # placeholder, so the actual streamed chunks are checked here.
        self._guardrails = guardrails_service

    async def process_request(self, request: ChatRequest) -> Union[ChatResponse, AsyncGenerator[str, None]]:
        # 1. Validation & Setup
        # Create an initial ExecutionContext
        session_user, tenant_id = _resolve_user(request.token, request.client_id)
        context = ExecutionContext(
            correlation_id=uuid.uuid4(),
            session_user=session_user,
            tenant_id=tenant_id or None,
            streaming_mode=request.stream,
            metadata={
                "query": request.message,
                "token": request.token,
                "images": request.images,
                "files": request.files,
                "user_id": request.user_id,
                "client_id": request.client_id,
                "conversation_id": request.conversation_id,
                "language": request.language,
                "context": request.context,
            }
        )
        
        # 2. Execute Orchestrator Pipeline
        result = await self._orchestrator.execute_pipeline(context)
        
        # Resolved language (Sprint 7): the LanguageContextStage writes the
        # effective response language into context.metadata (the metadata dict
        # is shared across the immutable stage copies); expose it in the API
        # metadata so the frontend can show which language was used.
        language_meta = {
            "language": context.metadata.get("language"),
            "language_label": context.metadata.get("language_label"),
            "language_source": context.metadata.get("language_source"),
        }
        language_meta = {k: v for k, v in language_meta.items() if v}
        
        # 3. Handle output formats
        if context.streaming_mode:
            generator = result.metadata.get("generator")
            pending_turn = result.metadata.get("_pending_turn")
            # Create a safe copy of metadata without the generator for the final event
            # Use allowlist for client-safe fields only (F-05: no content_hash/chunk_id)
            _safe_keys = {"agent", "engine", "intent", "domain", "answer_source", "course_sources", "suggested_courses", "llm_used", "recommendation_used", "repositories"}
            stream_metadata = {k: v for k, v in result.metadata.items() if k in _safe_keys}
            # Sanitize sources to only safe metadata (no content_hash, chunk_id, text)
            if "sources" in result.metadata:
                safe_sources = []
                for doc in result.metadata["sources"]:
                    meta = doc.get("metadata", {})
                    safe_sources.append({
                        "metadata": {
                            "course_slug": meta.get("course_slug"),
                            "course_title": meta.get("course_title"),
                            "lesson_title": meta.get("lesson_title"),
                            "lesson_id": meta.get("lesson_id"),
                        }
                    })
                stream_metadata["sources"] = safe_sources
            stream_metadata.update({
                "latency": result.latency_ms,
                "citations": getattr(result, "citations", []),
                "trace_id": str(context.trace_id),
                **language_meta,
            })
            return self._stream_response(
                generator,
                result.message,
                stream_metadata,
                pending_turn=pending_turn,
                quota_scope=self._quota_scope(session_user),
            )
        else:
            final_metadata = {
                "latency": result.latency_ms,
                "citations": getattr(result, "citations", []),
                "trace_id": str(context.trace_id),
                **language_meta,
            }
            final_metadata.update(result.metadata)
            # Remove generator if present
            final_metadata.pop("generator", None)
            
            # Token accounting: persist the LLM tokens consumed by this request
            # (daily + monthly windows). Best-effort; never affects the reply.
            await self._record_token_usage(self._quota_scope(session_user))

            return ChatResponse(
                conversation_id=request.conversation_id or str(uuid.uuid4()),
                message=clean_response(result.message),
                metadata=final_metadata,
                used_tools=[t.get("tool") for t in getattr(result, "tool_outputs", [])]
            )

    @staticmethod
    def _quota_scope(session_user: Optional[str]) -> Optional[str]:
        """Map the identified session user to the token-quota scope key.

        Authenticated users are billed as ``user:<id>``; guests carry their
        persistent browser ``client_id`` as ``guest:<client_id>`` (per-device
        granularity — better than the shared office IP for measuring usage).
        Fully anonymous callers have no scope and are not billed.
        """
        if not session_user:
            return None
        if str(session_user).startswith("guest:"):
            return session_user
        return f"user:{session_user}"

    async def _record_token_usage(self, scope: Optional[str]) -> None:
        """Persist the LLM tokens this request consumed (daily + monthly).

        Best-effort: accounting must never break the user's answer, so any
        failure is logged and swallowed. For authenticated scopes we also
        persist the human-readable ``full_name`` + ``email`` from the Django
        ``accounts_user`` table so the usage log shows names, not just
        ``user:1``.
        """
        if not scope:
            return
        try:
            from app.runtime.context_manager import RuntimeContextManager
            from app.runtime.services.token_usage_recorder import record_tokens

            total = RuntimeContextManager.get().token_usage.total_tokens
            if total > 0:
                display_name, email = _get_display_name_for_scope(scope)
                await record_tokens(scope, total, display_name=display_name, email=email)
        except Exception as exc:
            logger.warning("Failed to record token usage for %s: %s", scope, exc)

    async def _stream_response(self, generator, fallback_message: str, metadata: dict = None, pending_turn: dict = None, quota_scope: str = None) -> AsyncGenerator[str, None]:
        import json
        parts = []
        emitted = 0
        # Audit A-07: streamed chunks previously reached the client raw —
        # neither clean_response() nor output guardrails ran on them, so
        # internal artifacts ([Document N], SOURCE lines, debug tags) could
        # leak. Naively sanitizing every token corrupts matches that span
        # chunks, so we buffer per *line* (all artifact patterns are
        # line-anchored) and sanitize each complete line before emitting.
        # The trailing partial line is held back until more text or the end
        # of the stream, keeping SSE behaviour and wording intact.
        buffer = ""

        def _normalize_table_newlines(text: str) -> str:
            """Fix collapsed markdown tables and bullet lists inside a streamed chunk.

            LLMs occasionally stream "| Details ||---|---|" or
            "|---|---| | **What** |" without the required newline between
            rows, or "here are 5 key points:- Collection" without newline
            before bullets. The boundary then lives *inside* a single
            512-char safety-valve flush, so the frontend inter-token fix
            never fires. Normalizing here ensures the SSE token itself is
            already valid markdown (and that persisted history is correct).
            """
            if not text:
                return text
            import re as _re
            out = text
            if "|" in out:
                # Generic row boundary for Wazuh-style tables: "alerts || Indexer" or "alerts | | Indexer"
                if "---" in out and "||" in out:
                    out = _re.sub(r"\|\s*\|\s*", "|\n|", out)
                elif "---" in out and "| |" in out:
                    out = _re.sub(r"\|\s*\|\s*", "|\n|", out)
                elif "||" in out and "---" in out:
                    out = out.replace("||", "|\n|")
                else:
                    if "||" in out and "---" in out:
                        out = out.replace("||", "|\n|")
                    out = _re.sub(r"\|\s*\|\s*(?=-)", "|\n|", out)
                # 1) Missing newline before separator row
                out = _re.sub(r"([^\n])\s+(\|\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|)", lambda m: m.group(1) + "\n" + m.group(2).strip() if "---" in m.group(2) else m.group(0), out)
                # 2) Separator glued to next data row: "|---|---| | What" -> "|---|---| \n| What"
                out = _re.sub(r"(\|[-:\s|]+\|)\s+(\|)", lambda m: m.group(1) + "\n" + m.group(2) if "---" in m.group(1) else m.group(0), out)
            if "- " in out:
                # Bullet list: "analyst:- Collection" -> "analyst:\n\n- Collection"
                out = _re.sub(r"([^\n]):\s*-\s+(?=[A-Z*•])", r"\1:\n\n- ", out)
                # "entry point.- Parsing" -> "entry point.\n- Parsing"
                out = _re.sub(r"([^\n])\.\s*-\s+(?=[A-Z*•])", r"\1.\n- ", out)
            return out

        async def _emit_sanitized(text: str) -> str:
            """Sanitize one complete segment and run output guardrails.

            Returns the SSE frame, or '' when the segment was removed by
            sanitization. Guardrail blocks replace the segment with a short
            notice instead of failing the whole stream.
            """
            text = _normalize_table_newlines(text)
            cleaned = clean_response(text)
            if not cleaned:
                return ""
            if self._guardrails is not None:
                try:
                    await self._guardrails.validate_output(
                        GuardrailContext(
                            text=cleaned,
                            trace_id="stream",
                            request_id="stream",
                            environment="production",
                            metadata={"stage": "stream_output"},
                        )
                    )
                except PolicyViolationError as e:
                    logger.warning("Streamed output blocked by guardrails: %s", e)
                    return (
                        'data: {"token": "\\n\\n[Part of this response was '
                        'withheld by our content safety policy.]"}\\n\\n'
                    )
                except Exception as exc:
                    # Safety checking must never break the answer stream.
                    logger.warning("Stream output guardrail check failed: %s", exc)
            return f'data: {json.dumps({"token": cleaned})}\n\n'

        def _deliver(text: str, frame: str):
            nonlocal emitted
            if not frame:
                return
            parts.append(text)
            emitted += len(text)
            return frame

        if generator:
            async for chunk in generator:
                if emitted >= _MAX_STREAM_CHARS:
                    break
                buffer += chunk
                # Flush every complete line (kept in order, with its newline).
                while "\n" in buffer and emitted < _MAX_STREAM_CHARS:
                    line, buffer = buffer.split("\n", 1)
                    frame = await _emit_sanitized(line + "\n")
                    frame = _deliver(line + "\n", frame)
                    if frame:
                        yield frame
                # Safety valve: very long single-line streams must still
                # render progressively; flush the buffer once it grows past
                # the cap (artifact patterns are line-anchored, so a partial
                # line cannot hide a ^-anchored match).
                if len(buffer) >= _STREAM_FLUSH_CHARS and emitted < _MAX_STREAM_CHARS:
                    # Normalize table newlines before flush so a collapsed
                    # "| Details ||---|---|" inside the 512-char window
                    # becomes two proper lines.
                    buffer = _normalize_table_newlines(buffer)
                    # If normalization introduced newlines, emit line-by-line
                    # to keep markdown structure, otherwise emit as single chunk
                    if "\n" in buffer:
                        while "\n" in buffer and emitted < _MAX_STREAM_CHARS:
                            line, buffer = buffer.split("\n", 1)
                            frame = await _emit_sanitized(line + "\n")
                            frame = _deliver(line + "\n", frame)
                            if frame:
                                yield frame
                        if buffer and emitted < _MAX_STREAM_CHARS and len(buffer) >= _STREAM_FLUSH_CHARS:
                            frame = await _emit_sanitized(buffer)
                            frame = _deliver(buffer, frame)
                            if frame:
                                yield frame
                            buffer = ""
                    else:
                        frame = await _emit_sanitized(buffer)
                        frame = _deliver(buffer, frame)
                        if frame:
                            yield frame
                        buffer = ""
            if buffer and emitted < _MAX_STREAM_CHARS:
                frame = await _emit_sanitized(buffer)
                frame = _deliver(buffer, frame)
                if frame:
                    yield frame
        else:
            # Fallback mock streaming if engine didn't provide a generator.
            # Preserve newlines so markdown structure (headings, bullets) is
            # not flattened into a single paragraph.
            for chunk in _tokenize_preserving_newlines(clean_response(fallback_message)):
                if emitted >= _MAX_STREAM_CHARS:
                    break
                emitted += len(chunk)
                parts.append(chunk)
                payload = {"token": chunk}
                yield f"data: {json.dumps(payload)}\n\n"

        # Persist the real streamed content once the stream completes so the
        # conversation history stores the actual reply instead of the
        # "[Streaming Generator]" placeholder (which was deferred by
        # PersistenceStage).
        if pending_turn and self._memory_manager is not None:
            try:
                await self._persist_pending_turn(pending_turn, "".join(parts))
            except Exception as exc:
                logger.warning("Failed to persist streamed turn: %s", exc)

        # Token accounting for streamed replies: the real LLM token usage is
        # only known once the stream has been fully consumed, so record it here.
        await self._record_token_usage(quota_scope)

        # Yield metadata at the end of the stream
        if metadata:
            yield f"data: {json.dumps({'metadata': metadata})}\n\n"
        yield "data: [DONE]\n\n"

    async def _persist_pending_turn(self, pending_turn: dict, ai_message: str) -> None:
        """Persist a turn whose response was only available after streaming."""
        ai_message = clean_response(ai_message)
        if not ai_message:
            return

        query = pending_turn.get("query") or ""
        memory_user = pending_turn.get("memory_session_user") or pending_turn.get("session_user")

        await self._memory_manager.save_turn(
            session_user=memory_user,
            tenant_id=pending_turn.get("tenant_id") or "default",
            turn_data={"query": query, "response": ai_message},
        )

        if self._conversations is not None and getattr(settings, "CONVERSATION_PERSISTENCE_ENABLED", True):
            # Guest threads only feed the short-term memory window above; they
            # must not appear in the authenticated user's Recent Conversations.
            if pending_turn.get("session_user") and not str(
                pending_turn.get("session_user")
            ).startswith(GUEST_ID_PREFIX):
                try:
                    await self._conversations.record_turn(
                        user_id=pending_turn.get("session_user"),
                        conversation_id=pending_turn.get("conversation_id"),
                        user_message=query,
                        ai_message=ai_message,
                        metadata=pending_turn.get("conversation_metadata") or {},
                    )
                except Exception as exc:
                    logger.warning("Failed to record streamed conversation turn: %s", exc)
