"""
Unfollow service - handles unfollowing operations.
Follows Single Responsibility Principle: ONLY handles unfollowing.
"""
import time
import logging

from integrations.interfaces import InstagramUnfollowInterface, SessionStoreInterface
from models.exceptions import SessionNotFoundError, UnfollowError

logger = logging.getLogger(__name__)


class UnfollowService:
    """
    Service for unfollowing users.
    Implements rate limiting and safety checks.
    """

    def __init__(
        self,
        session_store: SessionStoreInterface,
        unfollow_delay_seconds: float = 15.0
    ):
        """
        Initialize unfollow service.

        Args:
            session_store: Session storage implementation
            unfollow_delay_seconds: Delay between unfollows (default 15 seconds)
        """
        self.session_store = session_store
        self.unfollow_delay_seconds = unfollow_delay_seconds
        self._last_unfollow_time = 0.0

    def unfollow_user(self, session_token: str, target_user_id: int) -> bool:
        """
        Unfollow a specific user.

        Args:
            session_token: User's session token
            target_user_id: Instagram user ID to unfollow

        Returns:
            True if successful

        Raises:
            SessionNotFoundError: If session is invalid or expired
            UnfollowError: If unfollow operation fails
        """
        # Retrieve session
        session = self.session_store.get_session(session_token)
        if not session:
            raise SessionNotFoundError("Session not found or expired. Please log in again.")

        instagram_client: InstagramUnfollowInterface = session["client"]
        user_id = session["user_id"]

        # Safety check: don't unfollow yourself
        if target_user_id == user_id:
            raise UnfollowError("Cannot unfollow yourself.")

        # Apply rate limiting
        current_time = time.time()
        time_since_last_unfollow = current_time - self._last_unfollow_time

        if time_since_last_unfollow < self.unfollow_delay_seconds:
            wait_time = self.unfollow_delay_seconds - time_since_last_unfollow
            logger.info(f"Rate limiting: waiting {wait_time:.1f} seconds")
            time.sleep(wait_time)

        # Perform unfollow
        logger.info(f"Unfollowing user {target_user_id}")
        result = instagram_client.unfollow_user(target_user_id)

        self._last_unfollow_time = time.time()

        logger.info(f"Successfully unfollowed user {target_user_id}")
        return result
