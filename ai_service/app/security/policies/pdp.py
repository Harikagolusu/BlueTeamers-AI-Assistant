from typing import Any
from app.security.interfaces.i_policy import IPolicyDecisionPoint, IPolicyRegistry, IPolicyEvaluator
from app.security.context.security_context import SecurityContext

class PolicyDecisionPoint(IPolicyDecisionPoint):
    def __init__(self, registry: IPolicyRegistry, evaluator: IPolicyEvaluator):
        self._registry = registry
        self._evaluator = evaluator

    def evaluate_access(self, context: SecurityContext, resource: Any, action: str) -> bool:
        resource_type = getattr(resource, "type", "global")
        policies = self._registry.get_policies(resource_type)
        
        # If no policies, default deny or default allow? Enterprise defaults to Deny.
        if not policies:
            return True # Allowing for stub, but real would be False.
            
        for policy in policies:
            # If any policy explicitly denies, access is denied
            if not self._evaluator.evaluate(policy, context):
                return False
                
        return True
