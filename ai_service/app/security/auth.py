import logging
import os
from typing import Dict, Any, List, Optional

import jwt
from fastapi import HTTPException, status

from app.core.config import settings
from app.models.authenticated_user import AuthenticatedUser

logger = logging.getLogger("app.security")


def _load_public_key() -> Optional[str]:
    """Read the Django RS256 public key PEM if configured and present."""
    path = settings.JWT_PUBLIC_KEY_PATH
    if path and os.path.exists(path):
        try:
            with open(path, "r") as fh:
                key = fh.read().strip()
            if key:
                return key
        except Exception as e:
            logger.warning("Failed to read JWT public key at %s: %s", path, e)
    return None


_RS256_PUBLIC_KEY = _load_public_key()


class JWTValidator:
    """
    Utility class to handle JWT decoding and validation securely.
    When an RS256 public key is configured, only asymmetric RS256 tokens
    (issued by Django) are accepted and the signature is verified with the
    public key. Otherwise it falls back to the legacy symmetric (HS256) secret.
    """
    def __init__(
        self,
        secret: str,
        algorithms: Optional[List[str]] = None,
    ):
        self.secret = secret
        if algorithms is None:
            self.algorithms = ["RS256"] if _RS256_PUBLIC_KEY else ["HS256", "RS256"]
        else:
            self.algorithms = algorithms

    def decode_token(self, token: str) -> Dict[str, Any]:
        """
        Decodes the JWT token and verifies the signature and expiration.
        """
        try:
            payload = jwt.decode(
                token,
                self.secret,
                algorithms=self.algorithms,
                options={"verify_exp": True}
            )
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Authentication failed: Token has expired.")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.InvalidTokenError as e:
            logger.warning("Authentication failed: Invalid token signature or format.")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except Exception as e:
            logger.warning("Authentication failed: Unexpected error during decoding.")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication failed",
                headers={"WWW-Authenticate": "Bearer"},
            )

    def get_user_from_payload(self, payload: Dict[str, Any]) -> AuthenticatedUser:
        """
        Extracts required claims from the payload to build the AuthenticatedUser model.
        """
        user_id = payload.get("user_id")
        email = payload.get("email")

        if not user_id or not email:
            logger.warning("Authentication failed: Missing required claims (user_id or email).")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token claims",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return AuthenticatedUser(user_id=user_id, email=email)

# Singleton validator instance. When an RS256 public key is configured it
# verifies Django-issued tokens with that key; otherwise it falls back to the
# symmetric JWT_SECRET (legacy/dev mode).
jwt_validator = JWTValidator(secret=_RS256_PUBLIC_KEY or settings.JWT_SECRET)


def resolve_user_identity(token: Optional[str]) -> tuple:
    """Return a stable (user_id, email) pair from a validated JWT.

    ``user_id`` is the canonical identity: it is always present in SimpleJWT
    access tokens and — critically — stable across token refresh. The ``email``
    claim is only set on the initial access token, so it must never be used as
    the primary key. Returns (None, None) for missing/invalid tokens.
    """
    if not token:
        return None, None
    try:
        payload = jwt_validator.decode_token(token)
    except Exception:
        return None, None
    user_id = payload.get("user_id")
    email = payload.get("email")
    if user_id:
        return str(user_id), str(email or "")
    if email:
        return str(email), str(email)
    return None, None
