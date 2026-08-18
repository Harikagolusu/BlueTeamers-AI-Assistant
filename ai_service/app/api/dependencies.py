import logging
import secrets
from typing import Optional

from fastapi import Depends, HTTPException, Request, Header, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.security.auth import jwt_validator
from app.models.authenticated_user import AuthenticatedUser

logger = logging.getLogger("app.api.dependencies")

# HTTPBearer handles extracting the token from the Authorization header.
# It also automatically integrates with Swagger/OpenAPI UI.
security = HTTPBearer()
optional_security = HTTPBearer(auto_error=False)

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> AuthenticatedUser:
    """
    FastAPI dependency that extracts the Bearer token, validates it, 
    and returns a strongly typed AuthenticatedUser object.
    """
    token = credentials.credentials
    if not token:
        logger.warning("Authentication failed: Missing token in Authorization header.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Validate and extract
    payload = jwt_validator.decode_token(token)
    user = jwt_validator.get_user_from_payload(payload)
    
    logger.info(f"Authentication successful for user_id: {user.user_id}")
    return user

from app.integrations.django_client import DjangoClient, django_client
from app.integrations.courses_api import CoursesAPI
from app.integrations.progress_api import ProgressAPI
from app.integrations.assessments_api import AssessmentsAPI
from app.integrations.certificates_api import CertificatesAPI

def get_raw_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Extract raw JWT token string for downstream Django requests."""
    return credentials.credentials

def get_optional_raw_token(credentials: HTTPAuthorizationCredentials = Depends(optional_security)) -> Optional[str]:
    """Extract raw JWT token string if provided, otherwise return None."""
    return credentials.credentials if credentials else None

def get_django_client() -> DjangoClient:
    return django_client

def get_courses_api(client: DjangoClient = Depends(get_django_client)) -> CoursesAPI:
    return CoursesAPI(client)

def get_progress_api(client: DjangoClient = Depends(get_django_client)) -> ProgressAPI:
    return ProgressAPI(client)

def get_assessments_api(client: DjangoClient = Depends(get_django_client)) -> AssessmentsAPI:
    return AssessmentsAPI(client)

def get_certificates_api(client: DjangoClient = Depends(get_django_client)) -> CertificatesAPI:
    return CertificatesAPI(client)


def require_internal_token(
    request: Request,
    x_internal_token: str = Header(default=""),
):
    """Gate internal/admin operations (knowledge ingest, debug endpoints).

    Requires a matching INTERNAL_ADMIN_TOKEN in the ``X-Internal-Token`` header
    (or as a Bearer token). Development mode short-circuits so local tooling
    keeps working; production has no bypass.
    """
    from app.core.config import settings

    configured = (settings.INTERNAL_ADMIN_TOKEN or "").strip()
    if settings.is_development and not configured:
        return True
    auth = request.headers.get("authorization", "")
    candidate = (x_internal_token or "").strip()
    if auth.lower().startswith("bearer "):
        candidate = auth[7:].strip()
    if configured and candidate and secrets.compare_digest(candidate, configured):
        return True
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Forbidden: valid internal token required.",
    )


def has_internal_token(
    request: Request,
    x_internal_token: str = Header(default=""),
) -> bool:
    """Whether the caller presented a valid internal admin token.

    Unlike :func:`require_internal_token` this never short-circuits in
    development and never raises: it is used to gate *detailed* (info-heavy)
    health payloads behind an explicit token while still answering public
    health probes with a minimal ``{"status": "ok"}``. Keeping the dev bypass
    out of scope here matters because development environments are the most
    commonly exposed and were the exact target of the information-disclosure
    finding.
    """
    from app.core.config import settings

    configured = (settings.INTERNAL_ADMIN_TOKEN or "").strip()
    if not configured:
        return False
    auth = request.headers.get("authorization", "")
    candidate = (x_internal_token or "").strip()
    if auth.lower().startswith("bearer "):
        candidate = auth[7:].strip()
    return bool(candidate) and secrets.compare_digest(candidate, configured)
