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

# Production must fail fast rather than silently running without a verify key:
# every request would be rejected (RS256-only) anyway, so surfacing the
# misconfiguration at startup beats discovering it after deploy.
if settings.is_production and not _RS256_PUBLIC_KEY:
    raise RuntimeError(
        "Production requires a readable JWT_PUBLIC_KEY_PATH. Set it to the "
        "Django RS256 public key and restart. Refusing to start without it."
    )


class JWTValidator:
    """
    Utility class to handle JWT decoding and validation securely.

    When an RS256 public key is configured, only asymmetric RS256 tokens
    (issued by Django) are accepted and the signature is verified with the
    public key.

    If no public key is readable, behaviour is mode-dependent:
      - Development: falls back to the legacy symmetric (HS256) secret so
        local tooling keeps working.
      - Production: FAILS CLOSED — only RS256 is accepted, so any request whose
        token cannot be verified with the configured public key is rejected.
        A deployment must provide a readable JWT_PUBLIC_KEY_PATH.
    """
    def __init__(
        self,
        secret: str,
        algorithms: Optional[List[str]] = None,
    ):
        self.secret = secret
        if algorithms is None:
            if _RS256_PUBLIC_KEY:
                self.algorithms = ["RS256"]
            elif settings.is_development:
                self.algorithms = ["HS256", "RS256"]
            else:
                # No trusted key in production: reject HS256 wholesale rather
                # than trusting a static secret -- avoids algorithm-confusion
                # and keeps invalid tokens from being accepted.
                self.algorithms = ["RS256"]
        else:
            self.algorithms = algorithms

    def decode_token(self, token: str) -> Dict[str, Any]:
        """
        Decodes the JWT token and verifies the signature, expiration, not-before
        and (when configured) issuer/audience claims.
        """
        try:
            decode_options: Dict[str, Any] = {
                "verify_exp": True,
                "verify_nbf": True,
                "verify_iat": True,
                # PyJWT raises InvalidAudienceError whenever a token carries an
                # ``aud`` claim without an explicit ``audience`` arg. Django
                # stamps aud/iss on every token, so only enforce those claims
                # when an issuer/audience is actually configured.
                "verify_aud": bool(settings.JWT_AUDIENCE),
                "verify_iss": bool(settings.JWT_ISSUER),
                "require": ["exp", "iat"],
            }
            verify_kwargs: Dict[str, Any] = {}
            if settings.JWT_ISSUER:
                verify_kwargs["issuer"] = settings.JWT_ISSUER
                decode_options["require"].append("iss")
            if settings.JWT_AUDIENCE:
                verify_kwargs["audience"] = settings.JWT_AUDIENCE
                decode_options["require"].append("aud")
            payload = jwt.decode(
                token,
                self.secret,
                algorithms=self.algorithms,
                options=decode_options,
                **verify_kwargs,
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
