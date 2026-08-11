import json
import logging
from typing import List, Any, Dict, Optional

from pydantic import ValidationError

from app.agents.base import BaseAgent
from app.agents.manifests.models import AgentManifest
from app.agents.models.agent_models import AgentState
from app.agents.events.event_bus import agent_event_bus
from app.agents.events.agent_events import AgentStartedEvent, AgentCompletedEvent
from app.agents.investigation.models import (
    InvestigationRequest,
    InvestigationContext,
    InvestigationResponse
)
from app.services.orchestration.service import AgentOrchestrationService
from app.services.workflow import (
    WorkflowBuilder,
    WorkflowExecutor,
    WorkflowContext
)
from app.shared.models.communication import AgentInvocation, AgentRequest, AgentExecutionContext
import uuid

logger = logging.getLogger(__name__)

class InvestigationAgent(BaseAgent):
    """
    Orchestration Agent for coordinating full security investigations.
    Leverages AgentOrchestrationService to invoke expert agents.
    """
    def __init__(self, manifest: AgentManifest, orchestration_service: AgentOrchestrationService):
        super().__init__(manifest)
        self.orchestration_service = orchestration_service
        self.investigation_context = InvestigationContext()
        self._tools: List[Any] = []

    def set_tools(self, tools: List[Any]):
        self._tools = tools

    async def initialize(self) -> None:
        logger.info(f"Initializing Investigation Agent for session {self._context.conversation.session_id}")

    async def validate(self) -> None:
        if not self._context or not self._context.conversation.session_id:
            raise ValueError("Invalid context: missing session_id")
        logger.info("Investigation Agent validation complete.")

    async def prepare_context(self) -> None:
        # Load from context, e.g. raw evidence
        if hasattr(self, "raw_evidence"):
            self.investigation_context.raw_request = InvestigationRequest(
                evidence_items=self.raw_evidence,
                investigation_goal="Perform comprehensive investigation."
            )
        logger.info("Context prepared.")

    async def plan(self) -> None:
        logger.info("Planning investigation strategy.")

    async def select_tools(self) -> List[Any]:
        return self._tools

    async def execute_tools(self, tools: List[Any]) -> None:
        """
        Executes internal tools and orchestrates expert agents using WorkflowEngine.
        """
        tools_dict = {t.name: t for t in tools}
        builder = WorkflowBuilder(workflow_id=f"inv_wf_{self._context.conversation.session_id}")
        
        # 1. Evidence Collection
        async def step1_collect(wf_ctx: WorkflowContext):
            if "evidence_collection_tool" in tools_dict:
                res = await tools_dict["evidence_collection_tool"].execute(
                    self._context, 
                    raw_evidence=self.investigation_context.raw_request.evidence_items if self.investigation_context.raw_request else []
                )
                self.investigation_context.collection = res
                return res
            return None
            
        builder.add_function_step("collection", step1_collect)

        # 2. Evidence Correlation
        async def step2_correlate(wf_ctx: WorkflowContext):
            if "evidence_correlation_tool" in tools_dict and self.investigation_context.collection:
                res = await tools_dict["evidence_correlation_tool"].execute(
                    self._context, 
                    evidence_items=self.investigation_context.collection.get("items", []) if isinstance(self.investigation_context.collection, dict) else self.investigation_context.collection.items
                )
                self.investigation_context.correlation = res
                return res
            return None
            
        builder.add_function_step("correlation", step2_correlate, depends_on=["collection"])

        # 3. Investigation Planning
        async def step3_plan(wf_ctx: WorkflowContext):
            if "investigation_planning_tool" in tools_dict:
                items = self.investigation_context.collection.get("items", []) if isinstance(self.investigation_context.collection, dict) else (self.investigation_context.collection.items if self.investigation_context.collection else [])
                res = await tools_dict["investigation_planning_tool"].execute(
                    self._context, 
                    evidence_types=[item.get("type", "unknown") if isinstance(item, dict) else item.type for item in items]
                )
                self.investigation_context.plan = res
                return res
            return None
            
        builder.add_function_step("planning", step3_plan, depends_on=["collection"])
        
        # 4. Orchestrate Expert Agents
        async def step4_orchestrate(wf_ctx: WorkflowContext):
            if self.investigation_context.plan and "required_expert_agents" in self.investigation_context.plan:
                agents_to_run = self.investigation_context.plan["required_expert_agents"]
                logger.info(f"Orchestrating expert agents: {agents_to_run}")
                
                invocations = []
                for agent_name in agents_to_run:
                    req = AgentRequest(request_id=str(uuid.uuid4()), session_id=self._context.conversation.session_id)
                    ctx = AgentExecutionContext(execution_id=str(uuid.uuid4()), session_id=self._context.conversation.session_id)
                    inv = AgentInvocation(invocation_id=str(uuid.uuid4()), target_agent=agent_name, request=req, context=ctx)
                    invocations.append(inv)
                
                results = await self.orchestration_service.invoke_agents_concurrently(invocations, self._context)
                
                for agent_name, result in results.items():
                    if result.success and result.response.success:
                        # Extract data from AgentResponse
                        data = result.response.data
                        parsed_resp = json.loads(data) if isinstance(data, str) else data
                        if agent_name == "soc_analyst":
                            self.investigation_context.soc_findings.append(parsed_resp)
                        elif agent_name == "threat_intelligence":
                            self.investigation_context.ti_findings.append(parsed_resp)
                    else:
                        errors = result.response.errors if result.response else ["Unknown error"]
                        logger.warning(f"Expert agent {agent_name} failed: {errors}. Proceeding with partial results.")
            return True
            
        builder.add_function_step("orchestration", step4_orchestrate, depends_on=["planning"])

        # 5. Timeline Generation
        async def step5_timeline(wf_ctx: WorkflowContext):
            if "incident_timeline_tool" in tools_dict:
                res = await tools_dict["incident_timeline_tool"].execute(
                    self._context, 
                    correlated_data={"correlation": self.investigation_context.correlation, "ti": self.investigation_context.ti_findings}
                )
                self.investigation_context.timeline = res
                return res
            return None
            
        builder.add_function_step("timeline", step5_timeline, depends_on=["correlation", "orchestration"])
        
        engine = builder.build()
        executor = WorkflowExecutor(engine)
        wf_context = WorkflowContext(workflow_id=engine.workflow_id, session_id=self._context.conversation.session_id)
        
        result = await executor.execute(wf_context)
        if not result.success:
            logger.error(f"Investigation workflow failed: {result.errors}")

    async def reason(self) -> Any:
        """
        Sends the compiled context to the LLM Provider to generate the final response.
        """
        logger.info("Executing reasoning phase to synthesize investigation report.")
        prompt_builder = self._context.runtime.prompt_builder
        system_prompt = prompt_builder.build("investigation_agent_system")
        
        # We pass the entire context state to the LLM
        context_str = self.investigation_context.model_dump_json()
        
        llm = self._context.runtime.runtime_manager.llm_provider
        response = await llm.generate(
            prompt=context_str,
            system_prompt=system_prompt,
            model=self.manifest.model,
            temperature=0.2
        )
        
        try:
            parsed = json.loads(response.text)
            validated = InvestigationResponse(**parsed)
            return validated.model_dump()
        except (json.JSONDecodeError, ValidationError) as e:
            logger.error(f"Failed to parse LLM response: {e}")
            return self._fallback_response()

    async def post_process(self, result: Any) -> str:
        return json.dumps(result) if isinstance(result, dict) else str(result)

    async def update_memory(self, final_response: str) -> None:
        logger.info("Updating memory with investigation results.")

    async def publish_events(self) -> None:
        logger.info("Publishing investigation lifecycle events.")

    async def cleanup(self) -> None:
        logger.info("Cleaning up investigation context.")
        self.investigation_context = InvestigationContext()

    def _fallback_response(self) -> Dict[str, Any]:
        return {
            "executive_summary": "Investigation encountered a processing error.",
            "evidence_collected": {"items": [], "total_count": 0},
            "evidence_correlation": {"correlated_entities": {}, "process_trees": [], "network_sessions": []},
            "soc_findings": [],
            "threat_intelligence_findings": [],
            "mitre_mapping": [],
            "incident_timeline": {"events": []},
            "affected_assets": [],
            "risk_assessment": "UNKNOWN",
            "confidence": 0,
            "recommendations": [{"action": "Review logs manually.", "priority": "HIGH", "description": "LLM failed to output structured response."}],
            "next_investigation_steps": [],
            "learning_guidance": "Always ensure the parser can handle unstructured outputs gracefully."
        }
