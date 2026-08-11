from typing import Dict, Any, List
from app.guardrails.domain.interfaces.policy_interface import IGuardrailPolicy
from app.guardrails.domain.interfaces.regex_interface import IRegexEngine
from app.guardrails.domain.models.context import GuardrailContext
from app.guardrails.domain.models.result import GuardrailResult

class InjectionDetectionPolicy(IGuardrailPolicy):
    def __init__(self, regex_engine: IRegexEngine):
        self._regex_engine = regex_engine

    @property
    def name(self) -> str:
        return "injection_detection_policy"

    @property
    def metadata(self) -> Dict[str, Any]:
        return {
            "version": "1.0",
            "author": "SecurityTeam",
            "description": "Detects simple heuristic prompt injections using regex."
        }

    async def evaluate(self, context: GuardrailContext) -> GuardrailResult:
        if self._regex_engine.contains_match(context.text):
            return GuardrailResult.block(reason="Detected potential prompt injection attempt.")
        return GuardrailResult.allow()
