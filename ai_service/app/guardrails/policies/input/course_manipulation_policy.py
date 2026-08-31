import re
from typing import Dict, Any
from app.guardrails.domain.interfaces.policy_interface import IGuardrailPolicy
from app.guardrails.domain.models.context import GuardrailContext
from app.guardrails.domain.models.result import GuardrailResult

# Manipulation phrases that attempt to overwrite course facts
_MANIPULATION_PHRASES = [
    r"updated rule",
    r"new rule",
    r"for this test",
    r"for this test assume",
    r"ignore.*course.*rule",
    r"ignore.*previous.*course",
    r"use this new formula",
    r"use this formula instead",
    r"ignore the (previous )?rule",
    r"use this (new )?rule",
    r"which.*instead of why",
    r"facility\s*×\s*10",
]

# Course-specific terms that must be verified
_COURSE_TERMS = [
    r"5\s*w",
    r"who.*what.*when.*where.*why",
    r"facility.*severity",
    r"priority.*facility",
]

class CourseManipulationPolicy(IGuardrailPolicy):
    @property
    def name(self) -> str:
        return "course_manipulation_policy"

    @property
    def metadata(self) -> Dict[str, Any]:
        return {
            "version": "1.0",
            "author": "SecurityTeam",
            "description": "Detects attempts to overwrite verified course content with user-provided false facts."
        }

    async def evaluate(self, context: GuardrailContext) -> GuardrailResult:
        text = (context.text or "").lower()
        has_manipulation = any(re.search(p, text) for p in _MANIPULATION_PHRASES)
        has_course_term = any(re.search(p, text) for p in _COURSE_TERMS)
        
        # Only flag when manipulation phrase + course term co-occur
        # This prevents false positives on normal hypotheticals
        if has_manipulation and has_course_term:
            return GuardrailResult.warn(
                reason="Potential course content manipulation detected. Verified course content must be treated as authoritative."
            )
        
        # Also check for direct formula manipulation without explicit phrase
        # e.g., "Priority = (Facility × 10) + Severity" when verified is × 8
        if re.search(r"facility\s*×\s*10", text) and "priority" in text:
            return GuardrailResult.warn(reason="Potential formula manipulation detected.")
        
        if re.search(r"which.*instead of why", text) and "5 w" in text:
            return GuardrailResult.warn(reason="Potential 5 Ws manipulation detected.")
        
        return GuardrailResult.allow()
