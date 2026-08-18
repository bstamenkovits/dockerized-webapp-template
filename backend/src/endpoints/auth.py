from datetime import datetime, timedelta
from logging import getLogger

from fastapi import APIRouter, Cookie
from schemas.auth import LoginRequest, RegisterRequest, UserOut
from models.auth import AuthSession, AuthUser
from fastapi.param_functions import Depends
from fastapi import HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.config import settings
from core.database import view_sqlite_schema, get_db
from core.security import get_current_user, hash_password, resolve_active_session, verify_password


router = APIRouter(prefix="/auth", tags=["auth"])
logger = getLogger(__name__)


@router.post("/register")
async def register(payload: RegisterRequest, db: AsyncSession = Depends(get_db)):
    display_name = payload.display_name
    email = payload.email
    password = payload.password

    # check if user already exists
    existing_user = await db.execute(select(AuthUser).where(AuthUser.email == email))
    existing_user = existing_user.scalar_one_or_none()

    if existing_user:
        raise HTTPException(status_code=400, detail="Account with this email already exists.")

    # create user
    new_user = AuthUser(
        display_name=display_name,
        email=email,
        hashed_password=hash_password(password),
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)  # not necessary in this case, but good habit in case the database has default fields
    return


@router.post("/login")
async def login(payload: LoginRequest, response: Response, db: AsyncSession = Depends(get_db)):
    SESSION_TTL = timedelta(days=settings.session_ttl_days)

    # look up the user by email
    result = await db.execute(select(AuthUser).where(AuthUser.email == payload.email))
    user = result.scalar_one_or_none()

    # generic error to avoid revealing whether the email or password was wrong
    if user is None or not verify_password(user.hashed_password, payload.password):
        logger.warning("Login failed for %s", payload.email)
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    # create a session for the authenticated user
    now = datetime.now()
    session = AuthSession(
        user_id=user.id,
        created_at=now.isoformat(),
        expires_at=(now + SESSION_TTL).isoformat(),
        user_last_active=now.isoformat(),
    )
    db.add(session)
    await db.commit()
    await db.refresh(session)  # update session object with generated session id (see default AuthSession.id default factory)

    response.set_cookie(
        key="session_id",
        value=session.id,
        max_age=int(SESSION_TTL.total_seconds()),
        httponly=True,
        secure=True,
        samesite="lax",
    )
    logger.info("Login succeeded for user_id=%s", user.id)
    return


@router.post("/logout")
async def logout(
    response: Response,
    session_id: str | None = Cookie(default=None),
    db: AsyncSession = Depends(get_db),
):
    session = await resolve_active_session(session_id, db)
    session.revoked_at = datetime.now().isoformat()
    await db.commit()

    response.delete_cookie(key="session_id")
    logger.info("Logout succeeded for user_id=%s", session.user_id)
    return


@router.get("/me", response_model=UserOut)
async def me(user: AuthUser = Depends(get_current_user)):
    """
    Get the currently authenticated user's information (used for frontend auth state).
    """
    return user
