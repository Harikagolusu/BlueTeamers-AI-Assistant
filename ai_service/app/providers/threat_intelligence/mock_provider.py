from typing import Dict, Any, List
from app.providers.threat_intelligence.base_provider import ThreatIntelligenceProvider

class MockThreatIntelligenceProvider(ThreatIntelligenceProvider):
    """
    Mock implementation using realistic cybersecurity examples based on public knowledge.
    """
    async def lookup_ioc(self, indicator: str) -> Dict[str, Any]:
        if indicator == "8.8.8.8":
            return {"value": indicator, "type": "ip", "confidence": 100, "malicious": False, "description": "Google Public DNS"}
        elif indicator == "192.168.1.10":
            return {"value": indicator, "type": "ip", "confidence": 100, "malicious": False, "description": "Private IP Address"}
        elif indicator == "44d88612fea8a8f36de82e1278abb02f":
            return {"value": indicator, "type": "hash", "confidence": 95, "malicious": True, "description": "Known Malicious MD5 Hash"}
        elif indicator == "example.com":
            return {"value": indicator, "type": "domain", "confidence": 100, "malicious": False, "description": "Example Domain"}
        elif indicator == "https://example.com/login":
            return {"value": indicator, "type": "url", "confidence": 100, "malicious": False, "description": "Example Login URL"}
        else:
            return {"value": indicator, "type": "unknown", "confidence": 0, "malicious": False, "description": "No intelligence available"}

    async def get_reputation(self, indicator: str) -> Dict[str, Any]:
        data = await self.lookup_ioc(indicator)
        if data["malicious"]:
            return {"risk_level": "HIGH", "confidence": data["confidence"], "summary": "Indicator is known malicious.", "recommended_action": "Block immediately."}
        elif data["type"] == "unknown":
            return {"risk_level": "UNKNOWN", "confidence": 0, "summary": "No intelligence available", "recommended_action": "Monitor."}
        else:
            return {"risk_level": "LOW", "confidence": data["confidence"], "summary": "Indicator is known benign.", "recommended_action": "Allow."}

    async def get_threat_actor(self, actor_name: str) -> Dict[str, Any]:
        name = actor_name.upper()
        if name == "APT29":
            return {"aliases": ["Cozy Bear", "Nobelium"], "campaigns": ["SolarWinds"], "mitre_techniques": ["T1078", "T1566"], "common_ttps": ["Phishing", "Valid Accounts"], "target_industries": ["Government", "Technology"], "geographic_attribution": "Russia"}
        elif name == "APT28":
            return {"aliases": ["Fancy Bear", "Sofacy"], "campaigns": ["DNC Hack"], "mitre_techniques": ["T1003", "T1059"], "common_ttps": ["Credential Dumping", "Command and Scripting Interpreter"], "target_industries": ["Government", "Military"], "geographic_attribution": "Russia"}
        elif name == "LAZARUS GROUP":
            return {"aliases": ["HIDDEN COBRA", "Zinc"], "campaigns": ["WannaCry", "Sony Pictures"], "mitre_techniques": ["T1566"], "common_ttps": ["Ransomware", "Spearphishing"], "target_industries": ["Finance", "Entertainment"], "geographic_attribution": "North Korea"}
        return {"error": "No intelligence available"}

    async def get_campaign(self, campaign_name: str) -> Dict[str, Any]:
        name = campaign_name.lower()
        if name == "solarwinds":
            return {"summary": "Supply chain attack compromising SolarWinds Orion.", "timeline": "2020", "associated_malware": ["Sunburst", "Teardrop"], "mitre_techniques": ["T1078", "T1195"], "threat_actors": ["APT29"], "affected_sectors": ["Government", "Technology"]}
        elif name == "emotet":
            return {"summary": "Banking Trojan that evolved into a botnet.", "timeline": "2014-Present", "associated_malware": ["TrickBot", "Ryuk"], "mitre_techniques": ["T1059", "T1566"], "threat_actors": ["Mummy Spider"], "affected_sectors": ["Various"]}
        elif name == "wannacry":
            return {"summary": "Global ransomware attack exploiting EternalBlue.", "timeline": "May 2017", "associated_malware": ["WannaCry"], "mitre_techniques": ["T1210"], "threat_actors": ["Lazarus Group"], "affected_sectors": ["Healthcare", "Various"]}
        return {"error": "No intelligence available"}

    async def correlate_indicators(self, indicators: List[str]) -> Dict[str, Any]:
        results = []
        has_malicious = False
        for ind in indicators:
            data = await self.lookup_ioc(ind)
            results.append(data)
            if data.get("malicious"):
                has_malicious = True
        
        if has_malicious:
            return {"relationships": "Found mixed or malicious indicators.", "confidence": 85, "possible_campaign": "Unknown", "possible_actor": "Unknown", "recommendations": "Investigate the malicious indicators."}
        return {"relationships": "No clear malicious relationships found.", "confidence": 50, "possible_campaign": "None", "possible_actor": "None", "recommendations": "Continue monitoring."}

    async def map_to_mitre(self, entity: str) -> List[Dict[str, Any]]:
        entity = entity.upper()
        mapping = {
            "T1003": {"tactic": "Credential Access", "technique_id": "T1003", "technique_name": "OS Credential Dumping", "description": "Dumping credentials from memory."},
            "T1059": {"tactic": "Execution", "technique_id": "T1059", "technique_name": "Command and Scripting Interpreter", "description": "Executing commands via scripts."},
            "T1566": {"tactic": "Initial Access", "technique_id": "T1566", "technique_name": "Phishing", "description": "Sending spearphishing emails."},
            "T1078": {"tactic": "Defense Evasion", "technique_id": "T1078", "technique_name": "Valid Accounts", "description": "Using compromised valid accounts."}
        }
        if entity in mapping:
            return [mapping[entity]]
        
        actor = await self.get_threat_actor(entity)
        if "error" not in actor:
            res = []
            for tech in actor.get("mitre_techniques", []):
                if tech in mapping:
                    res.append(mapping[tech])
            return res
            
        campaign = await self.get_campaign(entity)
        if "error" not in campaign:
            res = []
            for tech in campaign.get("mitre_techniques", []):
                if tech in mapping:
                    res.append(mapping[tech])
            return res
            
        return []
