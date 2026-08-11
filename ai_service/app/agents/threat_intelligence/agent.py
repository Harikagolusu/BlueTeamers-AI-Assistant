import logging
import json
from typing import Any, List, Dict
from pydantic import ValidationError

from app.agents.base import BaseAgent
from app.agents.manifests.models import AgentManifest
from app.llm.schemas import LLMRequest
from app.prompt_builder.templates import TEMPLATES
from app.agents.threat_intelligence.models import ThreatIntelligenceResponse

logger = logging.getLogger(__name__)

class ThreatIntelligenceAgent(BaseAgent):
    """
    Threat Intelligence Agent specialized in CTI.
    Enriches indicators, correlates intelligence, and identifies threat actors/campaigns.
    Acts purely as the 'Brain' directing the 'Hands' (tools).
    """
    def __init__(self, manifest: AgentManifest):
        super().__init__(manifest=manifest)
        self.investigation_context: Dict[str, Any] = {}
        
    async def initialize(self) -> None:
        logger.info(f"Initializing Threat Intelligence Agent for session {self._context.conversation.session_id}")
            
    async def validate(self) -> None:
        logger.debug("Validating agent execution requirements.")
        if not self._context.conversation.session_id:
            raise ValueError("Session ID is required for CTI investigations.")
            
    async def prepare_context(self) -> None:
        logger.info("Preparing context from memory for Threat Intelligence Agent.")
        # In production, this would load previous memory context via self._context.memory_service
        self.investigation_context["historical_memory"] = "Loaded from memory service."
        
    async def plan(self) -> None:
        logger.info("Planning threat intelligence gathering phases...")
        self.investigation_context["plan"] = "Determine intent, select tools, and aggregate evidence."
        
    async def select_tools(self) -> List[Any]:
        logger.debug(f"Selecting tools based on manifest capabilities: {self.manifest.tools}")
        return self.manifest.tools
        
    async def execute_tools(self, tools: List[Any]) -> None:
        # In a real environment, this delegates to an IToolExecutor or similar runner.
        # It should only combine the evidence provided by tools.
        logger.info(f"Executing threat intel tools: {tools}")
        self.investigation_context["tool_outputs"] = "Mocked execution output aggregating IOCs, Reputation, Actors, and MITRE mapping."
        
    async def reason(self) -> Any:
        logger.info("Starting reasoning phase over collected evidence.")
        try:
            template = TEMPLATES.get(self.manifest.prompt_template)
            sys_prompt = template.system_prompt if template else ""
            user_template = template.user_prompt_template if template else "Perform Threat Intelligence Analysis on the following context:\n\n{context}"
            
            context_json = json.dumps(self.investigation_context, indent=2)
            user_input = user_template.replace("{context}", context_json)
            
            request = LLMRequest(
                prompt=user_input,
                system_prompt=sys_prompt,
                temperature=self.manifest.runtime_options.get("temperature", 0.1),
                max_tokens=self.manifest.runtime_options.get("max_tokens", 4000)
            )
            
            llm_provider = self._context.runtime.runtime_manager.llm_provider
            response = await llm_provider.generate(request)
            
            try:
                # Enforce JSON structured output as defined by ThreatIntelligenceResponse
                parsed_json = json.loads(response.text)
                # Validate against the Pydantic model
                validated_model = ThreatIntelligenceResponse(**parsed_json)
                return validated_model.model_dump()
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse LLM JSON output: {e}")
                return self._fallback_response(response.text, "Invalid JSON output")
            except ValidationError as ve:
                logger.error(f"LLM output failed schema validation: {ve}")
                return self._fallback_response(response.text, "Schema validation failed")
                
        except Exception as e:
            logger.error(f"Threat Intelligence Agent reasoning failed: {e}")
            raise e
            
    def _fallback_response(self, raw_text: str, reason: str) -> Dict[str, Any]:
        return {
            "executive_summary": "Analysis failed to produce structured output.",
            "indicator_details": [],
            "threat_assessment": {
                "risk_level": "UNKNOWN",
                "summary": f"Raw output fallback due to {reason}:\n{raw_text}",
                "affected_assets": []
            },
            "threat_intelligence": {
                "threat_actors": [],
                "campaigns": [],
                "related_malware": []
            },
            "mitre_attack_mapping": [],
            "evidence": [f"Failure reason: {reason}"],
            "confidence_score": 0,
            "recommended_next_steps": ["Review raw output manually", "Refine LLM prompt"],
            "references": []
        }

    async def post_process(self, result: Any) -> str:
        logger.debug("Generating final string response.")
        return json.dumps(result, indent=2) if isinstance(result, dict) else str(result)
        
    async def update_memory(self, final_response: str) -> None:
        logger.info("Storing generated response into memory.")
        # In production, self._context.memory_service.store(...)
        pass
        
    async def publish_events(self) -> None:
        logger.debug("Emitting queued events.")
        # Super class handles _publish_immediate, this hook is for final sweeps
        pass
        
    async def cleanup(self) -> None:
        logger.info("Cleaning up agent resources.")
        self.investigation_context.clear()

