from typing import Dict
from app.security.interfaces.i_governance import IQuotaManager

class QuotaManager(IQuotaManager):
    def __init__(self):
        self._quotas: Dict[str, Dict[str, int]] = {} # tenant_id -> resource -> usage
        self._limits: Dict[str, Dict[str, int]] = {} # tenant_id -> resource -> limit

    def set_quota(self, tenant_id: str, resource: str, limit: int) -> None:
        if tenant_id not in self._limits:
            self._limits[tenant_id] = {}
        self._limits[tenant_id][resource] = limit

    def check_quota(self, tenant_id: str, resource: str, amount: int) -> bool:
        usage = self._quotas.get(tenant_id, {}).get(resource, 0)
        limit = self._limits.get(tenant_id, {}).get(resource, float('inf'))
        return (usage + amount) <= limit

    def consume_quota(self, tenant_id: str, resource: str, amount: int) -> None:
        if not self.check_quota(tenant_id, resource, amount):
            raise ValueError(f"Quota exceeded for resource: {resource}")
            
        if tenant_id not in self._quotas:
            self._quotas[tenant_id] = {}
        self._quotas[tenant_id][resource] = self._quotas[tenant_id].get(resource, 0) + amount
