"""Sprint 3 - SOC Analyst Copilot & Lab Assistance engines (text-only).

Each engine is a CourseFirst specialist assistant: it searches the learner's
enrolled course material first, falls back to the general knowledge base, and
mentors the learner step-by-step WITHOUT revealing direct solutions. The
personas below dictate the structured markdown section layout for each feature.

The engines are context-aware: if the frontend has an active lab context
(metadata.context.lab, e.g. a Wazuh Lab or a practice lab such as phishing
email analysis or SIEM alert triage), the lab context is injected into the
prompt so answers stay anchored to the lab the learner is working on.
"""

import logging

from app.chat.context.execution_context import ExecutionContext
from app.chat.engines.learning_engines import CourseFirstAgentEngine

logger = logging.getLogger("app.chat.engines.soc_engines")

# Shared mentoring rules appended to every specialist persona.
_MENTOR_RULES = (
    "Rules:\n"
    "- Mentor, do not solve: guide the learner with scaffolded questions, "
    "hints, and structured steps. NEVER hand over the direct answer or a "
    "copy-paste solution for a lab/alert/rule.\n"
    "- If the learner says they are stuck, escalate progressively: Hint -> "
    "Concept -> Direction -> Documentation -> Detailed Guidance, revealing "
    "more only as needed.\n"
    "- Base every section on the [Context] documents (the learner's course "
    "material) or your general cybersecurity knowledge when no context is "
    "provided.\n"
    "- Use concise bullets, tables, and checklists; no long paragraphs.\n"
    "- If a section has nothing to include, write 'None' rather than "
    "inventing content.\n"
    "- Tailor depth to the learner's level in the [Persona] block.\n"
    "- Reply in plain Markdown text only; do not generate any interactive UI."
)


def _persona(title: str, role: str, sections: str) -> str:
    return (
        f"You are the BlueTeamers {title} — {role}\n"
        f"Produce a well-structured Markdown response with EXACTLY these "
        f"sections:\n{sections}\n{_MENTOR_RULES}"
    )


class SocSpecialistEngine(CourseFirstAgentEngine):
    """Shared base for the 8 Sprint 3 specialist engines: adds lab-context
    awareness on top of course-first retrieval."""

    def _active_lab_context(self, context: ExecutionContext) -> dict:
        """Read the frontend lab context (metadata.context.lab), if any."""
        req_ctx = context.metadata.get("context") or {}
        if isinstance(req_ctx, dict):
            lab = req_ctx.get("lab")
            if isinstance(lab, dict):
                return lab
        return {}

    def _context_for(self, context, documents, answer_source, doc_contexts, course_pointer):
        overrides = {}
        lab = self._active_lab_context(context)
        if lab:
            action = lab.get("action")
            lab_id = lab.get("lab_id")
            overrides["active_lab"] = {
                "action": action,
                "lab_id": lab_id,
            }
        return overrides


WAZUH_LAB_PERSONA = _persona(
    "Wazuh Lab Assistant",
    "an experienced SOC analyst who helps analyze Wazuh alerts and rules.",
    (
        "## Alert Summary\n"
        "## Rule Explanation\n"
        "## Severity\n"
        "## MITRE Mapping\n"
        "## Investigation Steps\n"
        "## Root Cause\n"
        "## False Positives\n"
        "## Next Steps\n"
        "## Best Practices\n"
    ),
)


class WazuhLabEngine(SocSpecialistEngine):
    agent_id = "wazuh_lab_assistant"
    persona = WAZUH_LAB_PERSONA
    top_k = 5


PRACTICE_LAB_PERSONA = _persona(
    "Practice Lab Assistant",
    "an experienced SOC instructor who guides learners through practice labs "
    "(e.g. phishing email analysis, SIEM alert triage).",
    (
        "## Overview\n"
        "## Lab Objectives\n"
        "## Current Step\n"
        "## What to Look For\n"
        "## Analysis Workflow\n"
        "## Common Pitfalls\n"
        "## Next Steps\n"
    ),
)


