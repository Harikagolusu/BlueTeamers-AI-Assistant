"""Tests for the adaptive topic registry (Sprint 4 feature 2)."""
from app.adaptive.topics import detect_topics


def test_detect_windows_event_log():
    assert detect_topics(["What does Event ID 4625 mean in windows event log?"])[0] == "windows_security"


def test_detect_wazuh():
    assert detect_topics(["How do I add a Wazuh agent to the manager?"])[0] == "wazuh"


def test_detect_mitre():
    assert detect_topics(["Explain MITRE ATT&CK T1059"])[0] == "mitre"


def test_detect_sigma():
    assert detect_topics(["Write a sigma rule for process creation"])[0] == "sigma"


def test_detect_yara():
    assert detect_topics(["Build a YARA rule for this malware sample"])[0] == "yara"


def test_detect_kql():
    assert detect_topics(["Write a KQL query in Azure Sentinel"])[0] == "kql"


def test_detect_splunk():
    assert detect_topics(["Splunk query for failed logons"])[0] == "splunk"


def test_detect_threat_hunting():
    assert detect_topics(["I want to start a threat hunting hypothesis"])[0] == "threat_hunting"


def test_detect_linux():
    assert detect_topics(["How do I read auth.log on Linux?"])[0] == "linux_security"


def test_detect_cloud():
    assert detect_topics(["AWS CloudTrail logs for cloud security"])[0] == "cloud_security"


def test_no_topic_for_greeting():
    assert detect_topics(["hello there"]) == []


def test_followup_keeps_context_topic():
    texts = [
        "Explain the Wazuh manager architecture",
        "What about the agents list?",
    ]
    assert detect_topics(texts)[0] == "wazuh"


def test_primary_is_most_matched():
    assert detect_topics(["wazuh wazuh and more wazuh, also a sigma sigma"])[0] == "wazuh"


def test_proper_name_beats_generic_vocab():
    assert detect_topics(["Explain Wazuh alert triage"])[0] == "wazuh"
    assert detect_topics(["How do I triage alerts?"])[0] == "soc_operations"
