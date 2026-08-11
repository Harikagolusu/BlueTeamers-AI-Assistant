from app.security.interfaces.i_policy import IPolicyEvaluator
from app.security.context.security_context import SecurityContext
from app.security.models.policy import Policy

class BasicPolicyEvaluator(IPolicyEvaluator):
    def evaluate(self, policy: Policy, context: SecurityContext) -> bool:
        for rule in policy.rules:
            # Stub logic for rule evaluation
            if rule.condition == "RequireAdmin" and "admin" not in context.roles:
                return False
            if rule.condition == "RequireVerified" and not context.token_metadata.get("verified"):
                return False
        return True
