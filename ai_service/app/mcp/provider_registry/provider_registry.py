from typing import Dict, List, Optional
from app.mcp.interfaces.i_provider_registry import IProviderRegistry
from app.mcp.interfaces.i_tool_provider import IToolProvider

class ProviderRegistry(IProviderRegistry):
    def __init__(self):
        self._providers: Dict[str, IToolProvider] = {}

    def register(self, provider: IToolProvider) -> None:
        self._providers[provider.provider_id] = provider

    def resolve(self, provider_id: str) -> Optional[IToolProvider]:
        return self._providers.get(provider_id)

    def remove(self, provider_id: str) -> None:
        if provider_id in self._providers:
            del self._providers[provider_id]

    def list_providers(self) -> List[IToolProvider]:
        return list(self._providers.values())
