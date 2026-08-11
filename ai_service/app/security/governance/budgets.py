from typing import Dict
from app.security.interfaces.i_governance import IBudgetManager

class BudgetManager(IBudgetManager):
    def __init__(self):
        self._spend: Dict[str, float] = {}
        self._budgets: Dict[str, float] = {}

    def set_budget(self, tenant_id: str, limit: float) -> None:
        self._budgets[tenant_id] = limit

    def check_budget(self, tenant_id: str, cost: float) -> bool:
        spend = self._spend.get(tenant_id, 0.0)
        limit = self._budgets.get(tenant_id, float('inf'))
        return (spend + cost) <= limit

    def consume_budget(self, tenant_id: str, cost: float) -> None:
        if not self.check_budget(tenant_id, cost):
            raise ValueError(f"Budget exceeded for tenant {tenant_id}")
            
        self._spend[tenant_id] = self._spend.get(tenant_id, 0.0) + cost
