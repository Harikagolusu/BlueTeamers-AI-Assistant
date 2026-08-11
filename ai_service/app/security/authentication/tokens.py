import uuid
from datetime import datetime, timedelta, timezone
from typing import Dict, Any
from app.security.interfaces.i_authentication import ITokenService

class JWTTokenService(ITokenService):
    def __init__(self, secret: str = "super_secret_stub", expiration_minutes: int = 60):
        self._secret = secret
        self._expiration = expiration_minutes
        self._store = {} # Stub for revocation checks

    def generate_token(self, principal: str, claims: Dict[str, Any]) -> str:
        # Stub: Generate a fake JWT string
        # Real impl uses PyJWT
        token = f"jwt.{principal}.{uuid.uuid4()}"
        self._store[token] = {
            "principal": principal,
            "claims": claims,
            "expires": datetime.now(timezone.utc) + timedelta(minutes=self._expiration)
        }
        return token

    def validate_token(self, token: str) -> Dict[str, Any]:
        if token not in self._store:
            raise ValueError("Invalid token")
        
        data = self._store[token]
        if datetime.now(timezone.utc) > data["expires"]:
            del self._store[token]
            raise ValueError("Token expired")
            
        return {"principal": data["principal"], "claims": data["claims"]}
