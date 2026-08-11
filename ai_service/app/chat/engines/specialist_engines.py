from app.chat.engines.agent_backed_engine import AgentBackedEngine
from app.models.chat.chat_models import ExecutionResult
from app.chat.context.execution_context import ExecutionContext

import logging
import re

logger = logging.getLogger("app.chat.engines.specialist_engines")


class LearningCoachExecutionEngine(AgentBackedEngine):
    agent_id = "learning_coach"
    supports_recommendations = True
    persona = (
        "You are the BlueTeamers Learning Coach. You build personalized learning "
        "roadmaps, study plans, and skill-gap analysis grounded in BlueTeamers "
        "course content. Use the retrieved course material for accuracy. Recommend "
        "only courses that exist in the BlueTeamers catalog."
    )


class ThreatIntelExecutionEngine(AgentBackedEngine):
    agent_id = "threat_intelligence"

    EXTERNAL_FALLBACK_PERSONA = (
        "You are the BlueTeamers Threat Intelligence Analyst — an experienced "
        "SOC analyst. The learner asked about a specific CVE, IOC, malware "
        "family, threat actor, attack technique, or vulnerability.\n"
        "The requested item was NOT found in the BlueTeamers knowledge base, so "
        "external threat-intelligence tool results are provided below where "
        "available.\n"
        "Produce a well-structured Markdown response with EXACTLY these "
        "sections where applicable:\n"
        "## Overview\n"
        "## Technical Details\n"
        "## Risk Level\n"
        "## MITRE ATT&CK Mapping (if applicable)\n"
        "## Indicators\n"
        "## Detection Guidance\n"
        "## Mitigation\n"
        "## Best Practices\n"
        "## References (when available)\n"
        "Rules:\n"
        "- Use the [External Tool Results] below as your primary evidence. They "
        "are the result of live external threat-intel lookups.\n"
        "- You MAY also use your own general cybersecurity knowledge to "
        "interpret and expand the tool results, but clearly label which "
        "statements come from the external tool results vs your general "
        "knowledge.\n"
        "- If both the external tools and your knowledge are insufficient, say "
        "so plainly and state exactly what additional evidence would be needed. "
        "Never fabricate specific IOCs, CVSS scores, or attacker infrastructure."
        "\n"
        "- Use concise bullets, tables, and checklists; no long paragraphs.\n"
        "- Tailor depth to the learner's level in the [Persona] block.\n"
        "- Reply in plain Markdown text only; do not generate any interactive "
        "UI."
    )

    persona = (
        "You are the BlueTeamers Threat Intelligence Analyst — an experienced "
        "SOC analyst. The learner asked about a specific CVE, IOC, malware "
        "family, threat actor, attack technique, or vulnerability.\n"
        "Produce a well-structured Markdown response with EXACTLY these "
        "sections where applicable:\n"
        "## Overview\n"
        "## Technical Details\n"
        "## Risk Level\n"
        "## MITRE ATT&CK Mapping (if applicable)\n"
        "## Indicators\n"
        "## Detection Guidance\n"
        "## Mitigation\n"
        "## Best Practices\n"
        "## References (when available)\n"
        "Rules:\n"
        "- Ground your answer strictly in the retrieved [Context] knowledge "
        "base.\n"
        "- If the requested indicator / CVE / actor / technique is NOT present "
        "in the knowledge base, state clearly that the information is "
        "unavailable instead of fabricating unsupported details, and suggest "
        "what evidence would be needed.\n"
        "- Use concise bullets, tables, and checklists; no long paragraphs.\n"
        "- Tailor depth to the learner's level in the [Persona] block.\n"
        "- Reply in plain Markdown text only; do not generate any interactive "
        "UI."
    )

    def __init__(self, retriever, llm_service, prompt_builder, external_tools=None):
        super().__init__(retriever, llm_service, prompt_builder)
        self._external_tools = external_tools or []

    # --- entity extraction & coverage detection ----------------------------
    _CVE_RE = re.compile(r"CVE-\d{4}-\d{4,7}", re.IGNORECASE)
    _TID_RE = re.compile(r"T\d{4}(?:\.\d{3})?", re.IGNORECASE)
    _IP_RE = re.compile(
        r"(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}"
        r"(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"
    )
    _DOMAIN_RE = re.compile(r"\b(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z]{2,}\b", re.IGNORECASE)
    _HASH_RE = re.compile(r"\b(?:[a-f0-9]{32}|[a-f0-9]{40}|[a-f0-9]{64})\b", re.IGNORECASE)

    def _extract_entities(self, query: str) -> list:
        entities = []
        for pattern, kind in (
            (self._CVE_RE, "CVE"),
            (self._TID_RE, "MITRE_TID"),
            (self._IP_RE, "IP_ADDRESS"),
            (self._DOMAIN_RE, "DOMAIN"),
            (self._HASH_RE, "HASH"),
        ):
            for match in set(pattern.findall(query)):
                entities.append((kind, match.upper() if kind in ("CVE", "MITRE_TID") else match.lower()))
        return entities

    def _entity_in_docs(self, entity, documents) -> bool:
        """Best-effort: is the entity literally mentioned in any retrieved doc?"""
        if not entity:
            return True
        for doc in documents:
            content = getattr(doc, "content", "") or ""
            if isinstance(content, str) and entity.lower() in content.lower():
                return True
        return False

    async def _run_external_tools(self, entity_kind: str, entity: str) -> list:
        """Best-effort external threat-intel lookups. Never raises."""
        results = []
        for tool in self._external_tools:
            try:
                from app.tools.context import ToolContext

                ctx = ToolContext(agent_id=self.agent_id)
                if entity_kind == "MITRE_TID":
                    payload = {"technique_id": entity}
                elif entity_kind == "HASH":
                    payload = {"indicator": entity, "type": "hash"}
                elif entity_kind == "IP_ADDRESS":
                    payload = {"indicator": entity, "type": "ip"}
                elif entity_kind == "DOMAIN":
                    payload = {"indicator": entity, "type": "domain"}
                else:
                    payload = {"indicator": entity, "type": "cve"}
                output = await tool.execute(ctx, **payload)
                results.append({
                    "tool": getattr(tool, "name", "unknown"),
                    "input": {**payload},
                    "output": output,
                })
            except Exception as e:
                logger.warning(f"External threat-intel tool failed: {e}")
        return results

    # --- persona / context hooks -------------------------------------------
    def _persona_for(self, context, documents, answer_source):
        return self.persona

    def _context_for(self, context, documents, answer_source, doc_contexts, course_pointer):
        return {}

    async def execute(self, context: ExecutionContext) -> ExecutionResult:
        query = context.metadata.get("query", "")
        documents, answer_source = await self._retrieve(query, context)

        entities = self._extract_entities(query)
        missing = [(kind, entity) for kind, entity in entities if not self._entity_in_docs(entity, documents)]

        if entities and missing:
            return await self._execute_with_external_fallback(
                context, query, documents, answer_source, missing
            )
        return await super().execute(context)

    async def _execute_with_external_fallback(
        self, context, query, documents, answer_source, missing
    ):
        """Runs external tool enrichment, then asks the LLM to synthesize an
        answer grounded in tool results + the model's own knowledge."""
        from app.models.chat.chat_models import ExecutionResult

        doc_contexts = [{"content": d.content, "metadata": d.metadata} for d in documents]

        tool_results = []
        for kind, entity in missing:
            tool_results.extend(await self._run_external_tools(kind, entity))

        metadata = {
            "agent": self.agent_id,
            "engine": self.name,
            "sources": doc_contexts,
            "llm_used": True,
            "recommendation_used": False,
            "repositories": [],
            "intent": context.metadata.get("intent", ""),
            "domain": context.metadata.get("domain", ""),
            "answer_source": answer_source,
            "external_fallback": True,
            "external_tool_results": tool_results,
            "external_entities": [e for _, e in missing],
        }
        metadata["course_sources"] = self._build_course_sources(documents)

        enhanced_context = {
            **context.memory,
            "retrieved_documents": doc_contexts,
            "agent_persona": self.EXTERNAL_FALLBACK_PERSONA,
            "answer_source": answer_source,
            "course_pointer": "",
            "external_fallback": True,
            "external_tool_results": tool_results,
        }
        prompt, system_prompt = self._prompt_builder.build_prompt(query, enhanced_context)
        from app.prompt_builder.simple_prompt_builder import RESPONSE_STYLE_BLOCK
        combined_system = f"{system_prompt}\n\n{self.EXTERNAL_FALLBACK_PERSONA}\n\n{RESPONSE_STYLE_BLOCK}"

        images = context.metadata.get("images")
        if context.streaming_mode:
            generator = self._llm.stream(prompt, system_prompt=combined_system, images=images)
            return ExecutionResult.success(
                engine=self.name,
                message="[Streaming Generator]",
                metadata={"generator": generator, **metadata},
                documents=doc_contexts,
            )

        response = await self._llm.generate(prompt, system_prompt=combined_system, images=images)
        return ExecutionResult.success(
            engine=self.name,
            message=response,
            metadata=metadata,
            documents=doc_contexts,
        )

    def _build_course_sources(self, documents):
        from app.chat.engines.course_sources import build_course_sources

        return build_course_sources(documents, progress_by_slug=None)


