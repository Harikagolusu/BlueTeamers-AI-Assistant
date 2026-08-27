from typing import Dict, Any, List
import re
from app.chat.intent.interfaces import IIntentClassifier
from app.chat.intent.models.entities import EntityCollection
from app.chat.intent.models.intent_types import IntentType
from app.chat.intent.models.analysis_result import DetectedIntent
from app.chat.intent.catalog_vocabulary import catalog_terms_in_query

# STEP 3A: Deterministic no-RAG for clearly conversational messages (imported
# from routing to keep single source of truth, zero LLM cost).
try:
    from app.chat.routing.domains import is_conversational_no_rag
except ImportError:
    # Fallback if routing not yet loaded (circular import safety)
    def is_conversational_no_rag(query: str) -> bool:  # type: ignore
        return False


def _has_word(query_lower: str, word: str) -> bool:
    """Word-boundary aware presence check (avoids 'exam' matching 'example')."""
    if re.search(rf"\b{re.escape(word)}\b", query_lower):
        return True
    # Simple plural-aware matching: firewall -> firewalls, event log -> event logs,
    # vulnerability -> vulnerabilities.
    if not word.endswith(("s", "es", "ies")):
        if re.search(rf"\b{re.escape(word)}s\b", query_lower):
            return True
        if word.endswith("y") and len(word) > 1 and word[-2] not in "aeiou":
            stem = word[:-1] + "ies"
            if re.search(rf"\b{re.escape(stem)}\b", query_lower):
                return True
    return False


def _has_phrase(query_lower: str, phrase: str) -> bool:
    return phrase in query_lower


# ------------------------------------------------------------------ #
# Platform detection signals (specificity-ordered).
# The FIRST matching group wins → the most specific platform intent.
# ------------------------------------------------------------------ #
_PLATFORM_ASSESSMENT = [
    "assessment", "assessments", "quiz", "quizzes", "exam", "exams",
    "grade", "grades", "score", "scores", "which assessment",
    "recommend an assessment",
]
_PLATFORM_CERTIFICATE = [
    "certificate", "certificates", "certification", "certifications",
    "my certificates", "cert status",
]
_PLATFORM_PROGRESS = [
    "progress", "completion", "completed", "how far am i",
    "am i done", "percent complete", "percent done",
]
_PLATFORM_PROFILE = ["profile", "my account", "account settings"]
_PLATFORM_DASHBOARD = ["dashboard", "my overview", "my stats", "my summary"]
_PLATFORM_BADGE = ["badge", "badges", "achievement", "achievements"]
_PLATFORM_LEARNING_PATH = ["learning path", "learning paths", "career path", "career paths"]
_PLATFORM_LAB_ACTION = [
    "start lab", "start my lab", "start the lab", "launch lab", "launch my lab",
    "open my lab", "open the lab", "resume lab", "resume my lab", "continue lab",
    "begin lab", "begin my lab", "my labs", "my lab",
    # Explicit practice-lab launch verbs keep PLATFORM routing; mentoring
    # questions ("how do I ... practice lab") route to the Sprint 3
    # PRACTICE_LAB specialist engine instead.
    "start practice lab", "start my practice lab", "start the practice lab",
    "launch practice lab", "launch my practice lab", "open practice lab",
    "resume practice lab", "begin practice lab", "my practice labs",
]
_PLATFORM_COURSE = [
    "enroll", "enrolled", "enrollment", "enrolment", "suggest", "recommend",
    "recommendation", "recommendations", "course", "courses", "my courses",
    "next course", "next courses", "which course", "which courses",
    "what course", "what courses", "courses do i", "resume", "continue learning",
    "continue my", "where was i", "bought", "purchase", "purchases", "purchased",
    "buy", "subscription", "upgrade", "paid", "have access", "do i have",
    "course catalog", "course catalogue", "available courses", "take next",
    "should i take", "recommend a course",
]

