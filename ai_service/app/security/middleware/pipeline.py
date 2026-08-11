from typing import Callable, Any, Dict
from app.security.interfaces.i_authentication import IAuthenticationService
from app.security.interfaces.i_context import ISecurityContextProvider
from app.security.interfaces.i_authorization import IAuthorizationService
from app.security.interfaces.i_policy import IPolicyEnforcementPoint
from app.security.interfaces.i_governance import IGovernanceService
from app.security.context.security_context import SecurityContext

class SecurityMiddlewarePipeline:
    def __init__(
        self,
        auth_service: IAuthenticationService,
        context_provider: ISecurityContextProvider,
        authz_service: IAuthorizationService,
        pep: IPolicyEnforcementPoint,
        governance: IGovernanceService
    ):
        self._auth_service = auth_service
        self._context_provider = context_provider
        self._authz_service = authz_service
        self._pep = pep
        self._governance = governance

    async def execute(self, request: Any, next_handler: Callable) -> Any:
        # 1. Authentication Middleware
        token = getattr(request, "token", None)
        if not token:
            # Depending on platform, may allow anonymous access
            claims = {"principal": "anonymous", "roles": []}
        else:
            claims = self._auth_service.validate_request(token)
            
        # 2. Security Context Middleware
        ctx = SecurityContext(
            principal=claims["principal"],
            roles=claims.get("claims", {}).get("roles", []),
            token_metadata=claims
        )
        self._context_provider.set_context(ctx)
        
        try:
            # 3. Authorization Middleware
            required_permission = getattr(request, "required_permission", None)
            if required_permission:
                if not self._authz_service.authorize(ctx, required_permission, request):
                    raise PermissionError(f"Principal {ctx.principal} lacks permission {required_permission}")
                    
            # 4. Policy Enforcement Middleware
            action = getattr(request, "action", "execute")
            self._pep.enforce(ctx, request, action)
            
            # 5. Governance Middleware
            self._governance.enforce_governance(ctx, request)
            
            # 6. Proceed to Business Pipeline
            return await next_handler(request)
        finally:
            # Clean up context
            self._context_provider.clear_context()
