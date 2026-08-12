from typing import AsyncGenerator, List, Union


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

logger = logging.getLogger("app.chat.service")


def _resolve_user(token: str):
    """Extract (session_user, tenant_id) from the JWT for memory scoping.

    session_user is the stable ``user_id`` claim (never the ``email`` claim,
    which vanishes after token refresh). This keeps conversation persistence,
    short-term memory and adaptive learning keyed consistently for the same
    user before and after a token refresh.
    """
    user_id, _email = resolve_user_identity(token)
    if not user_id:
        return None, None
    return user_id, user_id

class ChatService(IChatService):
    """
    Application Layer boundary for Chat processing.
    """
    def __init__(
        self,
        orchestrator: IChatOrchestrator,
        memory_manager: IMemoryManager = None,
        conversation_service: ConversationService = None,
    ):
        self._orchestrator = orchestrator
        self._memory_manager = memory_manager
        self._conversations = conversation_service

    async def process_request(self, request: ChatRequest) -> Union[ChatResponse, AsyncGenerator[str, None]]:
        # 1. Validation & Setup
        # Create an initial ExecutionContext
        session_user, tenant_id = _resolve_user(request.token)
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
            stream_metadata = {k: v for k, v in result.metadata.items() if k not in ("generator", "_pending_turn")}
            stream_metadata.update({
                "latency": result.latency_ms,
                "citations": getattr(result, "citations", []),
                "trace_id": str(context.trace_id),
                **language_meta,
            })
            return self._stream_response(generator, result.message, stream_metadata, pending_turn=pending_turn)
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
            
            return ChatResponse(
                conversation_id=request.conversation_id or str(uuid.uuid4()),
                message=clean_response(result.message),
                metadata=final_metadata,
                used_tools=[t.get("tool") for t in getattr(result, "tool_outputs", [])]
            )

    async def _stream_response(self, generator, fallback_message: str, metadata: dict = None, pending_turn: dict = None) -> AsyncGenerator[str, None]:
        import json
        parts = []
        if generator:
            async for chunk in generator:
                parts.append(chunk)
                payload = {"token": chunk}
                yield f"data: {json.dumps(payload)}\n\n"
        else:
            # Fallback mock streaming if engine didn't provide a generator.
            # Preserve newlines so markdown structure (headings, bullets) is
            # not flattened into a single paragraph.
            for chunk in _tokenize_preserving_newlines(clean_response(fallback_message)):
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
