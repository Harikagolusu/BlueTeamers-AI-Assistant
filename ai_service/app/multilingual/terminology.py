"""Cybersecurity terminology that is ALWAYS preserved in English.

Whatever language the assistant responds in, these security terms stay in
English (or their industry-conventional form) so that translations never lose
meaning, break log/file references, or confuse training material. The list is
injected into the language instruction block of the system prompt.
"""
from typing import Tuple

# Core terms, acronyms, and artefact types that must never be translated.
PRESERVED_TERMS: Tuple[str, ...] = (
    # Core security operations
    "SIEM", "SOC", "IDS", "IPS", "EDR", "NDR", "XDR", "UEBA", "SOAR", "NGFW",
    "firewall", "honeypot", "sandbox", "malware", "ransomware", "phishing",
    "spoofing", "spear-phishing", "zero-day", "exploit", "payload", "botnet",
    "APT", "threat actor", "threat hunting", "incident response",
    "log", "alert", "ticket", "false positive", "false negative", "SIEM rule",
    "detection rule", "detection engineering", "rule tuning",
    "threat intelligence", "intel", "IOC", "TTP", "TTPs", "ATT&CK", "MITRE",
    "MITRE ATT&CK", "MITM", "DDoS", "DoS", "brute force", "credential stuffing", "C2",
    "beaconing", "lateral movement", "privilege escalation", "persistence",
    "defense evasion", "exfiltration", "data exfiltration", "DLL injection",
    "process injection", "living off the land", "LOLBins", "YARA", "Sigma",
    # Formats / artefacts
    "hash", "MD5", "SHA1", "SHA-256", "SHA256", "file", "process", "registry",
    "event", "event ID", "Windows Event Log", "Sysmon", "OSquery", "AUDITD",
    "auditd", "journald", "journalctl", "PCAP", "NetFlow", "Suricata", "Zeek",
    "Snort", "Wazuh", "Splunk", "Elastic", "ELK", "QRadar", "ArcSight",
    # Standards / frameworks / CVEs
    "CVE", "CVSS", "NIST", "ISO 27001", "PCI-DSS", "GDPR", "SOC 2",
    "GDPR/DPA", "EWS", "AIS", "NATO", "Zero Trust", "ZTA", "CSIRT", "CERT",
)
_TERMS_JOINED = ", ".join(PRESERVED_TERMS)


def preserved_terms_text() -> str:
    """One-line, human-readable list of terms that stay in English."""
    return _TERMS_JOINED