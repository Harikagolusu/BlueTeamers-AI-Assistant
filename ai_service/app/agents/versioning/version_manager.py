from app.agents.interfaces.i_versioning import IVersionManager

class VersionManager(IVersionManager):
    def get_latest_version(self, component_id: str) -> str:
        # In a real implementation this would query the marketplace repository
        # For now, stub returning a fake latest version
        return "1.0.0"

    def is_update_available(self, component_id: str, current_version: str) -> bool:
        latest = self.get_latest_version(component_id)
        # Assuming semver string compare
        return latest > current_version
