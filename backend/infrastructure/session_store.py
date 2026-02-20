"""
In-memory session storage implementation.
Sessions are stored in memory with TTL (time-to-live).
No database or persistent storage is used.
"""
from typing import Dict, Optional
from datetime import datetime, timedelta
import threading

from integrations.interfaces import SessionStoreInterface


class InMemorySessionStore(SessionStoreInterface):
    """
    In-memory session storage with automatic expiration.
    Thread-safe implementation.
    """

    def __init__(self):
        """Initialize the session store."""
        self._sessions: Dict[str, Dict] = {}
        self._lock = threading.Lock()

    def create_session(
        self,
        session_token: str,
        instagram_client: any,
        user_id: int,
        ttl_seconds: int = 1800
    ) -> None:
        """
        Store a new session.

        Args:
            session_token: Unique session identifier
            instagram_client: Authenticated Instagram client instance
            user_id: Instagram user ID
            ttl_seconds: Time to live in seconds (default 30 minutes)
        """
        with self._lock:
            # Only one active session at a time - terminate existing sessions
            # This implements the "ONE active session at a time" requirement
            if self._sessions:
                self._sessions.clear()

            expires_at = datetime.utcnow() + timedelta(seconds=ttl_seconds)

            self._sessions[session_token] = {
                "client": instagram_client,
                "user_id": user_id,
                "expires_at": expires_at,
                "created_at": datetime.utcnow()
            }

    def get_session(self, session_token: str) -> Optional[Dict]:
        """
        Retrieve a session by token.

        Args:
            session_token: Session identifier

        Returns:
            Dictionary with 'client' and 'user_id' keys, or None if expired/not found
        """
        with self._lock:
            session = self._sessions.get(session_token)

            if not session:
                return None

            # Check if session has expired
            if datetime.utcnow() > session["expires_at"]:
                del self._sessions[session_token]
                return None

            return {
                "client": session["client"],
                "user_id": session["user_id"]
            }

    def delete_session(self, session_token: str) -> None:
        """
        Delete a session.

        Args:
            session_token: Session identifier
        """
        with self._lock:
            if session_token in self._sessions:
                del self._sessions[session_token]

    def cleanup_expired_sessions(self) -> None:
        """Remove all expired sessions from storage."""
        with self._lock:
            current_time = datetime.utcnow()
            expired_tokens = [
                token
                for token, session in self._sessions.items()
                if current_time > session["expires_at"]
            ]

            for token in expired_tokens:
                del self._sessions[token]

    def get_session_count(self) -> int:
        """
        Get the number of active sessions.

        Returns:
            Number of active sessions
        """
        with self._lock:
            self.cleanup_expired_sessions()
            return len(self._sessions)
