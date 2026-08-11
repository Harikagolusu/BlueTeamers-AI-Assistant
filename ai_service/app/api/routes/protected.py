from fastapi import APIRouter, Depends
from typing import Dict, Any

from app.api.dependencies import get_current_user
from app.models.authenticated_user import AuthenticatedUser

router = APIRouter(tags=["Protected"])

@router.get("/me")
async def get_current_user_profile(
    current_user: AuthenticatedUser = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Returns the authenticated user details based on the provided JWT.
    If the JWT is invalid or missing, a 401 Unauthorized error is returned.
    """
    return {
        "authenticated": True,
        "user": current_user.model_dump()
    }