class InvestigationExecutionEngine(AgentBackedEngine):
    agent_id = "investigation_assistant"
    persona = (
        "You are the BlueTeamers Investigation Assistant. Guide incident triage, "
        "evidence correlation, and investigation timelines using the retrieved "
        "BlueTeamers lesson content. Structure findings clearly and flag missing "
        "evidence honestly."
    )

    LOG_ANALYSIS_PERSONA = (
        "You are the BlueTeamers Investigation Assistant, acting as a senior SOC "
        "analyst performing log analysis.\n"
        "The user attached one or more log/data files. Their FULL content is "
        "provided above in the <attachment> blocks — analyze that content directly, "
        "never invent lines, events, or IOCs that are not present in it.\n"
        "Structure your analysis with clear markdown headings:\n"
        "## Executive Summary\n"
        "## Key Observations\n"
        "## Anomalies / Indicators of Interest\n"
        "## Severity Assessment\n"
        "## Recommended Next Steps\n"
        "Use concise bullet points. If the logs show no suspicious activity, say so "
        "plainly and describe the normal behavior instead. Do not recommend or "
        "reference BlueTeamers courses for this request — this is a direct "
        "investigation, not a lesson question."
    )

    _LOG_DATA_EXTS = (".log", ".csv", ".json", ".xml", ".txt", ".md", ".yaml", ".yml")

    def _has_log_attachment(self, context: ExecutionContext) -> bool:
        files: list = context.metadata.get("files") or []
        if not files:
            return False
        for f in files:
            name = (f.get("name") or "").lower()
            ftype = (f.get("type") or "").lower()
            if any(name.endswith(ext) for ext in self._LOG_DATA_EXTS) or ftype.startswith("text/"):
                return True
        return False

    async def execute(self, context: ExecutionContext) -> ExecutionResult:
        # Log/data analysis is a direct investigation: the file content is
        # already in the query (AttachmentParseStage), so we do NOT retrieve
        # course material or attach course-source cards.
        if self._has_log_attachment(context):
            return await self._execute_log_analysis(context)
        return await super().execute(context)

    async def _execute_log_analysis(self, context: ExecutionContext) -> ExecutionResult:
        query = context.metadata.get("query", "")

        metadata = {
            "agent": self.agent_id,
            "engine": self.name,
            "sources": [],
            "llm_used": True,
            "recommendation_used": False,
            "repositories": [],
            "intent": context.metadata.get("intent", ""),
            "domain": context.metadata.get("domain", ""),
            "answer_source": "log_attachment",
        }

        enhanced_context = {
            **context.memory,
            "retrieved_documents": [],
            "agent_persona": self.LOG_ANALYSIS_PERSONA,
            "log_analysis": True,
        }
        prompt, system_prompt = self._prompt_builder.build_prompt(query, enhanced_context)
        from app.prompt_builder.simple_prompt_builder import RESPONSE_STYLE_BLOCK
        combined_system = f"{system_prompt}\n\n{self.LOG_ANALYSIS_PERSONA}\n\n{RESPONSE_STYLE_BLOCK}"

        images = context.metadata.get("images")
        if context.streaming_mode:
            generator = self._llm.stream(
                prompt, system_prompt=combined_system, images=images
            )
            return ExecutionResult.success(
                engine=self.name,
                message="[Streaming Generator]",
                metadata={"generator": generator, **metadata},
            )

        response = await self._llm.generate(
            prompt, system_prompt=combined_system, images=images
        )
        return ExecutionResult.success(
            engine=self.name,
            message=response,
            metadata=metadata,
        )


class LabMentorExecutionEngine(AgentBackedEngine):
    agent_id = "lab_mentor"
    persona = (
        "You are the BlueTeamers Lab Mentor. Guide learners through hands-on labs "
        "with hints and scaffolded questions WITHOUT revealing the solution. Use "
        "the retrieved lesson material to keep guidance accurate."
    )

    def __init__(self, retriever, llm_service, prompt_builder, lab_manager=None):
        super().__init__(retriever, llm_service, prompt_builder)
        self._lab_manager = lab_manager

    async def execute(self, context):
        lab = context.metadata.get("lab")
        if lab and lab.get("active") and self._lab_manager is not None:
            return await self._lab_manager.handle(context)
        return await super().execute(context)


class AssessmentCoachExecutionEngine(AgentBackedEngine):
    agent_id = "assessment_coach"
    persona = (
        "You are the BlueTeamers Assessment Coach. Prepare learners for quizzes, "
        "assessments, and certification readiness. Ask practice questions, explain "
        "answers with the retrieved course material, and assess readiness honestly."
    )
