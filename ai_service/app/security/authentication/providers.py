from typing import Dict, Any
from app.security.interfaces.i_authentication import IAuthenticationProvider

class UsernamePasswordProvider(IAuthenticationProvider):
    """Placeholder auth provider.

    NOT wired into any route. Intended to be replaced by a real credential
    store (DB/LDAP) with bcrypt/argon2 verification before use. The previous
    hardcoded ``admin``/``user`` credentials were removed: never ship static
    credentials in code.
    """
    def authenticate(self, credentials: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError(
            "UsernamePasswordProvider is a stub and must be backed by a real "
            "credential store before it can be used."
        )

class APIKeyProvider(IAuthenticationProvider):
    """Placeholder API-key auth provider.

    Not wired into any route. The previous hardcoded ``secret-key`` was removed;
    implement real key verification against an env-configured key or database.
    """
    def authenticate(self, credentials: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError(
            "APIKeyProvider is a stub and must be backed by a real key store "
            "before it can be used."
        )
