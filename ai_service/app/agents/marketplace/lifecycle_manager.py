from app.agents.interfaces.i_marketplace import IAgentLifecycleManager, IMarketplaceRepository
from app.agents.models.agent_package import AgentPackage
from app.agents.marketplace.installer import AgentInstaller
from app.agents.marketplace.updater import AgentUpdater
from app.agents.marketplace.remover import AgentRemover

class AgentLifecycleManager(IAgentLifecycleManager):
    def __init__(
        self, 
        installer: AgentInstaller,
        updater: AgentUpdater,
        remover: AgentRemover,
        repository: IMarketplaceRepository
    ):
        self._installer = installer
        self._updater = updater
        self._remover = remover
        self._repository = repository

    def install(self, package: AgentPackage) -> None:
        self._installer.install(package)

    def remove(self, package_id: str) -> None:
        self._remover.remove(package_id)

    def update(self, package_id: str, new_package: AgentPackage) -> None:
        self._updater.update(package_id, new_package)

    def enable(self, package_id: str) -> None:
        self._repository.set_enabled_state(package_id, True)

    def disable(self, package_id: str) -> None:
        self._repository.set_enabled_state(package_id, False)

    def restart(self, package_id: str) -> None:
        self.disable(package_id)
        self.enable(package_id)

    def reload(self, package_id: str) -> None:
        self.restart(package_id)
