from datetime import datetime

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from fastapi import Cookie, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from models.auth import AuthSession, AuthUser
from logging import getLogger


logger = getLogger(__name__)

_password_hasher = PasswordHasher()


def hash_password(password: str) -> str:
    """Hash a plaintext password using Argon2."""
    return _password_hasher.hash(password)


def verify_password(hashed_password: str, password: str) -> bool:
    """Return True if the plaintext password matches the Argon2 hash."""
    try:
        return _password_hasher.verify(hashed_password, password)
    except VerifyMismatchError:
        return False


async def get_current_user(
    session_id: str | None = Cookie(default=None),
    db: AsyncSession = Depends(get_db),
) -> AuthUser:
    """
    Resolve the authenticated user from the session_id cookie or raise 401.

    Uses the session_id in the cookie to look up a session in the database. Raises
    a 401 code (not authenticated) if
        - session_id is not provided
        - session does not exist
        - session has been revoked (e.g. logged out)
        - session has expired
        - user does not exist
    """
    if session_id is None:
        logger.warning("No session_id cookie provided")
        raise HTTPException(status_code=401, detail="Not authenticated.")

    # Look up session in database
    result = await db.execute(select(AuthSession).where(AuthSession.id == session_id))
    session = result.scalar_one_or_none()

    # Validate session
    if session is None:
        logger.warning("Session not found")
        raise HTTPException(status_code=401, detail="Not authenticated.")

    if session.revoked_at is not None:
        logger.warning("Session revoked")
        raise HTTPException(status_code=401, detail="Not authenticated.")

    if session.expires_at < datetime.now().isoformat():
        logger.warning("Session expired")
        raise HTTPException(status_code=401, detail="Not authenticated.")

    # Look up user in database
    result = await db.execute(select(AuthUser).where(AuthUser.id == session.user_id))
    user = result.scalar_one_or_none()

    # validate user
    if user is None:
        logger.warning("User not found")
        raise HTTPException(status_code=401, detail="Not authenticated.")

    return user
