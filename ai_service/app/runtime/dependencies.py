from app.runtime.services.runtime_manager import RuntimeManager
from app.runtime.services.governance_service import RuntimeGovernanceService, SlidingWindowRateLimiter, ConfigFeatureFlagService, StructuredAuditLogger
from app.runtime.services.telemetry_service import RuntimeTelemetryService
from app.runtime.services.accounting_service import RuntimeAccountingService, TokenAccountant, ConfigurableCostCalculator
from app.runtime.services.token_usage_store import TokenUsageStore
from app.runtime.services.token_quota_manager import PersistentTokenQuotaManager
from app.observability.dependencies import get_observability_service

def _token_quota_manager() -> PersistentTokenQuotaManager:
    """Build the persistent daily+monthly token quota manager from settings."""
    from app.core.config import settings
    store = TokenUsageStore(db_path=settings.TOKEN_QUOTA_DB_PATH)
    store.prune_old()
    return PersistentTokenQuotaManager(
        store=store,
        daily_limit=settings.TOKEN_DAILY_LIMIT,
        monthly_limit=settings.TOKEN_MONTHLY_LIMIT,
        enforce=settings.TOKEN_QUOTA_ENFORCE,
    )

# Singleton instances for the runtime layer
_governance_service = RuntimeGovernanceService(
    rate_limiter=SlidingWindowRateLimiter(),
    quota_manager=_token_quota_manager(),
    feature_flags=ConfigFeatureFlagService(),
    audit_logger=StructuredAuditLogger()
)
_telemetry_service = RuntimeTelemetryService(observability=get_observability_service())
_accounting_service = RuntimeAccountingService(
    accountant=TokenAccountant(),
    cost_calculator=ConfigurableCostCalculator()
)

_runtime_manager = RuntimeManager(
    governance=_governance_service,
    telemetry=_telemetry_service,
    accounting=_accounting_service
)

def get_runtime_manager() -> RuntimeManager:
    return _runtime_manager
