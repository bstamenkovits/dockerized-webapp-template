from collections.abc import AsyncGenerator
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from core.config import config


engine = create_async_engine(config.db_url)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


async def view_sqlite_schema(db: AsyncSession, table_name: str | None = None):
    if table_name:
        # Show metadata for a specific table
        query = text("""
            SELECT name, sql
            FROM sqlite_schema
            WHERE type = 'table' AND name = :table_name;
        """)
        result = await db.execute(query,params={"table_name": table_name})

    else:
        # List all tables in the database
        query = text("""
            SELECT name, sql
            FROM sqlite_schema
            WHERE type = 'table' AND name NOT LIKE 'sqlite_%';
        """)
        result = await db.execute(query)

    return result.mappings().all()
