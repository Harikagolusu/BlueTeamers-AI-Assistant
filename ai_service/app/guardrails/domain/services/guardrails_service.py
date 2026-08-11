import logging
import time
from app.guardrails.domain.interfaces.service_interface import IGuardrailsService
from app.guardrails.domain.models.context import GuardrailContext
from app.guardrails.pipeline.input_pipeline import InputPipeline
from app.guardrails.pipeline.output_pipeline import OutputPipeline
from app.guardrails.domain.services.policy_registry import PolicyRegistry
from app.guardrails.config.guardrails_config import GuardrailsConfig
from app.observability.service import ObservabilityService

logger = logging.getLogger(__name__)

class GuardrailsService(IGuardrailsService):
    """Facade for executing guardrails validation."""
    
    def __init__(self, config: GuardrailsConfig, registry: PolicyRegistry, input_pipeline: InputPipeline, output_pipeline: OutputPipeline, observability: ObservabilityService = None):
        self._config = config
        self._registry = registry
        self._input_pipeline = input_pipeline
        self._output_pipeline = output_pipeline
        self._observability = observability

    async def validate_input(self, context: GuardrailContext) -> GuardrailContext:
        if not self._config.guardrails_enabled:
            logger.info("Guardrails disabled. Skipping input validation.")
            return context
            
        context.is_audit_mode = self._config.audit_mode_enabled
        start_time = time.time()
        
        try:
            result = await self._input_pipeline.execute(context)
            if self._observability:
                self._observability.observe_histogram("guardrails_input_latency_ms", (time.time() - start_time) * 1000)
                self._observability.increment_counter("guardrails_input_evaluated")
            return result
        except Exception as e:
            if self._observability:
                self._observability.increment_counter("guardrails_input_blocked")
                self._observability.log_warning(f"Request blocked: {str(e)}", trace_id=context.trace_id)
            raise

    async def validate_output(self, context: GuardrailContext) -> GuardrailContext:
        if not self._config.guardrails_enabled:
            return context
            
        context.is_audit_mode = self._config.audit_mode_enabled
        start_time = time.time()
        
        try:
            result = await self._output_pipeline.execute(context)
            if self._observability:
                self._observability.observe_histogram("guardrails_output_latency_ms", (time.time() - start_time) * 1000)
                self._observability.increment_counter("guardrails_output_evaluated")
            return result
        except Exception as e:
            if self._observability:
                self._observability.increment_counter("guardrails_output_blocked")
                self._observability.log_warning(f"Response blocked: {str(e)}", trace_id=context.trace_id)
            raise

    async def get_health_status(self) -> dict:
        groups = self._registry.get_all_groups()
        registered_groups = [g.name for g in groups]
        registered_policies = [p.name for g in groups for p in g.policies]
        
        return {
            "status": "healthy" if self._config.guardrails_enabled else "disabled",
            "enabled": self._config.guardrails_enabled,
            "audit_mode": self._config.audit_mode_enabled,
            "registered_groups": registered_groups,
            "registered_policies": registered_policies,
            "pipeline_health": "ok"
        }
