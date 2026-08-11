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
    blocked_injection_patterns: List[str] = [
        r"ignore previous instructions",
        r"system prompt",
        r"bypass filters",
        r"you are now DAN"
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
