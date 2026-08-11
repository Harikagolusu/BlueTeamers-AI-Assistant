import pytest
from app.security.authorization.rbac import RoleManager, PermissionManager
from app.security.authorization.evaluators import AuthorizationService
from app.security.context.security_context import SecurityContext

def test_rbac_authorization():
    roles = RoleManager()
    perms = PermissionManager()
    
    roles.assign_role("alice", "admin")
    perms.assign_permission("admin", "read:all")
    perms.assign_permission("admin", "write:all")
    
    service = AuthorizationService(roles, perms)
    ctx = SecurityContext(principal="alice", roles=["admin"])
    
    assert service.authorize(ctx, "read:all") == True
    assert service.authorize(ctx, "delete:all") == False
