from fastapi import APIRouter
from fastapi.param_functions import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import view_sqlite_schema, get_db

router = APIRouter()

@router.get("/health")
async def health():
    return {"status": "ok"}


@router.get("/hello")
async def hello():
    return {"message": "Hello World"}


@router.get("/sqlite_schema")
async def get_sqlite_schema(table_name: str | None = None, db: AsyncSession = Depends(get_db)):
    return await view_sqlite_schema(db, table_name)
