"""
Custom exceptions for the application.
All exceptions are handled at the service layer and converted to HTTP responses at the router layer.
"""


class InstagramAnalyzerException(Exception):
    """Base exception for all application errors."""
    pass


class AuthenticationError(InstagramAnalyzerException):
    """Raised when Instagram authentication fails."""
    pass


class TwoFactorRequiredError(InstagramAnalyzerException):
    """Raised when 2FA is required for authentication."""
    def __init__(self, message: str = "Two-factor authentication required", session_token: str = None):
        super().__init__(message)
        self.session_token = session_token


class NotAuthenticatedError(InstagramAnalyzerException):
    """Raised when an operation requires authentication but no session exists."""
    pass


class SessionNotFoundError(InstagramAnalyzerException):
    """Raised when a session token is invalid or expired."""
    pass


class RateLimitError(InstagramAnalyzerException):
    """Raised when Instagram rate limit is hit."""
    pass


class UnfollowError(InstagramAnalyzerException):
    """Raised when unfollow operation fails."""
    pass


class UserNotFoundError(InstagramAnalyzerException):
    """Raised when a user cannot be found on Instagram."""
    pass