# ------------------------------------------------------------------ #
# Sprint 2 content-generation signals: notes, topic summaries, threat intel.
# These fire only when no platform intent claimed the query, so account/course
# queries keep their authoritative PLATFORM routing.
# ------------------------------------------------------------------ #
_NOTES_SIGNALS = [
    "generate notes", "create notes", "make notes", "write notes",
    "prepare notes", "take notes", "note down", "notes for", "notes on",
    "notes about", "study notes", "revision notes", "revision material",
    "interview notes", "interview preparation notes", "cheat sheet",
    "cheatsheet", "quick notes", "short notes", "summary notes",
    "exam notes", "key notes", "concise notes",
]

_TOPIC_SUMMARY_SIGNALS = [
    "summarize", "summarise", "summary", "summarization", "summarize this",
    "summarize today", "summarize the", "quick revision", "revision points",
    "explain in short", "in short", "explain briefly", "tl;dr", "tldr",
    "recap", "sum it up", "gist", "key points of", "key takeaways of",
    "brief me", "brief summary", "short version", "overview of the lesson",
]

_THREAT_INTEL_SIGNALS = [
    "malware family", "threat actor", "threat group", "attack technique",
    "explain this ioc", "explain the ioc", "ioc analysis", "ioc report",
    "indicator of compromise", "explain this vulnerability",
    "explain this exploit", "explain this malware", "apt group",
    "campaign", "tell me about this threat", "exploit analysis",
    "tell me about cve", "explain cve", "cve analysis", "threat intelligence",
]

# Lab mentor help markers. LAB_ASSISTANT only fires when the user asks for
# help/guidance with a lab, so concept questions that merely mention a lab
# stay on the knowledge/RAG path. Platform lab actions ("start lab", "my lab")
# are claimed by _PLATFORM_LAB_ACTION above.
_LAB_HELP_MARKERS = [
    "help", "stuck", "hint", "hints", "step", "steps", "guide", "guidance",
    "troubleshoot", "fix", "error", "not working", "can't", "cant", "cannot",
    "assist", "walk me through", "proceed", "next step", "do next", "try",
    "run", "complete", "finish", "stuck on", "where do i", "what do i do",
]

# ------------------------------------------------------------------ #
# Sprint 3 - SOC Analyst Copilot specialist intents (text-only).
# These fire when no platform intent claimed the query and no log/data
# attachment is present (attachments stay on the investigation path).
# Each scores above generic RAG (max 0.9) so it routes to a dedicated
# CourseFirst specialist engine that mentors rather than reveals answers.
# ------------------------------------------------------------------ #
_WAZUH_SIGNALS = [
    "wazuh", "ossec", "syscheck", "filebeat", "wazuh alert", "wazuh alerts",
    "wazuh rule", "wazuh rules", "wazuh agent", "wazuh dashboard",
    "wazuh log", "wazuh logs", "alert id", "rule id", "rule level",
    "active response", "integrity monitoring",
]

_PRACTICE_LAB_SIGNALS = [
    "practice lab", "practice labs", "hands-on lab", "hands on lab",
    "lab exercise", "lab exercises", "lab walkthrough",
    "walk me through the lab", "phishing email analysis", "phishing lab",
    "email analysis lab", "siem alert triage", "alert triage lab",
    "triage lab", "try the lab",
]

_INVESTIGATION_GUIDANCE_SIGNALS = [
    "how do i investigate", "how to investigate", "investigate an alert",
    "investigate the alert", "investigate an incident", "investigate the incident",
    "investigate a breach", "investigate this alert", "investigation guidance",
    "investigation steps", "investigation process", "investigation workflow",
    "guide me through the investigation", "guide my investigation",
    "alert investigation", "incident investigation", "triage an alert",
    "triage the alert", "how to triage", "investigate this event",
    "how to analyze an alert", "how do i analyze an alert",
]

_WINDOWS_EVENT_LOG_SIGNALS = [
    "windows event", "windows events", "windows log", "windows logs",
    "event id", "event ids", "event viewer", "event log analysis",
    "security log", "security logs", "security event", "security events",
    "logon event", "logon events", "logon type", "windows audit",
    "audit policy", "powershell event", "powershell events",
    "process creation", "eventlog", "windows security log",
]

_WINDOWS_EVENT_IDS = (
    "4624", "4625", "4672", "4688", "4697", "4698", "4720", "4732",
    "4768", "4771", "5156", "1102", "4104", "7045", "4728", "4740",
)

