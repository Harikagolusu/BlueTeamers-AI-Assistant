"""Tests for Sprint 4 smart conversation titles (Feature 10)."""
from app.conversations.title import generate_title


def test_windows_event_log_title():
    assert generate_title("Analyze event id 4625 from the windows event log") == "Windows Event Log Analysis"


def test_wazuh_title():
    assert generate_title("Investigate this Wazuh alert") == "Wazuh Rule Investigation"


def test_ioc_title():
    assert generate_title("Check this indicator of compromise for me") == "IOC Analysis"


def test_mitre_title():
    assert generate_title("Map this to MITRE ATT&CK") == "MITRE ATT&CK"


def test_threat_hunting_title():
    assert generate_title("Help me with a threat hunting exercise") == "Threat Hunting"


def test_resume_title():
    assert generate_title("Can you review my resume for a SOC role?") == "Resume Review"


def test_sigma_title():
    assert generate_title("Write a sigma detection rule") == "Sigma Rule Analysis"


def test_yara_title():
    assert generate_title("Create a YARA rule") == "YARA Rule Analysis"


def test_splunk_title():
    assert generate_title("Build a Splunk search") == "Splunk Investigation"


def test_kql_title():
    assert generate_title("Query this in KQL") == "KQL Investigation"


def test_soc_operations_title():
    assert generate_title("How do I triage alerts as a security operations analyst?") == "SOC Operations"


def test_generic_titles_still_work():
    title = generate_title("Can you explain how DNS resolution works?")
    assert "dns" in title.lower() or "Dns" in title
