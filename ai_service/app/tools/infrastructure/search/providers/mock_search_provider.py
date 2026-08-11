from datetime import datetime, timezone
from typing import List, Dict, Any
from app.tools.infrastructure.search.interfaces.i_search_provider import ISearchProvider
from app.tools.infrastructure.providers.models import ProviderHealth, ProviderStatus

class MockSearchProvider(ISearchProvider):
    async def search(self, query: str, limit: int = 10, **kwargs) -> List[Dict[str, Any]]:
        return [
            {"id": "doc_1", "title": "Mock Document 1", "content": f"Result for {query}", "score": 0.99, "source": "mock", "metadata": {}},
            {"id": "doc_2", "title": "Mock Document 2", "content": "Another result", "score": 0.85, "source": "mock", "metadata": {}}
        ][:limit]
        
    async def health_check(self) -> ProviderHealth:
        return ProviderHealth(
            status=ProviderStatus.CONNECTED,
            latency_ms=5.0,
            version="1.0-mock",
            provider_name="MockSearchProvider",
            last_checked=datetime.now(timezone.utc)
        )
