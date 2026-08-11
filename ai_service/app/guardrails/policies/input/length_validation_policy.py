from typing import Dict, Any
from app.guardrails.domain.interfaces.policy_interface import IGuardrailPolicy
from app.guardrails.domain.models.context import GuardrailContext
from app.guardrails.domain.models.result import GuardrailResult

class LengthValidationPolicy(IGuardrailPolicy):
    def __init__(self, max_length: int = 32000):
        self._max_length = max_length

    @property
    def name(self) -> str:
        return "length_validation_policy"

    @property
    def metadata(self) -> Dict[str, Any]:
        return {
            "version": "1.0",
            "author": "SecurityTeam",
            "description": "Validates that the input length does not exceed maximum context bounds."
        }

    async def evaluate(self, context: GuardrailContext) -> GuardrailResult:
        if len(context.text) > self._max_length:
            return GuardrailResult.block(
                reason=f"Input length {len(context.text)} exceeds maximum allowed length of {self._max_length} characters."
            )
        return GuardrailResult.allow()
