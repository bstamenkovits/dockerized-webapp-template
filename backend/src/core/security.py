from datetime import datetime

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from fastapi import Cookie, Depends, HTTPException, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import SESSION_TTL
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


async def resolve_active_session(
    session_id: str | None,
    db: AsyncSession,
) -> AuthSession:
    """
    Look up the session for session_id and raise 401 if it's missing, revoked, or expired.
    """
    if session_id is None:
        logger.warning("No session_id cookie provided")
        raise HTTPException(status_code=401, detail="Not authenticated.")

    result = await db.execute(select(AuthSession).where(AuthSession.id == session_id))
    session = result.scalar_one_or_none()

    if session is None:
        logger.warning("Session not found")
        raise HTTPException(status_code=401, detail="Not authenticated.")

    if session.revoked_at is not None:
        logger.warning("Session revoked")
        raise HTTPException(status_code=401, detail="Not authenticated.")

    if session.expires_at < datetime.now().isoformat():
        logger.warning("Session expired")
        raise HTTPException(status_code=401, detail="Not authenticated.")

    return session


async def get_current_user(
    response: Response,
    session_id: str | None = Cookie(default=None),
    db: AsyncSession = Depends(get_db),
) -> AuthUser:
    """
    Resolve the authenticated user from the session_id cookie or raise 401.

    On success, slides the session's expiration forward by SESSION_TTL and reissues
    the cookie, so a user who visits at least once per TTL window stays logged in.
    """
    session = await resolve_active_session(session_id, db)

    result = await db.execute(select(AuthUser).where(AuthUser.id == session.user_id))
    user = result.scalar_one_or_none()

    if user is None:
        logger.warning("User not found")
        raise HTTPException(status_code=401, detail="Not authenticated.")

    # sliding-window: extend the session and reissue the cookie
    now = datetime.now()
    session.expires_at = (now + SESSION_TTL).isoformat()
    session.user_last_active = now.isoformat()
    await db.commit()

    response.set_cookie(
        key="session_id",
        value=session.id,
        max_age=int(SESSION_TTL.total_seconds()),
        httponly=True,
        secure=True,
        samesite="lax",
    )

    return user
