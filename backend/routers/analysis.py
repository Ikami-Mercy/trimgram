"""
Analysis router - handles follower analysis endpoint.
NO BUSINESS LOGIC HERE - all logic is in the service layer.
"""
from fastapi import APIRouter, Depends, HTTPException, Header, status
import logging

from models.api import AnalysisResponse, ErrorResponse
from models.exceptions import (
    SessionNotFoundError,
    NotAuthenticatedError,
    RateLimitError
)
from services.analysis_service import AnalysisService
from dependencies import get_analysis_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["analysis"])


@router.get(
    "/analysis",
    response_model=AnalysisResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Not authenticated or session expired"},
        429: {"model": ErrorResponse, "description": "Rate limit exceeded"}
    }
)
def analyze_followers(
    session_token: str = Header(..., description="Session token from login"),
    analysis_service: AnalysisService = Depends(get_analysis_service)
) -> AnalysisResponse:
    """
    Analyze user's followers and return ranked list of non-followers.

    This endpoint:
    1. Fetches the user's followers and following lists
    2. Identifies accounts that don't follow back
    3. Calculates interaction scores (MY activity on THEIR posts)
    4. Returns top 100 ranked by least interaction first

    Args:
        session_token: Session token from Authorization header
        analysis_service: Injected AnalysisService instance

    Returns:
        AnalysisResponse with ranked non-followers list

    Raises:
        HTTPException: Various error conditions
    """
    try:
        logger.info("Starting follower analysis")

        result = analysis_service.analyze_non_followers(session_token)

        logger.info(
            f"Analysis complete: {result.non_followers_shown} results returned "
            f"out of {result.total_non_followers} non-followers"
        )

        return AnalysisResponse(
            total_following=result.total_following,
            total_followers=result.total_followers,
            total_non_followers=result.total_non_followers,
            non_followers_shown=result.non_followers_shown,
            results=result.results
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

    except NotAuthenticatedError as e:
        logger.warning(f"Not authenticated: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "NOT_AUTHENTICATED",
                "message": str(e)
            }
        )

    except RateLimitError as e:
        logger.warning(f"Rate limit hit during analysis: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "error": "RATE_LIMIT",
                "message": str(e)
            }
        )

    except Exception as e:
        logger.error(f"Unexpected error during analysis: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "INTERNAL_ERROR",
                "message": "An unexpected error occurred during analysis"
            }
        )