_LINUX_LOG_SIGNALS = [
    "linux log", "linux logs", "linux log analysis", "auth.log", "auth log",
    "auth logs", "secure log", "secure logs", "var/log", "syslog",
    "journalctl", "auditd", "dmesg", "sshd", "failed password",
    "failed passwords", "authentication failure", "authentication failures",
    "cron log", "cron logs", "ufw log", "apache log", "nginx log",
    "linux audit", "lastlog", "system log", "system logs",
]

_IOC_ANALYSIS_SIGNALS = [
    "ioc analysis", "ioc report", "analyze this ioc", "analyse this ioc",
    "explain this ioc", "explain the ioc", "indicator of compromise",
    "indicators of compromise", "malicious ip", "malicious domain",
    "malicious hash", "malicious url", "malicious email",
    "suspicious ip", "suspicious domain", "suspicious hash", "suspicious url",
    "is this ip", "is this domain", "is this hash", "is this url",
    "hash analysis", "ip analysis", "domain analysis", "url analysis",
    "ioc enrichment", "ioc indicator", "ioc indicators",
    "what does this ip", "what does this hash", "what does this domain",
    "phishing domain", "c2 ip", "command and control ip",
]

# Additional analysis framing words used when an IP/domain entity is present,
# e.g. "is 45.77.1.2 malicious?" or "analyze example.com".
_IOC_ANALYSIS_WORDS = [
    "analyze", "analyse", "analysis", "malicious", "suspicious", "ioc",
    "threat", "reputation", "check", "is this", "what does", "verdict",
    "blocklist", "sandbox", "investigate", "indicator", "detect",
]

_MITRE_GUIDANCE_SIGNALS = [
    "mitre", "att&ck", "attack matrix", "mitre framework", "attack framework",
    "attack technique", "attack techniques", "attack tactic", "attack tactics",
    "mitre mapping", "mitre map", "mitre matrix", "kill chain mapping",
    "map to mitre", "tactics and techniques", "tactics and procedures",
    "technique id", "ttp", "ttps", "attack chain",
]

_DETECTION_RULE_SIGNALS = [
    "sigma rule", "sigma rules", "detection rule", "detection rules",
    "detection logic", "detection engineering", "correlation rule",
    "correlation rules", "yara rule", "yara rules", "snort rule",
    "suricata rule", "splunk query", "kql", "alert rule", "alert rules",
    "write a detection", "build a detection", "detection query",
    "rule example", "rule examples", "detection use case",
]


# ------------------------------------------------------------------ #
# RAG (static knowledge) detection signals.
# ------------------------------------------------------------------ #
# Trigger phrases: explicit learning/intent framing.
_RAG_TRIGGER_PHRASES = [
    "what is", "what are", "what does", "what do", "what was", "what were",
    "how do", "how does", "how to", "how can", "how is", "how are",
    "explain", "define", "meaning of", "what means", "what mean",
    "tell me about", "tell me how", "describe", "show me a", "show me an",
    "show me how", "difference between", "for beginners", "in simple words",
    "in simple terms", "learn about", "want to understand",
    "i don't understand", "i dont understand", "confused", "not clear",
    "clarify", "doubt", "walkthrough", "example", "examples", "explain in",
]

# Content references: the user is asking about course material itself.
_RAG_CONTENT_REFS = [
    "module", "lesson", "section", "chapter", "topic", "concept",
    "lecture", "lab", "course content", "learning path",
]

