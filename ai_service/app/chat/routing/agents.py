"""Canonical agent catalog.

Exactly ONE agent is selected per request. Each agent maps to an execution
engine owned by the ExecutionEngineFactory. Platform recommendations are owned
by engines (never by the router, RAG, or keyword matching).
"""
from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from app.chat.routing.domains import CyberDomain


class Agent(BaseModel):
    agent_id: str
    name: str
    description: str
    domain: CyberDomain
    engine: str
    capabilities: List[str] = Field(default_factory=list)
    llm_required: bool = True
    supports_recommendations: bool = False
    priority: int = 0


_AGENTS = [
    Agent(
        agent_id="general_assistant",
        name="General Assistant",
        description="Handles greetings, small talk and general conversation.",
        domain=CyberDomain.GENERAL,
        engine="GENERAL",
        capabilities=["conversation", "greeting"],
        llm_required=True,
        priority=10,
    ),
    Agent(
        agent_id="knowledge_assistant",
        name="Knowledge Assistant",
        description="Explains cybersecurity concepts from the BlueTeamers knowledge base.",
        domain=CyberDomain.KNOWLEDGE,
        engine="RAG",
        capabilities=["concept_explanation", "knowledge_retrieval"],
        llm_required=True,
        priority=10,
    ),
    Agent(
        agent_id="learning_coach",
        name="Learning Coach",
        description="Builds learning roadmaps, study plans and skill-gap analysis.",
        domain=CyberDomain.LEARNING,
        engine="LEARNING_COACH",
        capabilities=["learning_path", "skill_gap_analysis", "roadmap"],
        llm_required=True,
        supports_recommendations=True,
        priority=20,
    ),
    Agent(
        agent_id="threat_intelligence",
        name="Threat Intelligence",
        description="Answers questions about threat actors, TTPs, IOCs and campaigns.",
        domain=CyberDomain.THREAT_INTEL,
        engine="THREAT_INTEL",
        capabilities=["threat_intelligence", "ioc_enrichment", "mitre_mapping"],
        llm_required=True,
        priority=20,
    ),
    Agent(
        agent_id="investigation_assistant",
        name="Investigation Assistant",
        description="Guides incident triage, evidence correlation and investigation timelines.",
        domain=CyberDomain.INVESTIGATION,
        engine="INVESTIGATION",
        capabilities=["evidence_correlation", "timeline_generation", "investigation"],
        llm_required=True,
        priority=20,
    ),
    Agent(
        agent_id="platform_assistant",
        name="Platform Assistant",
        description="Answers account questions: courses, progress, certificates, assessments, profile.",
        domain=CyberDomain.PLATFORM,
        engine="PLATFORM",
        capabilities=["platform_account", "enrollment", "progress"],
        llm_required=False,
        supports_recommendations=True,
        priority=20,
    ),
    Agent(
        agent_id="lab_mentor",
        name="Lab Mentor",
        description="Guides learners through hands-on labs without revealing solutions.",
        domain=CyberDomain.LAB,
        engine="LAB_MENTOR",
        capabilities=["lab_mentoring"],
        llm_required=True,
        priority=10,
    ),
    Agent(
        agent_id="assessment_coach",
        name="Assessment Coach",
        description="Prepares learners for quizzes, assessments and certifications.",
        domain=CyberDomain.ASSESSMENT,
        engine="ASSESSMENT_COACH",
        capabilities=["readiness_assessment", "adaptive_assessment"],
        llm_required=True,
        priority=10,
    ),
    Agent(
        agent_id="soc_analyst",
        name="SOC Analyst",
        description="Performs tool-backed analysis tasks such as log and alert review.",
        domain=CyberDomain.TOOLING,
        engine="TOOL",
        capabilities=["tool_execution", "log_analysis"],
        llm_required=True,
        priority=10,
    ),
    Agent(
        agent_id="wazuh_lab_assistant",
        name="Wazuh Lab Assistant",
        description="Answers questions about Wazuh alerts and rules, guiding step-by-step alert analysis and basic rule writing.",
        domain=CyberDomain.WAZUH_LAB,
        engine="WAZUH_LAB",
        capabilities=["wazuh_alert_analysis", "rule_explanation"],
        llm_required=True,
        priority=20,
    ),
    Agent(
        agent_id="practice_lab_assistant",
        name="Practice Lab Assistant",
        description="Guides learners through practice labs (phishing email analysis, SIEM alert triage) without revealing solutions.",
        domain=CyberDomain.PRACTICE_LAB,
        engine="PRACTICE_LAB",
        capabilities=["practice_lab_mentoring"],
        llm_required=True,
        priority=20,
    ),
    Agent(
        agent_id="investigation_guidance_assistant",
        name="Investigation Guidance Assistant",
        description="Provides structured investigation workflows for alerts, incidents, and breaches.",
        domain=CyberDomain.INVESTIGATION_GUIDANCE,
        engine="INVESTIGATION_GUIDANCE",
        capabilities=["investigation_workflow", "evidence_gathering"],
        llm_required=True,
        priority=20,
    ),
    Agent(
        agent_id="windows_event_log_assistant",
        name="Windows Event Log Assistant",
        description="Explains Windows security events, event IDs, and logon/PowerShell/process-creation analysis.",
        domain=CyberDomain.WINDOWS_EVENT_LOG,
        engine="WINDOWS_EVENT_LOG",
        capabilities=["windows_event_analysis", "event_id_explanation"],
        llm_required=True,
        priority=20,
    ),
    Agent(
        agent_id="linux_log_assistant",
        name="Linux Log Assistant",
        description="Explains Linux system logs (auth.log, syslog, auditd, journalctl) and how to analyze them.",
        domain=CyberDomain.LINUX_LOG,
        engine="LINUX_LOG",
        capabilities=["linux_log_analysis"],
        llm_required=True,
        priority=20,
    ),
    Agent(
        agent_id="ioc_analysis_assistant",
        name="IOC Analysis Assistant",
        description="Analyzes indicators of compromise (IPs, domains, hashes, URLs, email addresses) and guides investigation.",
        domain=CyberDomain.IOC_ANALYSIS,
        engine="IOC_ANALYSIS",
        capabilities=["ioc_analysis", "threat_context"],
        llm_required=True,
        priority=20,
    ),
    Agent(
        agent_id="mitre_guidance_assistant",
        name="MITRE ATT&CK Guidance Assistant",
        description="Explains MITRE ATT&CK tactics and techniques and maps alerts and behaviors to techniques.",
        domain=CyberDomain.MITRE_GUIDANCE,
        engine="MITRE_GUIDANCE",
        capabilities=["mitre_mapping", "detection_mapping"],
        llm_required=True,
        priority=20,
    ),
    Agent(
        agent_id="detection_rule_assistant",
        name="Detection Rule Assistant",
        description="Helps write, improve, and validate detection rules (Sigma, YARA, Wazuh, Splunk, SQL).",
        domain=CyberDomain.DETECTION_RULE,
        engine="DETECTION_RULE",
        capabilities=["rule_authoring", "rule_validation"],
        llm_required=True,
        priority=20,
    ),
]


class AgentCatalog:
    def __init__(self, agents: List[Agent] | None = None):
        self._agents: List[Agent] = agents or list(_AGENTS)
        self._by_id: Dict[str, Agent] = {a.agent_id: a for a in self._agents}

    def list_agents(self) -> List[Agent]:
        return list(self._agents)

    def get(self, agent_id: str) -> Optional[Agent]:
        return self._by_id.get(agent_id)

    def select_for_domain(self, domain: CyberDomain) -> Agent:
        """Select exactly one agent for a domain (highest priority wins)."""
        matches = [a for a in self._agents if a.domain == domain]
        if not matches:
            matches = [a for a in self._agents if a.domain == CyberDomain.GENERAL]
        return max(matches, key=lambda a: a.priority)

    def engine_for_domain(self, domain: CyberDomain) -> str:
        return self.select_for_domain(domain).engine
