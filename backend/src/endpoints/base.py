from fastapi import APIRouter
from fastapi.param_functions import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from core.database import view_sqlite_schema, get_db
from core.security import get_current_user
from models.auth import AuthUser


router = APIRouter()


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.get("/ping")
async def ping():
    return {"message": "Pong!"}


@router.get("/ping-database")
async def ping_database(
    user: AuthUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    await db.execute(text("SELECT 1"))
    return {"message": "Database is reachable!"}


@router.get("/hello")
async def hello(user: AuthUser = Depends(get_current_user)):
    name = user.display_name or user.email
    return {"message": f"Hello {name}!"}
