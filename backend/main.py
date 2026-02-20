"""
Main FastAPI application entry point.
Sets up the application, CORS, logging, and routes.
"""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from infrastructure.config import settings
from routers import auth, analysis, unfollow
from dependencies import get_session_store


# Configure logging
logging.basicConfig(
    level=logging.INFO if not settings.debug else logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Disable password logging - SECURITY REQUIREMENT
logging.getLogger("fastapi").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler.
    Runs startup and shutdown logic.
    """
    # Startup
    logger.info(f"Starting {settings.app_name} v{settings.api_version}")
    logger.info(f"Debug mode: {settings.debug}")
    logger.info(f"Session TTL: {settings.session_ttl_seconds} seconds")

    # Initialize session store
    session_store = get_session_store()
    logger.info("Session store initialized")

    yield

    # Shutdown
    logger.info("Shutting down application")
    session_store.cleanup_expired_sessions()


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.api_version,
    description="Instagram follower analyzer - Clean up who you follow. One tap at a time.",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins_list(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(analysis.router)
app.include_router(unfollow.router)


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "app": settings.app_name,
        "version": settings.api_version,
        "status": "running",
        "message": "Welcome to Trimgram API"
    }


@app.get("/health")
def health_check():
    """Health check endpoint for monitoring."""
    session_store = get_session_store()
    return {
        "status": "healthy",
        "active_sessions": session_store.get_session_count()
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info"
    )
