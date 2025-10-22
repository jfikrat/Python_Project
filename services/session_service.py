"""
Session management service for storing temporary data between API calls.

NOTE: This is an in-memory implementation suitable for development.
For production, use Redis, Memcached, or a database with TTL support.
"""
import uuid
from datetime import datetime, timedelta
from typing import Any


class SessionService:
    """In-memory session storage for idea details."""

    def __init__(self, ttl_minutes: int = 30):
        """
        Initialize session storage.

        Args:
            ttl_minutes: Time-to-live for sessions in minutes (default: 30)
        """
        self._storage: dict[str, dict[str, Any]] = {}
        self._ttl = timedelta(minutes=ttl_minutes)

    def create_session(self, data: dict[str, Any]) -> str:
        """
        Create a new session and store data.

        Args:
            data: Dictionary of data to store

        Returns:
            session_id: Unique session identifier
        """
        session_id = str(uuid.uuid4())
        self._storage[session_id] = {
            "data": data,
            "created_at": datetime.now(),
            "expires_at": datetime.now() + self._ttl,
        }
        self._cleanup_expired()
        return session_id

    def get_session(self, session_id: str) -> dict[str, Any] | None:
        """
        Retrieve session data by ID.

        Args:
            session_id: Session identifier

        Returns:
            Session data dictionary or None if not found/expired
        """
        if session_id not in self._storage:
            return None

        session = self._storage[session_id]

        # Check expiration
        if datetime.now() > session["expires_at"]:
            del self._storage[session_id]
            return None

        return session["data"]

    def delete_session(self, session_id: str) -> bool:
        """
        Delete a session.

        Args:
            session_id: Session identifier

        Returns:
            True if deleted, False if not found
        """
        if session_id in self._storage:
            del self._storage[session_id]
            return True
        return False

    def _cleanup_expired(self):
        """Remove expired sessions (runs on each create_session call)."""
        now = datetime.now()
        expired_ids = [
            sid for sid, session in self._storage.items()
            if now > session["expires_at"]
        ]
        for sid in expired_ids:
            del self._storage[sid]

    def get_session_count(self) -> int:
        """Get current number of active sessions (for monitoring)."""
        self._cleanup_expired()
        return len(self._storage)
