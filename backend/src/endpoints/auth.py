from fastapi import APIRouter
from schemas.auth import RegisterRequest
from models.auth import AuthUser
from fastapi.param_functions import Depends
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.database import view_sqlite_schema, get_db
from core.security import hash_password


router = APIRouter(prefix="/auth", tags=["auth"])


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


