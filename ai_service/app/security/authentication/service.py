from typing import Dict, Any
from app.security.interfaces.i_authentication import IAuthenticationService, IAuthenticationProvider, ITokenService, ISessionManager
from app.agents.events.event_bus import agent_event_bus
from app.agents.events.agent_events import AgentEvent

class UserAuthenticatedEvent(AgentEvent):
    type: str = "UserAuthenticated"
    principal: str
    auth_method: str

class AuthenticationFailedEvent(AgentEvent):
    type: str = "AuthenticationFailed"
    method: str
    error: str

class UserLoggedOutEvent(AgentEvent):
    type: str = "UserLoggedOut"
    principal: str

class AuthenticationService(IAuthenticationService):
    def __init__(
        self,
        providers: Dict[str, IAuthenticationProvider],
        token_service: ITokenService,
        session_manager: ISessionManager
    ):
        self._providers = providers
        self._token_service = token_service
        self._session_manager = session_manager

    def login(self, provider_id: str, credentials: Dict[str, Any]) -> str:
        provider = self._providers.get(provider_id)
        if not provider:
            raise ValueError(f"Unknown provider: {provider_id}")
            
        try:
            auth_data = provider.authenticate(credentials)
            principal = auth_data["principal"]
            
            token = self._token_service.generate_token(principal, auth_data)
            
            agent_event_bus.publish(UserAuthenticatedEvent(
                session_id="system",
                principal=principal,
                auth_method=provider_id
            ))
            
            return token
        except Exception as e:
            agent_event_bus.publish(AuthenticationFailedEvent(
                session_id="system",
                method=provider_id,
                error=str(e)
            ))
            raise

    def logout(self, session_id: str) -> None:
        # Simplistic mapping, mostly we'd decode session_id
        self._session_manager.invalidate_session(session_id)
        agent_event_bus.publish(UserLoggedOutEvent(
            session_id="system",
            principal="unknown_logout"
        ))

    def validate_request(self, token: str) -> Dict[str, Any]:
        return self._token_service.validate_token(token)
