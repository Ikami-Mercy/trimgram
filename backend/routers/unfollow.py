"""
Unfollow router - handles unfollow endpoint.
NO BUSINESS LOGIC HERE - all logic is in the service layer.
"""
from fastapi import APIRouter, Depends, HTTPException, status
import logging

from models.api import UnfollowRequest, UnfollowResponse, ErrorResponse
from models.exceptions import (
    SessionNotFoundError,
    UnfollowError,
    RateLimitError
)
from services.unfollow_service import UnfollowService
from dependencies import get_unfollow_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["unfollow"])


@router.post(
    "/unfollow",
    response_model=UnfollowResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Not authenticated or session expired"},
        429: {"model": ErrorResponse, "description": "Rate limit exceeded"},
        400: {"model": ErrorResponse, "description": "Invalid request"}
    }
)
def unfollow(
    body: UnfollowRequest,
    unfollow_service: UnfollowService = Depends(get_unfollow_service)
) -> UnfollowResponse:
    """
    Unfollow a specific Instagram user.

    Args:
        body: UnfollowRequest with session token and target user ID
        unfollow_service: Injected UnfollowService instance

    Returns:
        UnfollowResponse with success status

    Raises:
        HTTPException: Various error conditions
    """
    try:
        logger.info(f"Unfollow request for user {body.target_user_id}")

        result = unfollow_service.unfollow_user(
            session_token=body.session_token,
            target_user_id=body.target_user_id
        )

        if result:
            logger.info(f"Successfully unfollowed user {body.target_user_id}")
            return UnfollowResponse(
                success=True,
                message=f"Successfully unfollowed user {body.target_user_id}"
            )
        else:
            logger.warning(f"Unfollow failed for user {body.target_user_id}")
            return UnfollowResponse(
                success=False,
                message="Unfollow operation failed"
            )

    except SessionNotFoundError as e:
        logger.warning(f"Session not found: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "SESSION_EXPIRED",
                "message": str(e)
            }
        )

    except UnfollowError as e:
        logger.warning(f"Unfollow error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "UNFOLLOW_FAILED",
                "message": str(e)
            }
        )

    except RateLimitError as e:
        logger.warning(f"Rate limit hit during unfollow: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "error": "RATE_LIMIT",
                "message": str(e)
            }
        )

    except Exception as e:
        logger.error(f"Unexpected error during unfollow: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "INTERNAL_ERROR",
                "message": "An unexpected error occurred during unfollow"
            }
        )
