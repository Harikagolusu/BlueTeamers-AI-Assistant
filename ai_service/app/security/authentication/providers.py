from typing import Dict, Any
from app.security.interfaces.i_authentication import IAuthenticationProvider

class UsernamePasswordProvider(IAuthenticationProvider):
    def authenticate(self, credentials: Dict[str, Any]) -> Dict[str, Any]:
        # Stub logic: In enterprise, verify against DB or LDAP with bcrypt/argon2
        username = credentials.get("username")
        password = credentials.get("password")
        if username == "admin" and password == "admin":
            return {"principal": username, "tenant": "default", "roles": ["admin"]}
        if username == "user" and password == "user":
            return {"principal": username, "tenant": "default", "roles": ["user"]}
        raise ValueError("Invalid credentials")

class APIKeyProvider(IAuthenticationProvider):
    def authenticate(self, credentials: Dict[str, Any]) -> Dict[str, Any]:
        api_key = credentials.get("api_key")
        if api_key == "secret-key":
            return {"principal": "service-account", "tenant": "default", "roles": ["service"]}
        raise ValueError("Invalid API Key")
