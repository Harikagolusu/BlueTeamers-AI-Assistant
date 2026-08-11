from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class IAuthenticationProvider(ABC):
    @abstractmethod
    def authenticate(self, credentials: Dict[str, Any]) -> Dict[str, Any]: pass

class ITokenService(ABC):
    @abstractmethod
    def generate_token(self, principal: str, claims: Dict[str, Any]) -> str: pass
    @abstractmethod
    def validate_token(self, token: str) -> Dict[str, Any]: pass

class ISessionManager(ABC):
    @abstractmethod
    def create_session(self, principal: str) -> str: pass
    @abstractmethod
    def validate_session(self, session_id: str) -> bool: pass
    @abstractmethod
    def invalidate_session(self, session_id: str) -> None: pass

class IAuthenticationService(ABC):
    @abstractmethod
    def login(self, provider_id: str, credentials: Dict[str, Any]) -> str: pass
    @abstractmethod
    def logout(self, session_id: str) -> None: pass
    @abstractmethod
    def validate_request(self, token: str) -> Dict[str, Any]: pass