# Cybersecurity domain lexicon → content that exists in the vector store.
# Word-boundary matched so short acronyms (dns, tcp, c2) do not collide.
_RAG_DOMAIN_TERMS = [
    # SIEM / SOC
    "siem", "security information and event management",
    "soc", "security operations center", "security operations",
    "soc analyst", "triage",
    # MITRE / frameworks
    "mitre", "att&ck", "attack framework", "attack matrix", "ttp",
    "kill chain", "cyber kill chain", "cybersecurity framework", "nist",
    # Detection
    "sigma", "detection rule", "detection engineering", "detection rules",
    "detection", "alerting", "correlation rule", "correlation rules",
    "yara", "snort", "suricata", "zeek", "splunk", "qradar",
    "elastic", "kibana", "kql", "sentinel", "use case", "use cases",
    # Logs & events
    "event log", "event logs", "event id", "event ids", "windows event",
    "event viewer", "log analysis", "log management", "log parsing",
    "syslog", "windows registry",
    # Indicators
    "ioc", "iocs", "indicator of compromise", "indicators of compromise",
    "osint", "stix", "taxii", "indicator", "indicators",
    # Vulnerabilities / scoring
    "cve", "cves", "cvss", "vulnerability management", "vulnerability scanning",
    "exposure", "cwe",
    # Network
    "firewall", "intrusion detection", "intrusion prevention", "idps",
    "waf", "network monitoring", "network traffic", "packet capture",
    "pcap", "tcpdump", "wireshark", "tcp", "udp", "dns", "http",
    "https", "tls", "port", "ports", "syn flood", "ddos", "dos attack",
    "protocol", "subnet", "vpn", "proxy",
    # Malware & phishing
    "malware", "ransomware", "virus", "trojan", "worm", "spyware",
    "keylogger", "rootkit", "phishing", "spear phishing", "social engineering",
    "payload", "exploit", "zero day", "zero-day", "shellcode", "obfuscation",
    "packing", "botnet",
    # Threat behavior
    "command and control", "c2 server", "beacon", "beaconing", "exfiltration",
    "lateral movement", "privilege escalation", "persistence",
    "reconnaissance", "threat hunting", "threat intelligence",
    "threat intel", "incident response", "adversary", "attack chain",
    "credentials", "credential", "kerberos", "ntlm", "active directory",
    "authentication bypass", "sql injection", "xss", "injection",
    # Tools / roles / operations
    "endpoint detection", "edr", "xdr", "vulnerability", "vulnerabilities",
    "penetration testing", "red team", "blue team", "security analyst",
    "monitoring", "hunting", "forensics", "digital forensics",
    "blue teamer", "defensive security", "defense", "detect",
]


# ------------------------------------------------------------------ #
# Off-topic gating: clearly non-cybersecurity content is refused so the
# assistant only answers security content. A query is OFF_TOPIC only when
# it matches the off-topic lexicon AND carries NO cybersecurity signal.
# ------------------------------------------------------------------ #
_OFF_TOPIC_SIGNALS = [
    # Entertainment
    "joke", "jokes", "funny", "meme", "movie", "movies", "film", "song",
    "songs", "music", "singer", "celebrity", "gossip", "football", "cricket",
    "basketball", "soccer", "sports", "gaming", "fifa",
    # Food
    "recipe", "recipes", "cook", "cooking", "restaurant", "pizza", "dinner",
    "lunch", "breakfast", "baking", "bake",
    # Travel / weather / leisure
    "travel", "vacation", "holiday", "flight", "trip", "beach", "weather",
    "forecast", "temperature",
    # General trivia / academia (non-security)
    "capital of", "geography", "history", "literature", "math", "mathematics",
    "algebra", "calculus", "physics", "chemistry", "biology", "poem", "poetry",
    "novel", "book summary",
    # Programming languages (non-security framing)
    "python", "javascript", "java", "c++", "c#", "ruby", "golang", "html",
    "css", "react", "node.js",
    # Other unrelated topics
    "astrology", "horoscope", "zodiac", "politics", "election", "stock market",
    "economy", "dating", "relationship", "fashion", "shopping", "astronomy",
]

# Broad cybersecurity vocabulary used only by the OFF_TOPIC gate. If ANY of
# these is present the query is treated as in-scope even if the off-topic
# lexicon also matched (e.g. "python used for security automation").
_CYBER_RELEVANCE_EXTRA = [
    "security", "secure", "securing", "protection", "protect", "cyber",
    "cybersecurity", "threat", "threats", "hack",
    "hacking", "hacker", "attack", "attacker", "attackers", "malware", "virus",
    "phishing", "firewall", "network", "networking", "wifi", "router",
    "password", "passwords", "encrypt", "encryption", "decrypt", "login",
    "privacy", "breach", "ioc", "cve", "exploit", "vulnerability",
    "vulnerabilities", "siem", "soc", "edr", "endpoint", "ransomware", "botnet",
    "ddos", "logs", "forensic", "forensics", "incident", "intrusion", "packet",
    "vpn", "detection", "monitoring", "alert", "triage", "response", "malicious",
    "compromised", "authentication", "data breach",
]


