"""
Instagram integration interfaces following Interface Segregation Principle.
Each interface defines a narrow contract for a specific Instagram capability.
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from models.domain import UserModel, FollowRelationshipModel, PostModel, SessionModel


class InstagramAuthInterface(ABC):
    """Interface for Instagram authentication operations."""

    @abstractmethod
    def login(self, username: str, password: str) -> SessionModel:
        """
        Authenticate a user with Instagram.

        Args:
            username: Instagram username
            password: Instagram password

        Returns:
            SessionModel containing session info and user ID

        Raises:
            AuthenticationError: If login fails
            TwoFactorRequiredError: If 2FA is enabled
        """
        pass

    @abstractmethod
    def resolve_2fa(self, session_token: str, code: str) -> SessionModel:
        """
        Resolve two-factor authentication challenge.

        Args:
            session_token: Temporary session token from initial login attempt
            code: 6-digit 2FA code

        Returns:
            SessionModel with authenticated session

        Raises:
            AuthenticationError: If 2FA code is invalid
        """
        pass

    @abstractmethod
    def get_user_id(self) -> int:
        """
        Get the authenticated user's Instagram ID.

        Returns:
            Instagram user ID

        Raises:
            NotAuthenticatedError: If no active session
        """
        pass


class InstagramFollowerInterface(ABC):
    """Interface for fetching follower/following data."""

    @abstractmethod
    def get_followers(self, user_id: int) -> Dict[int, FollowRelationshipModel]:
        """
        Fetch all followers for a given user.

        Args:
            user_id: Instagram user ID

        Returns:
            Dictionary mapping user_id to FollowRelationshipModel

        Raises:
            RateLimitError: If Instagram rate limit is hit
        """
        pass

    @abstractmethod
    def get_following(self, user_id: int) -> Dict[int, FollowRelationshipModel]:
        """
        Fetch all accounts a user is following.

        Args:
            user_id: Instagram user ID

        Returns:
            Dictionary mapping user_id to FollowRelationshipModel

        Raises:
            RateLimitError: If Instagram rate limit is hit
        """
        pass

    @abstractmethod
    def get_user_posts(self, user_id: int, count: int = 12) -> List[PostModel]:
        """
        Fetch recent posts from a user.

        Args:
            user_id: Instagram user ID
            count: Number of posts to fetch (default 12)

        Returns:
            List of PostModel objects

        Raises:
            RateLimitError: If Instagram rate limit is hit
        """
        pass

    @abstractmethod
    def get_post_likers(self, post_id: str) -> List[int]:
        """
        Get list of user IDs who liked a post.

        Args:
            post_id: Instagram post ID (pk)

        Returns:
            List of user IDs who liked the post
        """
        pass

    @abstractmethod
    def get_post_comments(self, post_id: str) -> List[Dict]:
        """
        Get all comments on a post.

        Args:
            post_id: Instagram post ID (pk)

        Returns:
            List of comment dictionaries with user info
        """
        pass


class InstagramUnfollowInterface(ABC):
    """Interface for unfollow operations."""

    @abstractmethod
    def unfollow_user(self, user_id: int) -> bool:
        """
        Unfollow a specific user.

        Args:
            user_id: Instagram user ID to unfollow

        Returns:
            True if successful, False otherwise

        Raises:
            RateLimitError: If Instagram rate limit is hit
            NotAuthenticatedError: If no active session
        """
        pass


class SessionStoreInterface(ABC):
    """Interface for session storage operations."""

    @abstractmethod
    def create_session(self, session_token: str, instagram_client: any, user_id: int, ttl_seconds: int = 1800) -> None:
        """
        Store a new session.

        Args:
            session_token: Unique session identifier
            instagram_client: Authenticated Instagram client instance
            user_id: Instagram user ID
            ttl_seconds: Time to live in seconds (default 30 minutes)
        """
        pass

    @abstractmethod
    def get_session(self, session_token: str) -> Optional[Dict]:
        """
        Retrieve a session by token.

        Args:
            session_token: Session identifier

        Returns:
            Dictionary with 'client' and 'user_id' keys, or None if expired/not found
        """
        pass

    @abstractmethod
    def delete_session(self, session_token: str) -> None:
        """
        Delete a session.

        Args:
            session_token: Session identifier
        """
        pass

    @abstractmethod
    def cleanup_expired_sessions(self) -> None:
        """Remove all expired sessions from storage."""
        pass
