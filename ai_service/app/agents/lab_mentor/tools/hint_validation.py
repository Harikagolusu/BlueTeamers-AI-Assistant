from app.tools.base import BaseTool, ToolMetadata
from app.tools.context import ToolContext
from app.services.lab.models import HintValidationPolicy
from typing import Any

class HintValidationTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="hint_validation",
            metadata=ToolMetadata(
                input_schema={"hint_content": "str", "policy": "HintValidationPolicy"},
                output_schema={"is_safe": "bool", "feedback": "str"},
                tags=["lab", "validation", "anti-leakage"]
            )
        )

    async def execute(self, context: ToolContext, **kwargs) -> Any:
        hint_content = kwargs.get("hint_content", "").lower()
        policy = kwargs.get("policy")
        if not policy:
            policy = HintValidationPolicy()
            
        if not policy.anti_leakage_enabled:
            return {"is_safe": True, "feedback": "Hint is safe (anti-leakage disabled)."}

        # Validate against policy rules
        if policy.check_flags and ("flag{" in hint_content or "ctf{" in hint_content):
            return {"is_safe": False, "feedback": "Leakage detected! Hint contains flag format."}
            
        if policy.check_exact_answers and "answer is" in hint_content:
            return {"is_safe": False, "feedback": "Leakage detected! Hint contains explicit answer."}
            
        if policy.check_passwords and ("password123" in hint_content or "admin:" in hint_content):
            return {"is_safe": False, "feedback": "Leakage detected! Hint contains password."}
            
        if policy.check_api_keys and "ak_" in hint_content:
            return {"is_safe": False, "feedback": "Leakage detected! Hint contains API key."}
            
        if policy.check_tokens and "eyjh" in hint_content: # Common JWT prefix base64(eyJhbGciOi...)
            return {"is_safe": False, "feedback": "Leakage detected! Hint contains token."}

        return {"is_safe": True, "feedback": "Hint is safe."}
