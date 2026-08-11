from typing import List, Dict
from app.guardrails.domain.interfaces.group_interface import IPolicyGroup
import logging

logger = logging.getLogger(__name__)

class PolicyRegistry:
    """Manages the discovery and registration of policy groups."""
    
    def __init__(self):
        self._groups: Dict[str, IPolicyGroup] = {}

    def register_group(self, group: IPolicyGroup) -> None:
        if group.name in self._groups:
            raise ValueError(f"Policy group '{group.name}' is already registered.")
        self._groups[group.name] = group
        logger.info(f"Registered policy group: {group.name}")

    def get_group(self, name: str) -> IPolicyGroup:
        return self._groups.get(name)

    def get_all_groups(self) -> List[IPolicyGroup]:
        return list(self._groups.values())

    def validate_registry(self) -> None:
        """Validates that the registry contains no duplicate priorities or policies across groups."""
        seen_priorities = set()
        seen_policies = set()
        
        for group in self._groups.values():
            if group.priority in seen_priorities:
                raise ValueError(f"Duplicate priority '{group.priority}' found for group '{group.name}'.")
            seen_priorities.add(group.priority)
            
            for policy in group.policies:
                if policy.name in seen_policies:
                    raise ValueError(f"Duplicate policy '{policy.name}' found in group '{group.name}'.")
                seen_policies.add(policy.name)
        
        logger.info("Policy registry validation passed.")
