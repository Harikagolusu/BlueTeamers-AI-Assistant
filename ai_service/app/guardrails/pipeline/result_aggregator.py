from typing import List, Tuple
import logging
from app.guardrails.domain.models.context import GuardrailContext
from app.guardrails.domain.models.result import GuardrailResult
from app.guardrails.domain.interfaces.policy_interface import IGuardrailPolicy
from app.guardrails.domain.models.enums import PolicyAction

logger = logging.getLogger(__name__)

class ResultAggregator:
    def __init__(self, is_audit_mode: bool = False):
        self.is_audit_mode = is_audit_mode
        self.results: List[Tuple[IGuardrailPolicy, GuardrailResult]] = []
        self._should_block = False
        self._block_reasons: List[str] = []

    def add_result(self, policy: IGuardrailPolicy, result: GuardrailResult) -> None:
        self.results.append((policy, result))
        
        if result.action == PolicyAction.BLOCK:
            if self.is_audit_mode:
                logger.info(f"[AUDIT MODE] Block bypassed for policy {policy.name}. Reason: {result.reason}")
            else:
                self._should_block = True
                self._block_reasons.append(f"{policy.name}: {result.reason}")

    def should_block(self) -> bool:
        return self._should_block

    def get_block_reasons(self) -> str:
        return "; ".join(self._block_reasons)

    def apply_modifications(self, context: GuardrailContext) -> GuardrailContext:
        """Applies text modifications sequentially if any policy altered the text."""
        modified_context = context.model_copy()
        for policy, result in self.results:
            if result.modified_text is not None:
                modified_context.text = result.modified_text
        return modified_context
