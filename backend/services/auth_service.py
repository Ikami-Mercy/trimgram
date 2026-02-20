"""
Authentication service - handles all authentication business logic.
Follows Single Responsibility Principle: ONLY handles authentication.
"""
from integrations.interfaces import InstagramAuthInterface, SessionStoreInterface
from models.domain import SessionModel
from models.exceptions import AuthenticationError, TwoFactorRequiredError


class AuthService:
    """
    Service for handling authentication operations.
    All business logic for login and 2FA is here.
    """

    def __init__(
        self,
        instagram_client: InstagramAuthInterface,
        session_store: SessionStoreInterface,
        session_ttl_seconds: int = 1800
    ):
        """
        Initialize authentication service.

        Args:
            instagram_client: Instagram client implementing auth interface
            session_store: Session storage implementation
            session_ttl_seconds: Session time-to-live in seconds (default 30 minutes)
        """
        self.instagram_client = instagram_client
        self.session_store = session_store
        self.session_ttl_seconds = session_ttl_seconds

    def login(self, username: str, password: str) -> SessionModel:
        """
        Authenticate a user and create a session.

        Args:
            username: Instagram username
            password: Instagram password

        Returns:
            SessionModel with session token and user ID

        Raises:
            AuthenticationError: If login fails
            TwoFactorRequiredError: If 2FA is required
        """
        # Authenticate with Instagram
        session = self.instagram_client.login(username, password)

        # Store session
        self.session_store.create_session(
            session_token=session.session_token,
            instagram_client=self.instagram_client,
            user_id=session.user_id,
            ttl_seconds=self.session_ttl_seconds
        )

        return session

    def resolve_2fa(self, session_token: str, code: str) -> SessionModel:
        """
        Resolve two-factor authentication.

        Args:
            session_token: Temporary session token from initial login
            code: 6-digit 2FA code

        Returns:
            SessionModel with authenticated session

        Raises:
            AuthenticationError: If 2FA fails
        """
        # Resolve 2FA with Instagram
        session = self.instagram_client.resolve_2fa(session_token, code)

        # Store authenticated session
        self.session_store.create_session(
            session_token=session.session_token,
            instagram_client=self.instagram_client,
            user_id=session.user_id,
            ttl_seconds=self.session_ttl_seconds
        )

        return session

    def logout(self, session_token: str) -> None:
        """
        Log out a user by deleting their session.

        Args:
            session_token: Session token to invalidate
        """
        self.session_store.delete_session(session_token)
