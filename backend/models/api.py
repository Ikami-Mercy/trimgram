"""
API request and response models for FastAPI routes.
All HTTP communication uses these Pydantic models.
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from models.domain import InteractionScoreModel


class LoginRequest(BaseModel):
    """Request body for login endpoint."""
    username: str = Field(..., min_length=1, description="Instagram username")
    password: str = Field(..., min_length=1, description="Instagram password")


class LoginResponse(BaseModel):
    """Response for successful login."""
    session_token: str = Field(..., description="Session token for API authentication")
    user_id: int = Field(..., description="Instagram user ID")
    message: str = Field(default="Login successful", description="Success message")


class TwoFactorRequest(BaseModel):
    """Request body for 2FA challenge resolution."""
    session_token: str = Field(..., description="Temporary session token")
    code: str = Field(..., min_length=6, max_length=6, description="6-digit 2FA code")


class AnalysisResponse(BaseModel):
    """Response for analysis endpoint."""
    total_following: int = Field(..., description="Total accounts user is following")
    total_followers: int = Field(..., description="Total followers user has")
    total_non_followers: int = Field(..., description="Total non-followers")
    non_followers_shown: int = Field(..., description="Number of non-followers shown (max 100)")
    results: List[InteractionScoreModel] = Field(default_factory=list, description="Ranked non-followers")


class UnfollowRequest(BaseModel):
    """Request body for unfollow endpoint."""
    session_token: str = Field(..., description="Session token")
    target_user_id: int = Field(..., description="Instagram user ID to unfollow")


class UnfollowResponse(BaseModel):
    """Response for unfollow endpoint."""
    success: bool = Field(..., description="Whether unfollow was successful")
    message: str = Field(..., description="Success or error message")


class ErrorResponse(BaseModel):
    """Standard error response."""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Human-readable error message")
    details: Optional[str] = Field(None, description="Additional error details")
