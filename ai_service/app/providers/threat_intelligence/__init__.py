from app.providers.threat_intelligence.base_provider import ThreatIntelligenceProvider
from app.providers.threat_intelligence.mock_provider import MockThreatIntelligenceProvider

# Singleton instance for tools to use by default.
# In a real DI framework, this would be injected.
provider_instance: ThreatIntelligenceProvider = MockThreatIntelligenceProvider()

__all__ = ["ThreatIntelligenceProvider", "MockThreatIntelligenceProvider", "provider_instance"]
