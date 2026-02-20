"""
Dependency injection container for FastAPI.
All dependencies are wired here and injected into routes.
This is the ONLY place where concrete classes are instantiated.
"""
from functools import lru_cache

from integrations.instagram_client import InstagrapiClient
from infrastructure.session_store import InMemorySessionStore
from infrastructure.config import settings
from services.auth_service import AuthService
from services.analysis_service import AnalysisService
from services.unfollow_service import UnfollowService


# --- Singletons ---
# These are created once and reused throughout the application

@lru_cache()
def get_session_store() -> InMemorySessionStore:
    """
    Get the session store singleton.

    Returns:
        InMemorySessionStore instance
    """
    return InMemorySessionStore()


# --- Service Dependencies ---
# These create new instances but inject the singletons

def get_instagram_client() -> InstagrapiClient:
    """
    Create a new Instagram client instance.

    Returns:
        InstagrapiClient instance
    """
    return InstagrapiClient(request_delay=settings.instagram_request_delay)


def get_auth_service(
    session_store: InMemorySessionStore = None
) -> AuthService:
    """
    Create AuthService with dependency injection.

    Args:
        session_store: Session store (injected by FastAPI)

    Returns:
        AuthService instance
    """
    if session_store is None:
        session_store = get_session_store()

    # Note: We create a new Instagram client for each auth attempt
    # The client will be stored in the session after successful auth
    instagram_client = get_instagram_client()

    return AuthService(
        instagram_client=instagram_client,
        session_store=session_store,
        session_ttl_seconds=settings.session_ttl_seconds
    )


def get_analysis_service(
    session_store: InMemorySessionStore = None
) -> AnalysisService:
    """
    Create AnalysisService with dependency injection.

    Args:
        session_store: Session store (injected by FastAPI)

    Returns:
        AnalysisService instance
    """
    if session_store is None:
        session_store = get_session_store()

    return AnalysisService(
        session_store=session_store,
        max_results=settings.max_non_followers_shown,
        posts_to_analyze=settings.posts_to_analyze
    )


def get_unfollow_service(
    session_store: InMemorySessionStore = None
) -> UnfollowService:
    """
    Create UnfollowService with dependency injection.

    Args:
        session_store: Session store (injected by FastAPI)

    Returns:
        UnfollowService instance
    """
    if session_store is None:
        session_store = get_session_store()

    return UnfollowService(
        session_store=session_store,
        unfollow_delay_seconds=settings.unfollow_delay_seconds
    )
