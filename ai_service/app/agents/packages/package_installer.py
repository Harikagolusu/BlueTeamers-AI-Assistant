from app.agents.interfaces.i_packages import IPackageInstaller
from app.agents.models.agent_package import AgentPackage
from app.agents.events.event_bus import agent_event_bus
from app.agents.events.agent_events import AgentEvent

class PackageInstalledEvent(AgentEvent):
    type: str = "PackageInstalled"
    package_id: str
    version: str

class PackageRemovedEvent(AgentEvent):
    type: str = "PackageRemoved"
    package_id: str

class PackageInstaller(IPackageInstaller):
    def install_package_contents(self, package: AgentPackage) -> None:
        # Stub: Extract files, register dependencies, setup paths
        agent_event_bus.publish(PackageInstalledEvent(
            session_id="system",
            package_id=package.manifest.id,
            version=package.manifest.version
        ))

    def uninstall_package_contents(self, package_id: str) -> None:
        # Stub: Remove files and cleanup
        agent_event_bus.publish(PackageRemovedEvent(
            session_id="system",
            package_id=package_id
        ))
