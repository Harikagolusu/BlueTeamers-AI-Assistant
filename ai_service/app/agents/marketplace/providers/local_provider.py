import os
import yaml
from typing import List, Optional
from app.agents.interfaces.i_marketplace import IMarketplaceProvider
from app.agents.models.agent_package import AgentPackage, AgentManifest
from app.agents.models.metadata import PackageMetadata

class LocalMarketplaceProvider(IMarketplaceProvider):
    def __init__(self, packages_dir: str):
        self._packages_dir = packages_dir

    def fetch_package(self, package_id: str, version: Optional[str] = None) -> AgentPackage:
        # Stub: Load from local path
        path = os.path.join(self._packages_dir, package_id)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Package {package_id} not found in local provider")
            
        # In reality this parses all manifests, metadata, etc.
        manifest = AgentManifest(
            id=package_id,
            name=package_id.replace('-', ' ').title(),
            version=version or "1.0.0"
        )
        metadata = PackageMetadata(author="Local Provider")
        return AgentPackage(manifest=manifest, metadata=metadata)

    def search(self, query: str) -> List[AgentPackage]:
        # Stub: Scan local packages dir
        return []
