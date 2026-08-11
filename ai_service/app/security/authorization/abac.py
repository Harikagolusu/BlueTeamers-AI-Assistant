from typing import Dict, Any
from app.security.interfaces.i_authorization import IAccessEvaluator

class ABACEvaluator(IAccessEvaluator):
    def evaluate_rbac(self, principal: str, required_permission: str) -> bool:
        # Handled by RBAC components usually
        return False
        
    def evaluate_abac(self, principal: str, resource: Dict[str, Any], action: str) -> bool:
        # Example ABAC check: only owner can edit
        owner = resource.get("owner")
        if action == "edit" and owner == principal:
            return True
        return False
