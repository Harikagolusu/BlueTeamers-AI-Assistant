from typing import List, Dict, Optional
import threading
from app.agents.interfaces.i_marketplace import IMarketplaceRepository
from app.agents.models.agent_package import AgentPackage

class MarketplaceRepository(IMarketplaceRepository):
    def __init__(self):
        self._packages: Dict[str, AgentPackage] = {}
        self._enabled_state: Dict[str, bool] = {}
        self._lock = threading.RLock()

    def save_package(self, package: AgentPackage) -> None:
        with self._lock:
            self._packages[package.manifest.id] = package
            self._enabled_state[package.manifest.id] = True

    def remove_package(self, package_id: str) -> None:
        with self._lock:
            if package_id in self._packages:
                del self._packages[package_id]
            if package_id in self._enabled_state:
                del self._enabled_state[package_id]

    def get_package(self, package_id: str) -> Optional[AgentPackage]:
        with self._lock:
            return self._packages.get(package_id)

    def list_packages(self) -> List[AgentPackage]:
        with self._lock:
            return list(self._packages.values())

    def set_enabled_state(self, package_id: str, enabled: bool) -> None:
        with self._lock:
            if package_id in self._packages:
                self._enabled_state[package_id] = enabled

    def is_enabled(self, package_id: str) -> bool:
        with self._lock:
            return self._enabled_state.get(package_id, False)
