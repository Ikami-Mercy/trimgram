"""
Authentication router - handles login and 2FA endpoints.
NO BUSINESS LOGIC HERE - all logic is in the service layer.
"""
from fastapi import APIRouter, Depends, HTTPException, status
import logging

from models.api import (
    LoginRequest,
    LoginResponse,
    TwoFactorRequest,
    ErrorResponse
)
from models.exceptions import (
    AuthenticationError,
    TwoFactorRequiredError,
    RateLimitError
)
from services.auth_service import AuthService
from dependencies import get_auth_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["authentication"])


@router.post(
    "/login",
    response_model=LoginResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Authentication failed"},
        429: {"model": ErrorResponse, "description": "Rate limit exceeded"},
        449: {"model": ErrorResponse, "description": "2FA required"}
    }
)
def login(
    body: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service)
) -> LoginResponse:
    """
    Authenticate a user with Instagram credentials.

    Args:
        body: LoginRequest with username and password
        auth_service: Injected AuthService instance

    Returns:
        LoginResponse with session token and user ID

    Raises:
        HTTPException: Various error conditions
    """
    try:
        logger.info(f"Login attempt for user: {body.username}")

        session = auth_service.login(body.username, body.password)

        logger.info(f"Login successful for user: {body.username}")

        return LoginResponse(
            session_token=session.session_token,
            user_id=session.user_id,
            message="Login successful"
        )

    except TwoFactorRequiredError as e:
        logger.info(f"2FA required for user: {body.username}")
        raise HTTPException(
            status_code=449,  # Custom status for 2FA required
            detail={
                "error": "2FA_REQUIRED",
                "message": str(e),
                "session_token": e.session_token
            }
        )

    except RateLimitError as e:
        logger.warning(f"Rate limit hit during login for user: {body.username}")
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "error": "RATE_LIMIT",
                "message": str(e)
            }
        )

    except AuthenticationError as e:
        logger.warning(f"Authentication failed for user: {body.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "AUTH_FAILED",
                "message": str(e)
            }
        )

    except Exception as e:
        logger.error(f"Unexpected error during login: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "INTERNAL_ERROR",
                "message": "An unexpected error occurred during login"
            }
        )


@router.post(
    "/2fa",
    response_model=LoginResponse,
    responses={
        401: {"model": ErrorResponse, "description": "2FA verification failed"}
    }
)
def resolve_2fa(
    body: TwoFactorRequest,
    auth_service: AuthService = Depends(get_auth_service)
) -> LoginResponse:
    """
    Resolve two-factor authentication challenge.

    Args:
        body: TwoFactorRequest with session token and 2FA code
        auth_service: Injected AuthService instance

    Returns:
        LoginResponse with authenticated session

    Raises:
        HTTPException: If 2FA verification fails
    """
    try:
        logger.info("2FA verification attempt")

        session = auth_service.resolve_2fa(body.session_token, body.code)

        logger.info("2FA verification successful")

        return LoginResponse(
            session_token=session.session_token,
            user_id=session.user_id,
            message="2FA verification successful"
        )

    except AuthenticationError as e:
        logger.warning(f"2FA verification failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "2FA_FAILED",
                "message": str(e)
            }
        )

    except Exception as e:
        logger.error(f"Unexpected error during 2FA: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "INTERNAL_ERROR",
                "message": "An unexpected error occurred during 2FA verification"
            }
        )
