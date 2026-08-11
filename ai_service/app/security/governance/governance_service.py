from typing import Any
from app.security.interfaces.i_governance import IGovernanceService, IQuotaManager, IBudgetManager, IRestrictionManager
from app.security.context.security_context import SecurityContext
from app.agents.events.event_bus import agent_event_bus
from app.agents.events.agent_events import AgentEvent

class QuotaExceededEvent(AgentEvent):
    type: str = "QuotaExceeded"
    tenant: str
    resource: str

class BudgetExceededEvent(AgentEvent):
    type: str = "BudgetExceeded"
    tenant: str

class GovernanceService(IGovernanceService):
    def __init__(self, quotas: IQuotaManager, budgets: IBudgetManager, restrictions: IRestrictionManager):
        self._quotas = quotas
        self._budgets = budgets
        self._restrictions = restrictions

    def enforce_governance(self, context: SecurityContext, request: Any) -> None:
        tenant = context.tenant
        
        # Example check extracting cost/quota hints from request
        cost = getattr(request, "estimated_cost", 0.0)
        tokens = getattr(request, "estimated_tokens", 0)
        model = getattr(request, "model_id", None)
        
        if cost > 0 and not self._budgets.check_budget(tenant, cost):
            agent_event_bus.publish(BudgetExceededEvent(session_id=context.session or "sys", tenant=tenant))
            raise ValueError(f"Governance enforcement failed: Budget Exceeded")
            
        if tokens > 0 and not self._quotas.check_quota(tenant, "tokens", tokens):
            agent_event_bus.publish(QuotaExceededEvent(session_id=context.session or "sys", tenant=tenant, resource="tokens"))
            raise ValueError(f"Governance enforcement failed: Quota Exceeded")
            
        if model and not self._restrictions.is_allowed(tenant, "models", model):
            raise ValueError(f"Governance enforcement failed: Model {model} not allowed")
