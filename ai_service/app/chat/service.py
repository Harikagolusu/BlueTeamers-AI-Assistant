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
import uuid

from app.security.auth import resolve_user_identity
from app.chat.sanitize import clean_response


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
    def __init__(self, orchestrator: IChatOrchestrator):
        self._orchestrator = orchestrator

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
        # effective response language into context.memory; expose it in the API
        # metadata so the frontend can show which language was used.
        language_meta = {
            "language": context.memory.get("language"),
            "language_label": context.memory.get("language_label"),
            "language_source": context.memory.get("language_source"),
        }
        language_meta = {k: v for k, v in language_meta.items() if v}
        
        # 3. Handle output formats
        if context.streaming_mode:
            generator = result.metadata.get("generator")
            # Create a safe copy of metadata without the generator for the final event
            stream_metadata = {k: v for k, v in result.metadata.items() if k != "generator"}
            stream_metadata.update({
                "latency": result.latency_ms,
                "citations": getattr(result, "citations", []),
                "trace_id": str(context.trace_id),
                **language_meta,
            })
            return self._stream_response(generator, result.message, stream_metadata)
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

    async def _stream_response(self, generator, fallback_message: str, metadata: dict = None) -> AsyncGenerator[str, None]:
        import json
        if generator:
            async for chunk in generator:
                payload = {"token": chunk}
                yield f"data: {json.dumps(payload)}\n\n"
        else:
            # Fallback mock streaming if engine didn't provide a generator.
            # Preserve newlines so markdown structure (headings, bullets) is
            # not flattened into a single paragraph.
            for chunk in _tokenize_preserving_newlines(clean_response(fallback_message)):
                payload = {"token": chunk}
                yield f"data: {json.dumps(payload)}\n\n"
        
        # Yield metadata at the end of the stream
        if metadata:
            yield f"data: {json.dumps({'metadata': metadata})}\n\n"
        yield "data: [DONE]\n\n"