def _matches_any(query_lower: str, terms: List[str]) -> List[str]:
    """Return the subset of terms present in the query (word-boundary)."""
    return [t for t in terms if _has_word(query_lower, t)]


def _matches_any_phrase(query_lower: str, phrases: List[str]) -> List[str]:
    return [p for p in phrases if _has_phrase(query_lower, p)]


def _has_cyber_relevance(query_lower: str) -> bool:
    """True if the query contains any broad cybersecurity vocabulary."""
    if _matches_any(query_lower, _RAG_DOMAIN_TERMS):
        return True
    if _matches_any_phrase(query_lower, _CYBER_RELEVANCE_EXTRA):
        return True
    return False


class RuleIntentClassifier(IIntentClassifier):
    """
    Intent classification for the request router.

    Priority:
      1. Attachments (images / files)  -> IMAGE_CHAT / DOCUMENT_CHAT / INVESTIGATION
      2. Off-topic gate (cybersecurity-only scope) -> OFF_TOPIC
      3. Platform signals (specificity-ordered, word-boundary matched)
      4. Investigation keywords
      5. RAG (static knowledge) — domain-gated
      6. Tool actions
      7. Greetings
      8. General chat fallback
    """
    async def classify(self, query: str, context: Dict[str, Any], entities: EntityCollection) -> List[DetectedIntent]:
        query_lower = query.lower()
        candidate_intents: List[DetectedIntent] = []

        # 1. Attachments
        images = context.get("images", [])
        if images:
            candidate_intents.append(DetectedIntent(
                type=IntentType.IMAGE_CHAT,
                confidence=0.0,
                reason="Context contains images.",
                matched_features=["image_attached"],
            ))

        files = context.get("files", [])
        if files:
            log_exts = (".log", ".csv", ".json", ".xml")
            doc_exts = (".pdf", ".docx", ".txt", ".md")
            has_logs = any(any(f.get("name", "").lower().endswith(ext) for ext in log_exts) for f in files)
            has_docs = any(any(f.get("name", "").lower().endswith(ext) for ext in doc_exts) for f in files)
            if has_logs:
                candidate_intents.append(DetectedIntent(
                    type=IntentType.INVESTIGATION,
                    confidence=0.0,
                    reason="Context contains log/data files.",
                    matched_features=["log_file_attached"],
                ))
            else:
                candidate_intents.append(DetectedIntent(
                    type=IntentType.DOCUMENT_CHAT,
                    confidence=0.0,
                    reason="Context contains document files.",
                    matched_features=["document_file_attached"],
                ))

        # 2. Off-topic gate — the assistant answers ONLY cybersecurity content.
        # Fires before platform/greeting signals so platform lexicons cannot
        # claim clearly off-topic queries (e.g. "recommend a movie", "score").
        # Triple safety: off-topic lexicon AND no cyber vocabulary AND no catalog
        # term AND no security entity. Attachments already won above.
        off_topic_matched = _matches_any(query_lower, _OFF_TOPIC_SIGNALS)
        if (
            off_topic_matched
            and not _has_cyber_relevance(query_lower)
            and not catalog_terms_in_query(query_lower)
            and not (entities.has("CVE") or entities.has("MITRE_TID"))
        ):
            return [DetectedIntent(
                type=IntentType.OFF_TOPIC,
                confidence=0.9,
                reason="Query is outside the cybersecurity scope.",
                matched_features=off_topic_matched,
            )]

        # 2. Platform signals — most specific intent wins (first match in priority order).
        # Skip platform if the query is a transformation with untrusted content
        # (e.g., "Summarize this text: ... course data ...") - the "course" in
        # the data to be transformed should not trigger platform.
        is_transformation = any(p in query_lower for p in ["summarize this text:", "summarize this:", "translate this text:", "translate this:", "analyze this text:"])
        has_exclusion = "do not" in query_lower and any(n in query_lower for n in ["course", "progress", "account", "personal"])
        platform_specs = [
            (IntentType.PLATFORM_ASSESSMENT, _PLATFORM_ASSESSMENT),
            (IntentType.PLATFORM_CERTIFICATE, _PLATFORM_CERTIFICATE),
            (IntentType.PLATFORM_PROGRESS, _PLATFORM_PROGRESS),
            (IntentType.PLATFORM_PROFILE, _PLATFORM_PROFILE),
            (IntentType.PLATFORM_DASHBOARD, _PLATFORM_DASHBOARD),
            (IntentType.PLATFORM_BADGE, _PLATFORM_BADGE),
            (IntentType.PLATFORM_LEARNING_PATH, _PLATFORM_LEARNING_PATH),
            (IntentType.PLATFORM_LAB, _PLATFORM_LAB_ACTION),
            (IntentType.PLATFORM_COURSE, _PLATFORM_COURSE),
        ]
        platform_intent = None
        # For transformation content, only check the instruction prefix, not the data after colon
        query_for_platform = query_lower.split(":", 1)[0] if is_transformation and ":" in query_lower else query_lower
        # If the query explicitly says "do not" + platform, don't treat the platform words as intent
        if has_exclusion and ("what is 2" in query_lower or "summarize" in query_lower or "translate" in query_lower or "explain malware" in query_lower):
            # This is an exclusion/privacy request with a non-platform question, skip platform
            platform_intent = None
        else:
            for intent_type, signals in platform_specs:
                # For transformation, use the prefix only
                check_q = query_for_platform
                matched = _matches_any(check_q, signals)
                if matched:
                    platform_intent = DetectedIntent(
                        type=intent_type,
                    confidence=0.0,
                    reason=f"Matched {intent_type.value} platform keywords.",
                    matched_features=matched,
                )
                break

        if platform_intent:
            candidate_intents.append(platform_intent)

        # 3. Sprint 2 content-generation intents: notes, topic summaries, and
        # threat intelligence. These only fire when no platform intent claimed
        # the query (so account/course queries keep their PLATFORM routing) and
        # when no log/data attachment is present (attachments stay on the
        # investigation path).
        if platform_intent is None and not files:
            notes_matched = _matches_any_phrase(query_lower, _NOTES_SIGNALS)
            if notes_matched:
                candidate_intents.append(DetectedIntent(
                    type=IntentType.NOTES_GENERATION,
                    confidence=0.0,
                    reason="Matched notes-generation signals.",
                    matched_features=notes_matched,
                ))

            summary_matched = _matches_any_phrase(query_lower, _TOPIC_SUMMARY_SIGNALS)
            if summary_matched:
                candidate_intents.append(DetectedIntent(
                    type=IntentType.TOPIC_SUMMARY,
                    confidence=0.0,
                    reason="Matched topic-summary signals.",
                    matched_features=summary_matched,
                ))

            threat_matched = _matches_any_phrase(query_lower, _THREAT_INTEL_SIGNALS)
            has_cve_entity = entities.has("CVE")
            if threat_matched or has_cve_entity:
                features = threat_matched
                if has_cve_entity:
                    features = list(dict.fromkeys(features + ["cve_entity"]))
                candidate_intents.append(DetectedIntent(
                    type=IntentType.THREAT_INTEL,
                    confidence=0.0,
                    reason="Matched threat-intelligence signals.",
                    matched_features=features,
                ))

        # 4. Sprint 3 SOC specialist intents (text-only mentoring assistants).
        # Fire only when no platform intent claimed the query, no log/data
        # attachment is present, and no explicit content-generation request
        # (notes / summary) was made — so account/course queries stay on
        # PLATFORM, attached log files stay on the INVESTIGATION path, and
        # "make a cheat sheet for MITRE" stays a NOTES request.
        if platform_intent is None and not files and not notes_matched and not summary_matched:
            wazuh_matched = _matches_any(query_lower, _WAZUH_SIGNALS)
            wazuh_alert = bool(re.search(r"\balert\s+\d+\b", query_lower))
            if wazuh_matched or wazuh_alert:
                features = wazuh_matched + (["wazuh_alert_id"] if wazuh_alert else [])
                candidate_intents.append(DetectedIntent(
                    type=IntentType.WAZUH_LAB,
                    confidence=0.0,
                    reason="Matched Wazuh/SOC alert signals.",
                    matched_features=features,
                ))

            practice_lab_matched = _matches_any_phrase(query_lower, _PRACTICE_LAB_SIGNALS)
            if practice_lab_matched:
                candidate_intents.append(DetectedIntent(
                    type=IntentType.PRACTICE_LAB,
                    confidence=0.0,
                    reason="Matched practice-lab signals.",
                    matched_features=practice_lab_matched,
                ))

            investigation_matched = _matches_any_phrase(query_lower, _INVESTIGATION_GUIDANCE_SIGNALS)
            if investigation_matched:
                candidate_intents.append(DetectedIntent(
                    type=IntentType.INVESTIGATION_GUIDANCE,
                    confidence=0.0,
                    reason="Matched investigation-guidance signals.",
                    matched_features=investigation_matched,
                ))

            windows_matched = _matches_any(query_lower, _WINDOWS_EVENT_LOG_SIGNALS)
            windows_event_id = bool(re.search(rf"\b(?:{'|'.join(_WINDOWS_EVENT_IDS)})\b", query_lower))
            windows_id_ref = bool(re.search(r"\bevent\s+id\s+\d+\b", query_lower))
            if windows_matched or windows_event_id or windows_id_ref:
                features = windows_matched
                if windows_event_id:
                    features = list(dict.fromkeys(features + ["windows_event_id"]))
                candidate_intents.append(DetectedIntent(
                    type=IntentType.WINDOWS_EVENT_LOG,
                    confidence=0.0,
                    reason="Matched Windows event-log signals.",
                    matched_features=features,
                ))

            linux_matched = _matches_any(query_lower, _LINUX_LOG_SIGNALS)
            if linux_matched:
                candidate_intents.append(DetectedIntent(
                    type=IntentType.LINUX_LOG,
                    confidence=0.0,
                    reason="Matched Linux log signals.",
                    matched_features=linux_matched,
                ))

            ioc_matched = _matches_any_phrase(query_lower, _IOC_ANALYSIS_SIGNALS)
            has_ip_or_domain = entities.has("IP_ADDRESS") or entities.has("DOMAIN")
            ioc_entity_analysis = has_ip_or_domain and any(
                word in query_lower for word in _IOC_ANALYSIS_WORDS
            )
            if ioc_matched or ioc_entity_analysis:
                features = ioc_matched
                if ioc_entity_analysis:
                    features = list(dict.fromkeys(features + ["ip_domain_entity"]))
                candidate_intents.append(DetectedIntent(
                    type=IntentType.IOC_ANALYSIS,
                    confidence=0.0,
                    reason="Matched IOC analysis signals.",
                    matched_features=features,
                ))

            mitre_matched = _matches_any(query_lower, _MITRE_GUIDANCE_SIGNALS)
            has_mitre_tid = entities.has("MITRE_TID")
            if mitre_matched or has_mitre_tid:
                features = mitre_matched
                if has_mitre_tid:
                    features = list(dict.fromkeys(features + ["mitre_technique_id"]))
                candidate_intents.append(DetectedIntent(
                    type=IntentType.MITRE_GUIDANCE,
                    confidence=0.0,
                    reason="Matched MITRE ATT&CK signals.",
                    matched_features=features,
                ))

            detection_rule_matched = _matches_any_phrase(query_lower, _DETECTION_RULE_SIGNALS)
            if detection_rule_matched:
                candidate_intents.append(DetectedIntent(
                    type=IntentType.DETECTION_RULE,
                    confidence=0.0,
                    reason="Matched detection-rule signals.",
                    matched_features=detection_rule_matched,
                ))

        # 5. Investigation by keyword
        inv_keywords = ["analyze log", "investigate", "forensics", "pcap", "incident", "breach"]
        inv_matched = _matches_any_phrase(query_lower, inv_keywords)
        if inv_matched:
            candidate_intents.append(DetectedIntent(
                type=IntentType.INVESTIGATION,
                confidence=0.0,
                reason="Matched investigation keywords.",
                matched_features=inv_matched,
            ))

        # 4. RAG (static knowledge) — domain-gated
        trigger_matched = _matches_any_phrase(query_lower, _RAG_TRIGGER_PHRASES)
        content_ref_matched = _matches_any(query_lower, _RAG_CONTENT_REFS)
        domain_matched = _matches_any(query_lower, _RAG_DOMAIN_TERMS)
        # Data-driven domain signal: does the query share content-bearing terms
        # with the course catalog? Requires at least two distinct catalog terms
        # so single generic topic words ("python", "cloud") do not over-trigger.
        # Keeps the gate aligned with the knowledge base instead of a
        # hand-maintained keyword list.
        catalog_matched = catalog_terms_in_query(query_lower)
        catalog_strong = len(catalog_matched) >= 2
        has_entity = entities.has("CVE") or entities.has("MITRE_TID")

        # A query is a knowledge query when it is explicitly framed as one
        # AND concerns material that lives in the static knowledge base
        # (cyber domain term, catalog vocabulary, security entity, or course
        # content reference). The catalog signal makes this robust to topic gaps
        # in the hand-written domain lexicon (e.g. "endpoint security").
        explicit_knowledge = trigger_matched and (
            bool(domain_matched) or has_entity or content_ref_matched or catalog_strong
        )
        # Pure domain queries ("SIEM vs SOC", "endpoint security") are knowledge
        # queries even without an explicit framing phrase, as long as no platform
        # intent claimed them.
        pure_domain = (bool(domain_matched) or has_entity or catalog_strong) and platform_intent is None and not trigger_matched
        # A bare security entity ("T1059", "CVE-2024-1234") is a knowledge query.
        entity_only = has_entity and platform_intent is None and not trigger_matched and not pure_domain

        # STEP 3A: Skip RAG for clearly conversational messages (deterministic, zero LLM cost).
        # The check is exact-match on the whole query (e.g. "hi", "thank you"),
        # so "thanks, what is FIM?" or "okay explain Wazuh" do NOT match and still
        # get RAG as normal. This saves ~250-400 RAG tokens for pure greetings.
        if is_conversational_no_rag(query):
            # Do not add RAG_CHAT for pure conversational messages; they will
            # fall through to GREETING/GENERAL_CHAT below.
            pass
        elif explicit_knowledge or pure_domain or entity_only:
            rag_features = list(dict.fromkeys(
                trigger_matched + domain_matched + content_ref_matched + catalog_matched +
                [e.value for e in entities.all() if e.type in ("CVE", "MITRE_TID")]
            ))
            candidate_intents.append(DetectedIntent(
                type=IntentType.RAG_CHAT,
                confidence=0.0,
                reason="Matched RAG keywords/domain terms or detected security entities",
                matched_features=rag_features,
            ))

        # 5. Tool chat
        tool_keywords = ["scan", "lookup", "check", "run", "trace", "resolve"]
        tool_matched = _matches_any(query_lower, tool_keywords)
        if tool_matched:
            candidate_intents.append(DetectedIntent(
                type=IntentType.TOOL_CHAT,
                confidence=0.0,
                reason="Matched tool action keywords",
                matched_features=tool_matched,
            ))

        # Lab mentor — fires when the user is asking for help/guidance with a
        # lab (not claiming a platform lab action, which is handled above).
        # Requires a help marker alongside "lab" so pure concept questions that
        # merely mention a lab remain on the knowledge/RAG path.
        if (_has_word(query_lower, "lab") or _has_word(query_lower, "labs")):
            if any(marker in query_lower for marker in _LAB_HELP_MARKERS):
                candidate_intents.append(DetectedIntent(
                    type=IntentType.LAB_ASSISTANT,
                    confidence=0.0,
                    reason="Matched lab help request.",
                    matched_features=["lab"],
                ))

        # 6. Greeting
        greeting_keywords = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"]
        if any(query_lower.strip().startswith(kw) for kw in greeting_keywords):
            candidate_intents.append(DetectedIntent(
                type=IntentType.GREETING,
                confidence=0.0,
                reason="Matched greeting prefix",
                matched_features=[],
            ))

        # 7. General chat fallback
        if not candidate_intents:
            candidate_intents.append(DetectedIntent(
                type=IntentType.GENERAL_CHAT,
                confidence=0.0,
                reason="No specific intent detected",
                matched_features=[],
            ))

        return candidate_intents
