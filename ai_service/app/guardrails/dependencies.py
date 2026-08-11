from functools import lru_cache
from app.guardrails.config.guardrails_config import GuardrailsConfig
from app.guardrails.domain.services.policy_registry import PolicyRegistry
from app.guardrails.domain.services.guardrails_service import GuardrailsService
from app.guardrails.pipeline.input_pipeline import InputPipeline
from app.guardrails.pipeline.output_pipeline import OutputPipeline
from app.guardrails.groups.validation_group import ValidationGroup
from app.guardrails.groups.security_group import SecurityGroup
from app.guardrails.groups.compliance_group import ComplianceGroup
from app.guardrails.policies.input.length_validation_policy import LengthValidationPolicy
from app.guardrails.policies.input.injection_detection_policy import InjectionDetectionPolicy
from app.guardrails.infrastructure.adapters.regex_engine_adapter import RegexEngineAdapter
from app.observability.dependencies import get_observability_service
from app.observability.service import ObservabilityService
from fastapi import Depends

@lru_cache()
def get_guardrails_config() -> GuardrailsConfig:
    return GuardrailsConfig()

@lru_cache()
def get_policy_registry() -> PolicyRegistry:
    config = get_guardrails_config()
    registry = PolicyRegistry()
    
    # Validation Group
    validation_group = ValidationGroup()
    validation_group.add_policy(LengthValidationPolicy(max_length=config.max_prompt_length))
    registry.register_group(validation_group)
    
    # Security Group
    security_group = SecurityGroup()
    regex_engine = RegexEngineAdapter(patterns=config.blocked_injection_patterns)
    security_group.add_policy(InjectionDetectionPolicy(regex_engine=regex_engine))
    registry.register_group(security_group)
    
    # Compliance Group
    compliance_group = ComplianceGroup()
    # Currently empty, no policies implemented yet.
    registry.register_group(compliance_group)
    
    # Startup validation
    registry.validate_registry()
    
    return registry

def get_guardrails_service(
    observability: ObservabilityService = Depends(get_observability_service)
) -> GuardrailsService:
    config = get_guardrails_config()
    registry = get_policy_registry()
    
    input_pipeline = InputPipeline()
    output_pipeline = OutputPipeline()
    
    # Add groups to pipelines
    for group in registry.get_all_groups():
        input_pipeline.add_group(group)
        output_pipeline.add_group(group)
        
    return GuardrailsService(
        config=config,
        registry=registry,
        input_pipeline=input_pipeline,
        output_pipeline=output_pipeline,
        observability=observability
    )
