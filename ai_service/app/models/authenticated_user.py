from pydantic import BaseModel, Field

class AuthenticatedUser(BaseModel):
    """
    Model representing an authenticated user.
    Derived strictly from verified JWT claims.
    """
    user_id: int = Field(..., description="The unique user ID from Django")
    email: str = Field(..., description="The user's email address")
    is_authenticated: bool = Field(default=True, description="Authentication status flag")
