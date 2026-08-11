"""Guardrails integration as pipeline stages.

Runs the existing GuardrailsService against user input (before processing) and
against the final answer (before composition). Blocked content short-circuits
to a graceful refusal message instead of failing the request.
"""
import logging

from app.chat.interfaces.i_execution_stage import IExecutionStage
from app.chat.context.execution_context import ExecutionContext
from app.models.chat.chat_models import ExecutionResult, ExecutionStatus
from app.guardrails.domain.models.context import GuardrailContext
from app.guardrails.domain.services.guardrails_service import GuardrailsService
from app.guardrails.exceptions.guardrail_exceptions import PolicyViolationError

logger = logging.getLogger("app.chat.guardrails")

BLOCKED_MESSAGE = (
    "I can't help with that request — it was flagged by our content safety and "
    "input validation policies. Please rephrase your question."
)


def _guardrail_context(context: ExecutionContext, text: str, stage: str) -> GuardrailContext:
    return GuardrailContext(
        text=text,
        trace_id=str(context.trace_id),
        request_id=str(context.correlation_id),
        user_id=context.session_user,
        tenant_id=context.tenant_id,
        environment="production",
        metadata={"stage": stage},
    )


class InputGuardrailsStage(IExecutionStage):
    """Validates the raw user query before it reaches any other pipeline stage."""

    def __init__(self, service: GuardrailsService):
        self._service = service

    @property
    def name(self) -> str:
        return "InputGuardrails"

    async def execute(self, context: ExecutionContext) -> ExecutionContext:
        text = context.metadata.get("query", "") or ""
        if not text:
            return context

        try:
            await self._service.validate_input(
                _guardrail_context(context, text, stage="input")
            )
        except PolicyViolationError as e:
            logger.warning("Input blocked by guardrails: %s", e)
            result = ExecutionResult(
                status=ExecutionStatus.BLOCKED,
                engine_name="guardrails",
                message=BLOCKED_MESSAGE,
                metadata={
                    "guardrail_blocked": True,
                    "guardrail_reason": str(e),
                    "guardrail_stage": "input",
                },
            )
            new_metadata = {
                **context.metadata,
                "execution_result": result,
                "guardrail_blocked": True,
                "guardrail_reason": str(e),
            }
            return context.model_copy(update={"metadata": new_metadata})
        return context


class OutputGuardrailsStage(IExecutionStage):
    """Validates the final answer text before it is composed into a response."""

    def __init__(self, service: GuardrailsService):
        self._service = service

    @property
    def name(self) -> str:
        return "OutputGuardrails"

    async def execute(self, context: ExecutionContext) -> ExecutionContext:
        result = context.metadata.get("execution_result")
        if not result or getattr(result, "stream", False):
            return context

        text = result.message or ""
        if not text:
            return context

        try:
            out_ctx = await self._service.validate_output(
                _guardrail_context(context, text, stage="output")
            )
        except PolicyViolationError as e:
            logger.warning("Output blocked by guardrails: %s", e)
            new_result = result.model_copy(
                update={
                    "message": BLOCKED_MESSAGE,
                    "metadata": {
                        **result.metadata,
                        "guardrail_blocked": True,
                        "guardrail_reason": str(e),
                        "guardrail_stage": "output",
                    },
                }
            )
            new_metadata = {
                **context.metadata,
                "execution_result": new_result,
                "guardrail_blocked": True,
            }
            return context.model_copy(update={"metadata": new_metadata})

        if out_ctx.text != text:
            new_result = result.model_copy(
                update={
                    "message": out_ctx.text,
                    "metadata": {
                        **result.metadata,
                        "guardrail_modified": True,
                    },
                }
            )
            return context.model_copy(
                update={
                    "metadata": {
                        **context.metadata,
                        "execution_result": new_result,
                    }
                }
            )
        return context
