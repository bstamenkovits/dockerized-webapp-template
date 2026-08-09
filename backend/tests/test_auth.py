import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app import app
from core.database import get_db
from models.auth import AuthSession, AuthUser
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
    """
    Test that a user cannot register with an already existing email.
    """
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


async def test_login_success(session_maker, auth_client):
    """
    Test that a registered user can log in and receives a session_id cookie.
    """
    # create a temp test user
    await auth_client.post(
        "/api/auth/register",
        json={
            "display_name": "Carol",
            "email": "carol@example.com",
            "password": "s3cret-pass",
        },
    )

    # try to log in
    response = await auth_client.post(
        "/api/auth/login",
        json={"email": "carol@example.com", "password": "s3cret-pass"},
    )

    # test a valid response is returned
    assert response.status_code == 200

    # test that a session cookie was set
    session_id = response.cookies.get("session_id")
    assert session_id

    # test that the correct session was stored in the database
    async with session_maker() as session:
        result = await session.execute(
            select(AuthSession).where(AuthSession.id == session_id)
        )
        auth_session = result.scalar_one()
        # compare database session id with cookie session id
        assert auth_session.id == session_id

    # test the session is active (not revoked)
    assert auth_session.revoked_at is None


async def test_login_wrong_password(auth_client):
    """
    Test that a an existing user cannot log in with an incorrect password.
    """
    await auth_client.post(
        "/api/auth/register",
        json={
            "display_name": "Dave",
            "email": "dave@example.com",
            "password": "s3cret-pass",
        },
    )

    response = await auth_client.post(
        "/api/auth/login",
        json={"email": "dave@example.com", "password": "wrong-pass"},
    )

    # test if correct error code is returned
    assert response.status_code == 401
    # test that no session cookie was set
    assert response.cookies.get("session_id") is None


async def test_login_unknown_email(auth_client):
    """
    Test that a you cannot log in with an unknown email.
    """
    response = await auth_client.post(
        "/api/auth/login",
        json={"email": "nobody@example.com", "password": "s3cret-pass"},
    )

    # test if correct error code is returned
    assert response.status_code == 401
    # test that no session cookie was set
    assert response.cookies.get("session_id") is None
