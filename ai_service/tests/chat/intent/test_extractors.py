import pytest
from app.chat.intent.extractors.regex_extractor import RegexEntityExtractor

@pytest.mark.asyncio
async def test_regex_extractor():
    extractor = RegexEntityExtractor()
    
    # Test CVE
    res = await extractor.extract("search for CVE-2023-12345 and cve-2024-9999", {})
    cves = res.get("CVE")
    assert len(cves) == 2
    assert cves[0].value in ["CVE-2023-12345", "CVE-2024-9999"]
    
    # Test MITRE
    res = await extractor.extract("how does T1059.001 work?", {})
    assert res.has("MITRE_TID")
    assert res.get("MITRE_TID")[0].value == "T1059.001"
    
    # Test IP
    res = await extractor.extract("scan 192.168.1.1 please", {})
    assert res.has("IP_ADDRESS")
    assert res.get("IP_ADDRESS")[0].value == "192.168.1.1"
