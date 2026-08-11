from typing import Any
from app.security.interfaces.i_authorization import IAuthorizationService, IRoleManager, IPermissionManager
from app.security.context.security_context import SecurityContext

class AuthorizationService(IAuthorizationService):
    def __init__(self, role_manager: IRoleManager, permission_manager: IPermissionManager):
        self._role_manager = role_manager
        self._permission_manager = permission_manager

    def authorize(self, context: SecurityContext, required_permission: str, resource: Any = None) -> bool:
        # RBAC Check
        roles = context.roles or self._role_manager.get_roles(context.principal)
        for role in roles:
            permissions = self._permission_manager.get_permissions(role)
            if required_permission in permissions or "*" in permissions:
                return True
        return False
