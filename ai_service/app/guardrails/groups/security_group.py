from app.guardrails.groups.base_group import BasePolicyGroup
from app.guardrails.domain.models.enums import PolicyPriority

class SecurityGroup(BasePolicyGroup):
    def __init__(self):
        super().__init__(name="Security", priority=PolicyPriority.HIGH)
