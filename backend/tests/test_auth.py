import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app import app
from core.database import get_db
from models.auth import AuthUser
from models.base import Base
import models.auth  # noqa: F401  registers auth tables on Base.metadata


@pytest.fixture
async def engine():
    """
    Pytest Fixture: throwaway in-memory SQLite engine.

    StaticPool keeps a single connection alive, so the schema created below is
    visible to every request bound to this engine.
    """

    # create a temporary in-memory sqlite database
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # fill database with relevant tables based on sqlalchemy models
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    await engine.dispose()


@pytest.fixture
def session_maker(engine):
    """Pytest Fixture: async session factory bound to the in-memory engine."""
    return async_sessionmaker(engine, expire_on_commit=False)


@pytest.fixture
async def auth_client(session_maker):
    """
    Pytest Fixture: AsyncClient backed by the in-memory SQLite engine.

    get_db is overridden to hand out sessions bound to this engine instead of
    the real app database.
    """

    # override get_db to use this in-memory database instead of real database
    async def override_get_db():
        async with session_maker() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    # create custom client for httpx calls
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

    # cleanup
    app.dependency_overrides.clear()


async def test_register_success(session_maker, auth_client):
    """
    Test that a new user can be registered successfully.

    Check the API response is 200 OK and that the user landed in the database
    with the expected data and a hashed (not plaintext) password.
    """
    response = await auth_client.post(
        "/api/auth/register",
        json={
            "display_name": "Alice",
            "email": "alice@example.com",
            "password": "s3cret-pass",
        },
    )

    assert response.status_code == 200

    # verify the user was persisted with the correct data
    async with session_maker() as session:
        result = await session.execute(
            select(AuthUser).where(AuthUser.email == "alice@example.com")
        )
        user = result.scalar_one()

    assert user.display_name == "Alice"
    assert user.email == "alice@example.com"
    assert user.hashed_password != "s3cret-pass"


async def test_register_duplicate_email(auth_client):
    payload = {
        "display_name": "Bob",
        "email": "bob@example.com",
        "password": "s3cret-pass",
    }
    first = await auth_client.post("/api/auth/register", json=payload)
    assert first.status_code == 200

    second = await auth_client.post(
        "/api/auth/register",
        json={**payload, "display_name": "Bobby"},
    )

    assert second.status_code == 400
