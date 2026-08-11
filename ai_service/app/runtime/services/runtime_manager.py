from typing import Callable, Any, Awaitable
from app.runtime.interfaces.manager import IRuntimeManager
from app.runtime.models.context import RuntimeContext
from app.runtime.services.governance_service import RuntimeGovernanceService
from app.runtime.services.telemetry_service import RuntimeTelemetryService
from app.runtime.services.accounting_service import RuntimeAccountingService
from app.chat.exceptions.handlers import handle_chat_exception
from app.runtime.context_manager import RuntimeContextManager

class RuntimeManager(IRuntimeManager):
    """
    The Single Runtime Façade.
    Coordinates Governance, Telemetry, Accounting, and Resilience.
    """
    def __init__(
        self,
        governance: RuntimeGovernanceService,
        telemetry: RuntimeTelemetryService,
        accounting: RuntimeAccountingService
    ):
        self.governance = governance
        self.telemetry = telemetry
        self.accounting = accounting

    async def execute_with_governance(self, operation: Callable[..., Awaitable[Any]], context: RuntimeContext, *args, **kwargs) -> Any:
        # Pre-execution Governance
        user_id = context.user_id or "anonymous"
        
        # 1. Rate Limiting
        allowed = await self.governance.rate_limiter.check_limit(user_id, endpoint="chat")
        if not allowed:
            RuntimeContextManager.update(rate_limit_status="THROTTLED")
            raise Exception("Rate limit exceeded")
            
        # 2. Quota
        has_quota = await self.governance.quota_manager.check_quota(user_id)
        if not has_quota:
            RuntimeContextManager.update(quota_status="EXHAUSTED")
            raise Exception("Quota exhausted")
            
        # 3. Execution
        try:
            result = await operation(*args, **kwargs)
            return result
        finally:
            # Post-execution Accounting/Governance
            current_ctx = RuntimeContextManager.get()
            total_tokens = current_ctx.token_usage.total_tokens
            if total_tokens > 0:
                await self.governance.quota_manager.increment_usage(user_id, total_tokens)
                
            await self.governance.audit_logger.log_event("EXECUTION_COMPLETED", user_id, {
                "trace_id": current_ctx.trace_id,
                "tokens": total_tokens,
                "cost": current_ctx.cost.total_cost
            })

    async def execute_with_resilience(self, operation: Callable[..., Awaitable[Any]], *args, **kwargs) -> Any:
        # Note: The actual runtime resilience strategies (Retry, Timeout, CircuitBreaker)
        # are injected at the Execution Engine level (RuntimePolicyProxy)
        # This method can be used for higher-level resilience if needed.
        return await operation(*args, **kwargs)

    async def check_health(self) -> dict:
        return {"status": "healthy", "components": ["governance", "telemetry", "accounting"]}
