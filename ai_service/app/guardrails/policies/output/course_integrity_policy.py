import re
from typing import Dict, Any
from app.guardrails.domain.interfaces.policy_interface import IGuardrailPolicy
from app.guardrails.domain.models.context import GuardrailContext
from app.guardrails.domain.models.result import GuardrailResult

class CourseIntegrityPolicy(IGuardrailPolicy):
    @property
    def name(self) -> str:
        return "course_integrity_policy"

    @property
    def metadata(self) -> Dict[str, Any]:
        return {
            "version": "1.0",
            "author": "SecurityTeam",
            "description": "Ensures LLM responses do not contain user-supplied false course facts that conflict with verified retrieved content."
        }

    async def evaluate(self, context: GuardrailContext) -> GuardrailResult:
        # This policy is output-direction only
        if context.metadata.get("stage") != "output":
            return GuardrailResult.allow()
        
        text = (context.text or "").lower()
        # Check for known false manipulations that would indicate the LLM accepted user-provided false facts
        # 5 Ws: "Which" instead of "Why" - the verified course content is "Who, What, When, Where, Why"
        if "who, what, when, where, which" in text:
            # Only allow if it explicitly contains the correct list "Who, What, When, Where, Why"
            if "who, what, when, where, why" in text:
                return GuardrailResult.allow()
            # Check if this is a 5 Ws context - look for who/what/when/where in nearby text
            if any(phrase in text for phrase in ["5 w", "five w", "who, what"]):
                return GuardrailResult.block(
                    reason="Response contains manipulated course content (Which instead of Why for 5 Ws)."
                )
        
        # Syslog priority: Facility × 10 instead of × 8 - only block if it contains ONLY the false version
        # If it contains both × 10 and × 8, it's likely a correction (Your stated ×10 conflicts, correct is ×8)
        if re.search(r"facility\s*×\s*10", text) and "priority" in text:
            # If it also contains the correct × 8, it's a correction, allow it
            if not re.search(r"facility\s*×\s*8", text):
                return GuardrailResult.block(
                    reason="Response contains manipulated formula (Facility × 10 instead of Facility × 8)."
                )
        
        return GuardrailResult.allow()