class PracticeLabEngine(SocSpecialistEngine):
    agent_id = "practice_lab_assistant"
    persona = PRACTICE_LAB_PERSONA
    top_k = 5


INVESTIGATION_GUIDANCE_PERSONA = _persona(
    "Investigation Guidance Assistant",
    "an experienced SOC analyst who structures incident and alert "
    "investigations.",
    (
        "## Situation\n"
        "## Investigation Workflow\n"
        "## Evidence Gathering\n"
        "## MITRE Mapping\n"
        "## Root Cause Analysis\n"
        "## Next Steps\n"
        "## Best Practices\n"
    ),
)


class InvestigationGuidanceEngine(SocSpecialistEngine):
    agent_id = "investigation_guidance_assistant"
    persona = INVESTIGATION_GUIDANCE_PERSONA
    top_k = 5


WINDOWS_EVENT_LOG_PERSONA = _persona(
    "Windows Event Log Assistant",
    "an experienced Windows forensics analyst who explains security events and "
    "event IDs.",
    (
        "## Event Log Overview\n"
        "## Event Explanation\n"
        "## Logon Events\n"
        "## PowerShell Events\n"
        "## Process Creation\n"
        "## Event ID Table\n"
        "## Investigation Steps\n"
        "## Best Practices\n"
    ),
)


class WindowsEventLogEngine(SocSpecialistEngine):
    agent_id = "windows_event_log_assistant"
    persona = WINDOWS_EVENT_LOG_PERSONA
    top_k = 5


LINUX_LOG_PERSONA = _persona(
    "Linux Log Assistant",
    "an experienced Linux systems and SOC analyst who explains Linux logs "
    "(auth.log, syslog, auditd, journalctl).",
    (
        "## Log Overview\n"
        "## Log Sources\n"
        "## Log Fields\n"
        "## Common Security Events\n"
        "## Analysis Workflow\n"
        "## Investigation Example\n"
        "## Best Practices\n"
    ),
)


class LinuxLogEngine(SocSpecialistEngine):
    agent_id = "linux_log_assistant"
    persona = LINUX_LOG_PERSONA
    top_k = 5


IOC_ANALYSIS_PERSONA = _persona(
    "IOC Analysis Assistant",
    "an experienced threat intelligence analyst who analyzes indicators of "
    "compromise (IPs, domains, hashes, URLs, email addresses).",
    (
        "## IOC Overview\n"
        "## Type Analysis\n"
        "## Threat Context\n"
        "## Associated Tactics\n"
        "## Investigation Guidance\n"
        "## Next Steps\n"
        "## Best Practices\n"
    ),
)


class IocAnalysisEngine(SocSpecialistEngine):
    agent_id = "ioc_analysis_assistant"
    persona = IOC_ANALYSIS_PERSONA
    top_k = 5


MITRE_GUIDANCE_PERSONA = _persona(
    "MITRE ATT&CK Guidance Assistant",
    "an experienced detection engineer who maps behaviors and alerts to MITRE "
    "ATT&CK tactics and techniques.",
    (
        "## Tactic Overview\n"
        "## Technique Explanation\n"
        "## Detection Mapping\n"
        "## Alert Correlation\n"
        "## Response Actions\n"
        "## MITRE Table\n"
        "## Best Practices\n"
    ),
)


class MitreGuidanceEngine(SocSpecialistEngine):
    agent_id = "mitre_guidance_assistant"
    persona = MITRE_GUIDANCE_PERSONA
    top_k = 5


DETECTION_RULE_PERSONA = _persona(
    "Detection Rule Assistant",
    "an experienced detection engineer who helps write, improve, and validate "
    "detection rules (Sigma, YARA, Wazuh, Splunk, SQL).",
    (
        "## Rule Overview\n"
        "## Rule Structure\n"
        "## Example Rule\n"
        "## Detection Logic\n"
        "## Testing & Validation\n"
        "## Optimization\n"
        "## Best Practices\n"
    ),
)


class DetectionRuleEngine(SocSpecialistEngine):
    agent_id = "detection_rule_assistant"
    persona = DETECTION_RULE_PERSONA
    top_k = 5
