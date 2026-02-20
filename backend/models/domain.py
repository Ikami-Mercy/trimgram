"""
Domain models for the Instagram analyzer.
Pure Pydantic models with no framework dependencies.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class UserModel(BaseModel):
    """Represents an Instagram user."""
    user_id: int = Field(..., description="Instagram user ID")
    username: str = Field(..., description="Instagram username")
    full_name: Optional[str] = Field(None, description="User's full name")
    profile_pic_url: Optional[str] = Field(None, description="Profile picture URL")
    is_private: bool = Field(False, description="Whether account is private")


class FollowRelationshipModel(BaseModel):
    """Represents a follow relationship."""
    user_id: int = Field(..., description="Instagram user ID")
    username: str = Field(..., description="Instagram username")
    full_name: Optional[str] = Field(None, description="User's full name")
    profile_pic_url: Optional[str] = Field(None, description="Profile picture URL")
    is_verified: bool = Field(False, description="Whether account is verified")
    is_private: bool = Field(False, description="Whether account is private")


class PostModel(BaseModel):
    """Represents an Instagram post."""
    post_id: str = Field(..., description="Instagram post ID (pk)")
    user_id: int = Field(..., description="Owner's user ID")
    caption: Optional[str] = Field(None, description="Post caption")
    created_at: Optional[datetime] = Field(None, description="Post creation time")


class InteractionScoreModel(BaseModel):
    """
    Represents interaction score for a non-follower.
    Measures MY interaction on THEIR content.
    """
    user_id: int = Field(..., description="Target user's Instagram ID")
    username: str = Field(..., description="Target user's username")
    full_name: Optional[str] = Field(None, description="Target user's full name")
    profile_pic_url: Optional[str] = Field(None, description="Profile picture URL")
    likes_count: int = Field(0, description="Number of their posts I have liked")
    comments_count: int = Field(0, description="Number of their posts I have commented on")
    total_score: int = Field(0, description="Total interaction score (likes + comments)")

    def calculate_total_score(self) -> int:
        """Calculate the total interaction score."""
        self.total_score = self.likes_count + self.comments_count
        return self.total_score


class SessionModel(BaseModel):
    """Represents an authenticated session."""
    session_token: str = Field(..., description="Unique session identifier")
    user_id: int = Field(..., description="Instagram user ID")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Session creation time")
    expires_at: Optional[datetime] = Field(None, description="Session expiration time")


class NonFollowerAnalysisResult(BaseModel):
    """Result of non-follower analysis with interaction scores."""
    total_following: int = Field(..., description="Total accounts user is following")
    total_followers: int = Field(..., description="Total followers user has")
    total_non_followers: int = Field(..., description="Total non-followers")
    non_followers_shown: int = Field(..., description="Number of non-followers in results (max 100)")
    results: list[InteractionScoreModel] = Field(default_factory=list, description="Ranked non-followers list")
