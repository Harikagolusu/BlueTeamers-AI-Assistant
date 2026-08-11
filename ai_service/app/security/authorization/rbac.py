from typing import List, Dict
from app.security.interfaces.i_authorization import IRoleManager, IPermissionManager

class RoleManager(IRoleManager):
    def __init__(self):
        self._user_roles: Dict[str, List[str]] = {}

    def assign_role(self, principal: str, role: str) -> None:
        if principal not in self._user_roles:
            self._user_roles[principal] = []
        self._user_roles[principal].append(role)

    def get_roles(self, principal: str) -> List[str]:
        return self._user_roles.get(principal, [])

class PermissionManager(IPermissionManager):
    def __init__(self):
        self._role_permissions: Dict[str, List[str]] = {}

    def assign_permission(self, role: str, permission: str) -> None:
        if role not in self._role_permissions:
            self._role_permissions[role] = []
        self._role_permissions[role].append(permission)

    def get_permissions(self, role: str) -> List[str]:
        return self._role_permissions.get(role, [])
