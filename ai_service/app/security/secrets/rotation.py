from app.security.interfaces.i_secrets import ISecretRotationManager, ISecretVault
from app.security.secrets.cache import SecretCache
from app.agents.events.event_bus import agent_event_bus
from app.agents.events.agent_events import AgentEvent

class SecretRotatedEvent(AgentEvent):
    type: str = "SecretRotated"
    secret_id: str

class SecretRotationManager(ISecretRotationManager):
    def __init__(self, vault: ISecretVault, cache: SecretCache):
        self._vault = vault
        self._cache = cache
        self._schedules = {}

    def rotate_secret(self, secret_id: str) -> None:
        # In a real system, this would call out to a provider to regenerate the credential
        # Here we just invalidate the cache and simulate rotation
        self._cache.invalidate(secret_id)
        # Assuming provider rotated it out of band for the stub
        agent_event_bus.publish(SecretRotatedEvent(session_id="sys", secret_id=secret_id))

    def schedule_rotation(self, secret_id: str, cron: str) -> None:
        self._schedules[secret_id] = cron
        # Real system integrates with apscheduler
