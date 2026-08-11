from app.security.interfaces.i_secrets import ISecretVault, ISecretProvider
from app.security.secrets.cache import SecretCache
from app.agents.events.event_bus import agent_event_bus
from app.agents.events.agent_events import AgentEvent

class SecretAccessedEvent(AgentEvent):
    type: str = "SecretAccessed"
    secret_id: str

class SecretVault(ISecretVault):
    def __init__(self, provider: ISecretProvider, cache: SecretCache):
        self._provider = provider
        self._cache = cache

    def retrieve(self, secret_id: str) -> str:
        val = self._cache.get(secret_id)
        if val is None:
            val = self._provider.get_secret(secret_id)
            self._cache.put(secret_id, val)
            
        agent_event_bus.publish(SecretAccessedEvent(session_id="sys", secret_id=secret_id))
        return val

    def store(self, secret_id: str, value: str) -> None:
        self._provider.set_secret(secret_id, value)
        self._cache.invalidate(secret_id)
