from app.tools.base import BaseTool, ToolMetadata
from app.tools.context import ToolContext
from app.services.lab.models import ReflectionPrompt
from typing import Any

class ReflectionTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="reflection",
            metadata=ToolMetadata(
                input_schema={"action": "str"},
                output_schema={"reflection": "ReflectionPrompt"},
                tags=["lab", "reflection"]
            )
        )

    async def execute(self, context: ToolContext, **kwargs) -> Any:
        return ReflectionPrompt(
            what_happened="What exactly occurred during this step?",
            why_it_happened="Why do you think that specific parameter triggered an error?",
            evidence="What in the response body or headers supports this?",
            alternative_approach="What other tools could you have used?",
            detection_opportunity="How would a WAF detect this payload?",
            prevention_strategy="How should the vulnerable code be patched?",
            mitre_attack_mapping="Which MITRE ATT&CK technique does this map to?",
            real_soc_applicability="How does this apply to analyzing real-world web attacks?",
            expected_concept="SQL Injection fundamentals"
        )
