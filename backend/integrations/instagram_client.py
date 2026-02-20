"""
Concrete implementation of Instagram integration using instagrapi library.
This is the ONLY module that imports instagrapi - all other modules depend on interfaces.
"""
import uuid
import time
from typing import Dict, List, Optional
from instagrapi import Client
from instagrapi.exceptions import (
    LoginRequired,
    TwoFactorRequired,
    PleaseWaitFewMinutes,
    UserNotFound as InstagrapiUserNotFound
)

from integrations.interfaces import (
    InstagramAuthInterface,
    InstagramFollowerInterface,
    InstagramUnfollowInterface,
)
from models.domain import (
    FollowRelationshipModel,
    PostModel,
    SessionModel,
)
from models.exceptions import (
    AuthenticationError,
    TwoFactorRequiredError,
    NotAuthenticatedError,
    RateLimitError,
    UnfollowError,
    UserNotFoundError,
)


class InstagrapiClient(InstagramAuthInterface, InstagramFollowerInterface, InstagramUnfollowInterface):
    """
    Concrete implementation of Instagram integration using instagrapi.
    Implements all Instagram interfaces.
    """

    def __init__(self, request_delay: float = 2.0):
        """
        Initialize Instagram client.

        Args:
            request_delay: Delay between requests in seconds (default 2.0)
        """
        self.client: Optional[Client] = None
        self.request_delay = request_delay
        self._authenticated_user_id: Optional[int] = None

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
            RateLimitError: If Instagram rate limit is hit
        """
        try:
            self.client = Client()
            self.client.delay_range = [self.request_delay, self.request_delay + 1]

            self.client.login(username, password)

            self._authenticated_user_id = self.client.user_id
            session_token = str(uuid.uuid4())

            return SessionModel(
                session_token=session_token,
                user_id=self._authenticated_user_id
            )

        except TwoFactorRequired as e:
            # Generate temporary session token for 2FA flow
            temp_token = str(uuid.uuid4())
            raise TwoFactorRequiredError(
                message="Two-factor authentication required. Please provide your 2FA code.",
                session_token=temp_token
            )
        except PleaseWaitFewMinutes:
            raise RateLimitError("Instagram rate limit hit. Please wait a few minutes and try again.")
        except LoginRequired:
            raise AuthenticationError("Invalid username or password.")
        except Exception as e:
            raise AuthenticationError(f"Login failed: {str(e)}")

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
        try:
            if not self.client:
                raise AuthenticationError("No pending 2FA challenge found.")

            # Use instagrapi's challenge resolution
            self.client.two_factor_login(code)

            self._authenticated_user_id = self.client.user_id
            new_session_token = str(uuid.uuid4())

            return SessionModel(
                session_token=new_session_token,
                user_id=self._authenticated_user_id
            )

        except Exception as e:
            raise AuthenticationError(f"2FA verification failed: {str(e)}")

    def get_user_id(self) -> int:
        """
        Get the authenticated user's Instagram ID.

        Returns:
            Instagram user ID

        Raises:
            NotAuthenticatedError: If no active session
        """
        if not self.client or not self._authenticated_user_id:
            raise NotAuthenticatedError("No authenticated session found.")
        return self._authenticated_user_id

    def get_followers(self, user_id: int) -> Dict[int, FollowRelationshipModel]:
        """
        Fetch all followers for a given user.

        Args:
            user_id: Instagram user ID

        Returns:
            Dictionary mapping user_id to FollowRelationshipModel

        Raises:
            RateLimitError: If Instagram rate limit is hit
            NotAuthenticatedError: If no active session
        """
        if not self.client:
            raise NotAuthenticatedError("No authenticated session found.")

        try:
            followers = self.client.user_followers(user_id)

            return {
                uid: FollowRelationshipModel(
                    user_id=uid,
                    username=user.username,
                    full_name=user.full_name or "",
                    profile_pic_url=str(user.profile_pic_url) if user.profile_pic_url else "",
                    is_verified=user.is_verified,
                    is_private=user.is_private
                )
                for uid, user in followers.items()
            }
        except PleaseWaitFewMinutes:
            raise RateLimitError("Instagram rate limit hit while fetching followers.")
        except Exception as e:
            raise RateLimitError(f"Error fetching followers: {str(e)}")

    def get_following(self, user_id: int) -> Dict[int, FollowRelationshipModel]:
        """
        Fetch all accounts a user is following.

        Args:
            user_id: Instagram user ID

        Returns:
            Dictionary mapping user_id to FollowRelationshipModel

        Raises:
            RateLimitError: If Instagram rate limit is hit
            NotAuthenticatedError: If no active session
        """
        if not self.client:
            raise NotAuthenticatedError("No authenticated session found.")

        try:
            following = self.client.user_following(user_id)

            return {
                uid: FollowRelationshipModel(
                    user_id=uid,
                    username=user.username,
                    full_name=user.full_name or "",
                    profile_pic_url=str(user.profile_pic_url) if user.profile_pic_url else "",
                    is_verified=user.is_verified,
                    is_private=user.is_private
                )
                for uid, user in following.items()
            }
        except PleaseWaitFewMinutes:
            raise RateLimitError("Instagram rate limit hit while fetching following list.")
        except Exception as e:
            raise RateLimitError(f"Error fetching following list: {str(e)}")

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
            UserNotFoundError: If user not found
        """
        if not self.client:
            raise NotAuthenticatedError("No authenticated session found.")

        try:
            time.sleep(self.request_delay)  # Rate limiting
            medias = self.client.user_medias(user_id, amount=count)

            return [
                PostModel(
                    post_id=str(media.pk),
                    user_id=media.user.pk,
                    caption=media.caption_text if media.caption_text else "",
                    created_at=media.taken_at
                )
                for media in medias
            ]
        except InstagrapiUserNotFound:
            raise UserNotFoundError(f"User {user_id} not found.")
        except PleaseWaitFewMinutes:
            raise RateLimitError("Instagram rate limit hit while fetching posts.")
        except Exception as e:
            # Return empty list if user has no posts or account is private
            return []

    def get_post_likers(self, post_id: str) -> List[int]:
        """
        Get list of user IDs who liked a post.

        Args:
            post_id: Instagram post ID (pk)

        Returns:
            List of user IDs who liked the post
        """
        if not self.client:
            raise NotAuthenticatedError("No authenticated session found.")

        try:
            time.sleep(self.request_delay)  # Rate limiting
            likers = self.client.media_likers(post_id)
            return [liker.pk for liker in likers]
        except Exception:
            # Return empty list if we can't fetch likers (private account, etc.)
            return []

    def get_post_comments(self, post_id: str) -> List[Dict]:
        """
        Get all comments on a post.

        Args:
            post_id: Instagram post ID (pk)

        Returns:
            List of comment dictionaries with user info
        """
        if not self.client:
            raise NotAuthenticatedError("No authenticated session found.")

        try:
            time.sleep(self.request_delay)  # Rate limiting
            comments = self.client.media_comments(post_id)

            return [
                {
                    "user_id": comment.user.pk,
                    "username": comment.user.username,
                    "text": comment.text
                }
                for comment in comments
            ]
        except Exception:
            # Return empty list if we can't fetch comments
            return []

    def unfollow_user(self, user_id: int) -> bool:
        """
        Unfollow a specific user.

        Args:
            user_id: Instagram user ID to unfollow

        Returns:
            True if successful

        Raises:
            RateLimitError: If Instagram rate limit is hit
            NotAuthenticatedError: If no active session
            UnfollowError: If unfollow fails
        """
        if not self.client:
            raise NotAuthenticatedError("No authenticated session found.")

        try:
            time.sleep(self.request_delay)  # Rate limiting
            result = self.client.user_unfollow(user_id)
            return result
        except PleaseWaitFewMinutes:
            raise RateLimitError("Instagram rate limit hit. Please wait before unfollowing more accounts.")
        except Exception as e:
            raise UnfollowError(f"Failed to unfollow user: {str(e)}")
