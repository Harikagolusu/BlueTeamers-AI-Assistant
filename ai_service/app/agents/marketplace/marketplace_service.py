from typing import List, Optional
from app.agents.interfaces.i_marketplace import IMarketplaceService, IMarketplaceProvider, IAgentLifecycleManager, IMarketplaceRepository
from app.agents.models.agent_package import AgentPackage

class MarketplaceService(IMarketplaceService):
    def __init__(
        self, 
        provider: IMarketplaceProvider,
        lifecycle_manager: IAgentLifecycleManager,
        repository: IMarketplaceRepository
    ):
        self._provider = provider
        self._lifecycle_manager = lifecycle_manager
        self._repository = repository

    def install_package(self, package_id: str, version: Optional[str] = None) -> None:
        package = self._provider.fetch_package(package_id, version)
        self._lifecycle_manager.install(package)

    def remove_package(self, package_id: str) -> None:
        self._lifecycle_manager.remove(package_id)

    def upgrade_package(self, package_id: str, version: str) -> None:
        package = self._provider.fetch_package(package_id, version)
        self._lifecycle_manager.update(package_id, package)

    def downgrade_package(self, package_id: str, version: str) -> None:
        package = self._provider.fetch_package(package_id, version)
        self._lifecycle_manager.update(package_id, package)

    def enable_package(self, package_id: str) -> None:
        self._lifecycle_manager.enable(package_id)

    def disable_package(self, package_id: str) -> None:
        self._lifecycle_manager.disable(package_id)

    def search_packages(self, query: str) -> List[AgentPackage]:
        return self._provider.search(query)

    def list_installed_packages(self) -> List[AgentPackage]:
        return self._repository.list_packages()
