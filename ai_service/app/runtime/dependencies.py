from app.runtime.services.runtime_manager import RuntimeManager
from app.runtime.services.governance_service import RuntimeGovernanceService, SlidingWindowRateLimiter, DailyQuotaManager, ConfigFeatureFlagService, StructuredAuditLogger
from app.runtime.services.telemetry_service import RuntimeTelemetryService
from app.runtime.services.accounting_service import RuntimeAccountingService, TokenAccountant, ConfigurableCostCalculator
from app.observability.dependencies import get_observability_service

# Singleton instances for the runtime layer
_governance_service = RuntimeGovernanceService(
    rate_limiter=SlidingWindowRateLimiter(),
    quota_manager=DailyQuotaManager(),
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
