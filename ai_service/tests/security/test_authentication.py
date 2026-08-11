import pytest
from app.security.authentication.providers import UsernamePasswordProvider, APIKeyProvider
from app.security.authentication.tokens import JWTTokenService
from app.security.authentication.sessions import InMemorySessionManager
from app.security.authentication.service import AuthenticationService

def test_username_password_provider():
    provider = UsernamePasswordProvider()
    res = provider.authenticate({"username": "admin", "password": "admin"})
    assert res["principal"] == "admin"
    assert "admin" in res["roles"]
    
    with pytest.raises(ValueError):
        provider.authenticate({"username": "admin", "password": "bad"})

def test_authentication_service():
    providers = {"basic": UsernamePasswordProvider(), "apikey": APIKeyProvider()}
    tokens = JWTTokenService(expiration_minutes=1)
    sessions = InMemorySessionManager()
    
    service = AuthenticationService(providers, tokens, sessions)
    
    token = service.login("basic", {"username": "user", "password": "user"})
    assert token.startswith("jwt.user")
    
    claims = service.validate_request(token)
    assert claims["principal"] == "user"
