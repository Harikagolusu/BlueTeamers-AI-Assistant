from typing import Any, List, Dict
import json
import logging
from app.agents.base import BaseAgent
from app.agents.manifests.models import AgentManifest
from app.llm.schemas import LLMRequest
from app.prompt_builder.templates import TEMPLATES
from app.tools.context import ToolContext

logger = logging.getLogger(__name__)

class SOCAnalystAgent(BaseAgent):
    """
    Tier-1/Tier-2 SOC Analyst Agent acting as the 'Brain'.
    Orchestrates tools (the 'Hands') to investigate and map alerts.
    """
    def __init__(self, manifest: AgentManifest):
        super().__init__(manifest=manifest)
        self.investigation_context: Dict[str, Any] = {}
        
    async def initialize(self) -> None:
        logger.info(f"Initializing SOC Analyst Agent for session {self._context.conversation.session_id}")
            
    async def validate(self) -> None:
        if not self._context.conversation.session_id:
            raise ValueError("Session ID is required for SOC investigations.")
            
    async def prepare_context(self) -> None:
        # Load previous memory context
        pass
        
    async def plan(self) -> None:
        # Define the execution strategy
        logger.info("Planning investigation phases...")
        
    async def select_tools(self) -> List[Any]:
        # Fetch actual tools from registry based on manifest allowed tools
        # For simplicity in this implementation, we return the string names
        return self.manifest.tools
        
    async def execute_tools(self, tools: List[Any]) -> None:
        # In a real environment, we invoke the IToolExecutor here.
        # We store the results in self.investigation_context to be passed to the LLM.
        logger.info(f"Executing tools: {tools}")
        self.investigation_context["tool_outputs"] = "Mocked tool outputs for Timeline, IOCs, and MITRE mapping."
        
    async def reason(self) -> Any:
        try:
            template = TEMPLATES.get(self.manifest.prompt_template)
            sys_prompt = template.system_prompt if template else ""
            
            user_input = "Perform SOC Analysis on the following context:\n"
            user_input += json.dumps(self.investigation_context, indent=2)
            
            request = LLMRequest(
                prompt=user_input,
                system_prompt=sys_prompt,
                temperature=self.manifest.runtime_options.get("temperature", 0.1),
                max_tokens=self.manifest.runtime_options.get("max_tokens", 4000)
            )
            
            # Access LLM provider from runtime
            llm_provider = self._context.runtime.runtime_manager.llm_provider
            response = await llm_provider.generate(request)
            
            try:
                # Enforce JSON structured output as defined in the prompt
                return json.loads(response.text)
            except json.JSONDecodeError:
                return {
                    "summary": response.text,
                    "severity": "UNKNOWN",
                    "confidence": 0,
                    "analysis": "Raw text output. LLM failed to return structured JSON.",
                    "warnings": ["Invalid JSON output"]
                }
                
        except Exception as e:
            logger.error(f"SOC Agent reasoning failed: {e}")
            raise e
            
    async def post_process(self, result: Any) -> str:
        return json.dumps(result, indent=2) if isinstance(result, dict) else str(result)
