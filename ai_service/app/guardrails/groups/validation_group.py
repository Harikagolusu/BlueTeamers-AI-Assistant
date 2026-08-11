from app.guardrails.groups.base_group import BasePolicyGroup
from app.guardrails.domain.models.enums import PolicyPriority

class ValidationGroup(BasePolicyGroup):
    def __init__(self):
        super().__init__(name="Validation", priority=PolicyPriority.CRITICAL)
