import asyncio
from typing import List
from app.guardrails.domain.interfaces.group_interface import IPolicyGroup
from app.guardrails.domain.interfaces.policy_interface import IGuardrailPolicy
from app.guardrails.domain.models.context import GuardrailContext
from app.guardrails.domain.models.result import GuardrailResult
from app.guardrails.domain.models.enums import PolicyPriority

class BasePolicyGroup(IPolicyGroup):
    def __init__(self, name: str, priority: PolicyPriority):
        self._name = name
        self._priority = priority
        self._policies: List[IGuardrailPolicy] = []

    @property
    def name(self) -> str:
        return self._name

    @property
    def priority(self) -> PolicyPriority:
        return self._priority

    @property
    def policies(self) -> List[IGuardrailPolicy]:
        return self._policies

    def add_policy(self, policy: IGuardrailPolicy) -> None:
        self._policies.append(policy)

    async def evaluate_all(self, context: GuardrailContext) -> List[GuardrailResult]:
        if not self._policies:
            return []
        
        # Execute lifecycle hooks before evaluation
        await asyncio.gather(*(p.before_policy(context) for p in self._policies))
        
        # Execute evaluations in parallel
        results = await asyncio.gather(*(p.evaluate(context) for p in self._policies))
        
        # Execute lifecycle hooks after evaluation
        await asyncio.gather(*(p.after_policy(context, res) for p, res in zip(self._policies, results)))
        
        return list(results)
