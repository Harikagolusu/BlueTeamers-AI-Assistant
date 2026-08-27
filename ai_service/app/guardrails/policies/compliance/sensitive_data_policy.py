import re
from typing import Dict, Any, List, Pattern, Tuple

from app.guardrails.domain.interfaces.policy_interface import IGuardrailPolicy
from app.guardrails.domain.models.context import GuardrailContext
from app.guardrails.domain.models.result import GuardrailResult


class SensitiveDataLeakPolicy(IGuardrailPolicy):
    """Blocks credential/secret material from leaving the service in answers.

    Direction-aware by design:
      - OUTPUT (metadata stage == "output"): BLOCK when the answer contains
        credential-shaped strings. Patterns are high-precision formats only,
        so legitimate educational content is never modified.
      - INPUT: always ALLOW. Users may paste anything into a query; we protect
        what *we emit*, we do not punish what users type.
    """

    # High-precision secret formats (compiled once at startup).
    _PATTERNS: List[Tuple[Pattern, str]] = [
        (re.compile(r"sk-[A-Za-z0-9]{20,}"), "API key"),
        (re.compile(r"AKIA[0-9A-Z]{16}"), "AWS access key"),
        (re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"), "GitHub token"),
        (re.compile(r"xox[baprs]-[A-Za-z0-9\-]{10,}"), "Slack token"),
        (re.compile(r"AIza[0-9A-Za-z_\-]{35}"), "Google API key"),
        (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "private key block"),
        (
            re.compile(
                r"(?i)(api[_-]?key|secret|password|token)\s*[=:]\s*['\"][A-Za-z0-9/_\-]{16,}['\"]"
            ),
            "embedded credential",
        ),
    ]

    @property
    def name(self) -> str:
        return "sensitive_data_leak_policy"

    @property
    def metadata(self) -> Dict[str, Any]:
        return {
            "version": "1.0",
            "author": "SecurityTeam",
            "description": "Blocks credential-shaped strings from leaving the service in AI answers (output-direction only).",
        }

    async def evaluate(self, context: GuardrailContext) -> GuardrailResult:
        metadata = context.metadata or {}
        if metadata.get("stage") != "output":
            # Input direction: never block - users can paste anything and this
            # policy exists to stop US leaking secrets, not to police queries.
            return GuardrailResult.allow()

        text = context.text or ""
        if not text:
            return GuardrailResult.allow()

        for pattern, label in self._PATTERNS:
            match = pattern.search(text)
            if match:
                return GuardrailResult.block(
                    reason=f"Response contained a potential {label} and was withheld."
                )
        return GuardrailResult.allow()
