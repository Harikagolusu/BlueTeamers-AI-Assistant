from typing import List, Dict
from app.security.interfaces.i_policy import IPolicyRegistry
from app.security.models.policy import Policy

class InMemoryPolicyRegistry(IPolicyRegistry):
    def __init__(self):
        self._policies: Dict[str, List[Policy]] = {}

    def register_policy(self, policy: Policy) -> None:
        if policy.resource_type not in self._policies:
            self._policies[policy.resource_type] = []
        self._policies[policy.resource_type].append(policy)

    def get_policies(self, resource_type: str) -> List[Policy]:
        return self._policies.get(resource_type, [])
