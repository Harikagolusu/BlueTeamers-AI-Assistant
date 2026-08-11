"""Cyber topic registry used by the adaptive learning engine.

Covers the 13 Sprint-4 knowledge domains. Each topic carries a keyword lexicon
used to detect which domain the current question belongs to, plus an inherent
difficulty used to calibrate the recommended explanation depth.

Detection is score-based: a topic "wins" when it has the most keyword matches
in the query (recent conversation lines are also scanned so follow-ups like
"explain this further" keep their context topic).
"""
from dataclasses import dataclass
import re
from typing import Iterable, List, Optional, Sequence, Tuple

DIFFICULTY_FOUNDATIONAL = 1
DIFFICULTY_INTERMEDIATE = 3
DIFFICULTY_ADVANCED = 4


def _name_match(name: str, text: str) -> bool:
    """True when the topic's proper name appears as a word in the text.

    Used as a tie-breaker: "wazuh" (proper noun) should beat "triage" (generic)
    when both match a query like "Wazuh alert triage".
    """
    if not name or not text:
        return False
    return re.search(rf"\b{re.escape(name.lower())}\b", text.lower()) is not None


@dataclass(frozen=True)
class CyberTopic:
    key: str
    name: str
    keywords: Tuple[str, ...]
    difficulty: int

    def score(self, text: str) -> int:
        lowered = text.lower()
        return sum(1 for kw in self.keywords if kw in lowered)


TOPICS: List[CyberTopic] = [
    CyberTopic(
        "windows_security",
        "Windows Security",
        (
            "windows event", "event id", "windows security", "windows defender",
            "lsass", "windows logon", "windows auditing", "powershell log",
            "windows firewall", "event log", "scheduled task", "registry",
            "wmi", "sysmon", "amcache", "prefetch", "shimcache",
        ),
        DIFFICULTY_INTERMEDIATE,
    ),
    CyberTopic(
        "linux_security",
        "Linux Security",
        (
            "linux", "linux logs", "syslog", "auth.log", "bash history",
            "shell history", "systemd", "rsyslog", "journalctl", "ssh log",
            "var/log", "linux audit", "selinux", "cron log", "unix",
        ),
        DIFFICULTY_INTERMEDIATE,
    ),
    CyberTopic(
        "networking",
        "Networking",
        (
            "tcp", "udp", "dns", "subnet", "pcap", "tcpdump", "wireshark",
            "port scan", "netflow", "osi model", "network traffic", "http",
            "https", "ids", "ips", "routing", "packet capture",
        ),
        DIFFICULTY_INTERMEDIATE,
    ),
    CyberTopic(
        "soc_operations",
        "SOC Operations",
        (
            "soc", "security operations", "triage", "soc analyst", "shift",
            "ticket", "escalation", "runbook", "playbook", "soar",
            "security operation center", "alert triage", "soc team",
            "detection and response", "security analyst",
        ),
        DIFFICULTY_FOUNDATIONAL + 1,
    ),
    CyberTopic(
        "threat_hunting",
        "Threat Hunting",
        (
            "threat hunt", "threat hunting", "hunting hypothesis", "beaconing",
            "living off the land", "lotl", "ioc hunt", "hunting query",
            "adversary simulation", "hunt", "beacon detection", "hunting",
        ),
        DIFFICULTY_ADVANCED,
    ),
    CyberTopic(
        "incident_response",
        "Incident Response",
        (
            "incident response", "containment", "eradication", "recovery",
            "forensics", "chain of custody", "root cause", "blueteam exercise",
            "incident handling", "evidence collection", "aftermath", "ir plan",
        ),
        DIFFICULTY_INTERMEDIATE,
    ),
    CyberTopic(
        "wazuh",
        "Wazuh",
        (
            "wazuh", "ossec", "wazuh manager", "wazuh agent", "active response",
            "wazuh api", "wazuh groups", "wazuh decoders", "file integrity monitoring",
            "fim", "wazuh ruleset", "wazuh alerts", "agents list",
        ),
        DIFFICULTY_INTERMEDIATE,
    ),
    CyberTopic(
        "mitre",
        "MITRE ATT&CK",
        (
            "mitre", "attack", "t1059", "ttps", "tactic", "technique",
            "sub-technique", "kill chain", "mitre framework", "tactic id",
            "technique id", "privilege escalation", "lateral movement",
            "persistence mechanism", "defense evasion",
        ),
        DIFFICULTY_ADVANCED,
    ),
    CyberTopic(
        "sigma",
        "Sigma",
        (
            "sigma rule", "sigma detection", "logsource", "sigma yaml",
            "sigma backend", "sigma rule", "detection rule", "rule yaml",
            "sigma converter", "sigma specification",
        ),
        DIFFICULTY_ADVANCED,
    ),
    CyberTopic(
        "yara",
        "YARA",
        (
            "yara", "yara rule", "malware signature", "yara scan", "yara strings",
            "pe header", "malware detection", "signature rule", "yara match",
            "malware rule",
        ),
        DIFFICULTY_ADVANCED,
    ),
    CyberTopic(
        "cloud_security",
        "Cloud Security",
        (
            "cloud security", "aws", "azure", "gcp", "s3", "iam", "cloudtrail",
            "cloudwatch", "lambda", "eks", "ec2", "guard duty", "security hub",
            "azure ad", "cloud identity", "cloud logging",
        ),
        DIFFICULTY_INTERMEDIATE,
    ),
    CyberTopic(
        "splunk",
        "Splunk",
        (
            "splunk", "spl", "search head", "splunk query", "sourcetype",
            "splunk dashboard", "enterprise security", "splunk es", "index",
            "splunk search",
        ),
        DIFFICULTY_INTERMEDIATE,
    ),
    CyberTopic(
        "kql",
        "KQL",
        (
            "kql", "kusto", "azure sentinel", "sentinel query", "kusto query",
            "let statement", "sentinel", "kql query", "kusto query language",
        ),
        DIFFICULTY_INTERMEDIATE,
    ),
]

_TOPIC_BY_KEY = {t.key: t for t in TOPICS}


def topic_by_key(key: str) -> Optional[CyberTopic]:
    return _TOPIC_BY_KEY.get(key)


def detect_topics(texts: Sequence[str], max_results: int = 2) -> List[str]:
    """Return the topic keys (most matched first) across the given texts.

    At least one keyword match is required; empty input yields [].
    """
    if not texts:
        return []
    scores = {t.key: 0 for t in TOPICS}
    for text in texts:
        if not text:
            continue
        for topic in TOPICS:
            match = topic.score(text)
            if match == 0 and not _name_match(topic.name, text):
                continue
            # Proper-name matches weigh more than generic vocabulary.
            scores[topic.key] += match + (3 if _name_match(topic.name, text) else 0)
    ranked = sorted((k for k, v in scores.items() if v > 0), key=lambda k: scores[k], reverse=True)
    return ranked[:max_results]
