from pydantic_settings import BaseSettings
from pydantic import Field, field_validator, ConfigDict
from typing import List

class GuardrailsConfig(BaseSettings):
    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
    """Configuration for the Guardrails module."""
    
    # Global Settings
    guardrails_enabled: bool = True
    audit_mode_enabled: bool = False
    
    # Input Limits
    max_prompt_length: int = Field(default=32000, gt=0, description="Max allowed length for prompts")
    timeout_ms: int = Field(default=5000, gt=0, description="Timeout in ms for guardrail evaluation")
    
    # Security Patterns
    # Prompt-injection heuristics. Kept INTENT-SPECIFIC (targeting attempts to
    # override/extract this assistant's behaviour) so learners on a security
    # platform can still ask legitimate questions *about* these topics without
    # being blocked. All patterns are matched case-insensitively.
    blocked_injection_patterns: List[str] = [
        # Instruction-override attempts
        r"ignore previous instructions",
        r"ignore\s+(all|any|the)\s+(previous|prior|above|earlier)\s+(instructions?|prompts?|rules?|directions?)",
        r"disregard\s+(all\s+|your\s+|the\s+)?(previous|prior|above|earlier)\s+(instructions?|prompts?|rules?)",
        r"forget\s+(all\s+|your\s+|the\s+)?(previous|prior|above)\s+(instructions?|prompts?|rules?)",
        r"override\s+(your|the|all)\s+(system\s+)?(instructions?|prompts?|rules?|guardrails?|filters?)",
        r"bypass filters",
        # System-prompt extraction attempts (intent-specific; a bare "system
        # prompt" pattern used to false-positive on legitimate questions).
        r"(reveal|show|print|repeat|display|expose|leak|dump|spit\s+out)\s+(me\s+)?(your|the|its)\s+(system|initial|original|hidden)\s+(prompt|instructions?|message|directives?)",
        r"(what|whats|what's)\s+(is|are)\s+(your|the)\s+(system\s+prompt|hidden\s+instructions)",
        # Jailbreak personas / modes
        r"you are now DAN",
        r"(enter|enable|activate|switch\s+to)\s+developer\s+mode",
        r"act\s+as\s+(an?\s+)?(unfiltered|uncensored|unrestricted|evil)",
        r"(pretend|behave)\s+[^\n]{0,40}(no\s+rules|without\s+(any\s+)?restrictions|no\s+limits)",
        # Hosted-model template/delimiter smuggling
        r"<\|im_start\|>",
        r"<\|endoftext\|>",
    ]
    
    @field_validator('max_prompt_length')
    def validate_max_prompt_length(cls, v):
        if v <= 0:
            raise ValueError("max_prompt_length must be greater than 0")
        return v
        
    @field_validator('timeout_ms')
    def validate_timeout(cls, v):
        if v <= 0:
            raise ValueError("timeout_ms must be greater than 0")
        return v
