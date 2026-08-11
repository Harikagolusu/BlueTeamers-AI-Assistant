import pytest
from app.agents.models.agent_package import AgentPackage, AgentManifest
from app.agents.models.metadata import PackageMetadata
from app.agents.marketplace.repository import MarketplaceRepository
from app.agents.marketplace.providers.local_provider import LocalMarketplaceProvider
from app.agents.marketplace.lifecycle_manager import AgentLifecycleManager
from app.agents.marketplace.installer import AgentInstaller
from app.agents.marketplace.updater import AgentUpdater
from app.agents.marketplace.remover import AgentRemover
from app.agents.packages.package_installer import PackageInstaller
from app.agents.marketplace.marketplace_service import MarketplaceService

def test_marketplace_lifecycle():
    repository = MarketplaceRepository()
    package_installer = PackageInstaller()
    
    installer = AgentInstaller(repository, package_installer)
    updater = AgentUpdater(repository, package_installer)
    remover = AgentRemover(repository, package_installer)
    
    lifecycle = AgentLifecycleManager(installer, updater, remover, repository)
    
    # Mock Provider
    class MockProvider(LocalMarketplaceProvider):
        def fetch_package(self, package_id: str, version=None):
            return AgentPackage(
                manifest=AgentManifest(id=package_id, name="Test", version="1.0"),
                metadata=PackageMetadata(author="Test Author")
            )
            
    provider = MockProvider("/tmp")
    service = MarketplaceService(provider, lifecycle, repository)
    
    # Install
    service.install_package("test-package")
    assert len(service.list_installed_packages()) == 1
    
    # Disable/Enable
    service.disable_package("test-package")
    assert not repository.is_enabled("test-package")
    service.enable_package("test-package")
    assert repository.is_enabled("test-package")
    
    # Remove
    service.remove_package("test-package")
    assert len(service.list_installed_packages()) == 0
