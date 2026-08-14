import pytest
from app.security.authentication.providers import UsernamePasswordProvider, APIKeyProvider
from app.security.authentication.tokens import JWTTokenService
from app.security.authentication.sessions import InMemorySessionManager
from app.security.authentication.service import AuthenticationService

def test_username_password_provider():
    provider = UsernamePasswordProvider()
    # The provider is a fail-safe stub: it must NEVER accept hardcoded
    # credentials (the old admin/user demo accounts were removed).
    with pytest.raises(NotImplementedError):
        provider.authenticate({"username": "admin", "password": "admin"})
    with pytest.raises(NotImplementedError):
        provider.authenticate({"username": "admin", "password": "bad"})

def test_apikey_provider_is_fail_safe():
    provider = APIKeyProvider()
    with pytest.raises(NotImplementedError):
        provider.authenticate({"api_key": "secret-key"})

def test_authentication_service():
    providers = {"basic": UsernamePasswordProvider(), "apikey": APIKeyProvider()}
    tokens = JWTTokenService(expiration_minutes=1)
    sessions = InMemorySessionManager()

    service = AuthenticationService(providers, tokens, sessions)

    with pytest.raises(NotImplementedError):
        service.login("basic", {"username": "user", "password": "user"})
