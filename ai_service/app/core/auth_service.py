import logging
from abc import ABC, abstractmethod
from typing import Optional
from datetime import datetime, timezone
import httpx

from app.core.config import settings

logger = logging.getLogger("app.core.auth_service")

class AuthenticationProvider(ABC):
    """
    Abstraction for providing a valid authentication token.
    This allows the application layer to remain unaware of where the token comes from.
    """
    @abstractmethod
    async def get_token(self, provided_token: Optional[str] = None) -> Optional[str]:
        """
        Returns a valid authentication token.
        If a provided_token is given (e.g., from the frontend), it should be prioritized.
        If no token is given and demo mode is active, it may return a demo token.
        """
        pass

class DefaultAuthenticationProvider(AuthenticationProvider):
    """
    Standard provider that simply returns the provided token.
    Used in production.
    """
    async def get_token(self, provided_token: Optional[str] = None) -> Optional[str]:
        return provided_token

class DemoAuthenticationService(AuthenticationProvider):
    """
    Development-only provider that automatically authenticates as a configured Demo User
    against the Django backend to retrieve a real JWT. It caches the token to avoid
    hitting the login endpoint on every request.
    """
    def __init__(self):
        self._cached_token: Optional[str] = None
        self._token_expires_at: Optional[datetime] = None

    async def get_token(self, provided_token: Optional[str] = None) -> Optional[str]:
        # Rule 2: Never override a real authenticated user.
        # If a real token is provided (and not a dummy placeholder), use it directly.
        if provided_token and provided_token != "dummy_token":
            return provided_token

        # Rule 1: Demo Mode must remain development-only.
        if not settings.is_development or not settings.ENABLE_DEMO_MODE:
            return provided_token

        if not settings.DEMO_USER_EMAIL or not settings.DEMO_USER_PASSWORD:
            logger.warning("Demo mode enabled but DEMO_USER_EMAIL or DEMO_USER_PASSWORD is not set. Falling back to provided token.")
            return provided_token

        return await self._get_or_refresh_demo_token()

    async def _get_or_refresh_demo_token(self) -> Optional[str]:
        # Check if we have a valid cached token
        if self._cached_token and self._token_expires_at:
            # Refresh if it expires in less than 5 minutes
            if (self._token_expires_at - datetime.now(timezone.utc)).total_seconds() > 300:
                logger.debug("Using cached Demo User JWT.")
                return self._cached_token

        # Token is expired or missing. Fetch a new one from Django.
        logger.info(f"Authenticating Demo User ({settings.DEMO_USER_EMAIL}) against Django...")
        
        login_url = f"{settings.DJANGO_API_URL.rstrip('/')}/auth/login/"
        payload = {
            "email": settings.DEMO_USER_EMAIL,
            "password": settings.DEMO_USER_PASSWORD
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(login_url, json=payload, timeout=10.0)
                
                if response.status_code == 200:
                    data = response.json()
                    tokens = data.get("tokens", {})
                    access_token = tokens.get("access")
                    
                    if access_token:
                        self._cached_token = access_token
                        # We don't strictly need to parse the JWT to know when it expires,
                        # but parsing `exp` claim is more robust.
                        self._token_expires_at = self._extract_exp_from_jwt(access_token)
                        logger.info("Successfully retrieved and cached Demo User JWT.")
                        return access_token
                    else:
                        logger.error("Django login successful but no access token returned in 'tokens.access'.")
                else:
                    logger.error(f"Failed to authenticate Demo User. Django returned {response.status_code}: {response.text}")
                    
        except Exception as e:
            logger.error(f"Error communicating with Django during Demo Auth: {e}")

        # If we failed to get a demo token, clear cache just in case and return None
        self._cached_token = None
        self._token_expires_at = None
        return None

    def _extract_exp_from_jwt(self, token: str) -> Optional[datetime]:
        try:
            import jwt
            # We don't verify the signature here, just reading the exp claim to know when to refresh
            unverified_claims = jwt.decode(token, options={"verify_signature": False})
            exp = unverified_claims.get("exp")
            if exp:
                return datetime.fromtimestamp(exp, tz=timezone.utc)
        except Exception as e:
            logger.warning(f"Could not parse 'exp' from JWT: {e}")
            
        # Default to caching for 50 minutes if we can't parse it
        from datetime import timedelta
        return datetime.now(timezone.utc) + timedelta(minutes=50)

# Global instance for dependency injection
def get_auth_provider() -> AuthenticationProvider:
    if settings.is_development and settings.ENABLE_DEMO_MODE:
        if not hasattr(get_auth_provider, "_demo_instance"):
            get_auth_provider._demo_instance = DemoAuthenticationService()
        return get_auth_provider._demo_instance
    
    if not hasattr(get_auth_provider, "_default_instance"):
        get_auth_provider._default_instance = DefaultAuthenticationProvider()
    return get_auth_provider._default_instance
