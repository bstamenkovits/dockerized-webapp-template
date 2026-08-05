from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient

FRONTEND_DIST_ASSETS = Path(__file__).resolve().parents[2] / "frontend" / "dist" / "assets"
FRONTEND_DIST_ASSETS.mkdir(parents=True, exist_ok=True)

from app import app


@pytest.fixture
async def client():
    """
    Provide an AsyncClient that talks directly to the app's ASGI interface.

    ASGITransport lets httpx call the FastAPI app in-process, without opening
    a real network socket. This is useful here because it makes tests fast
    and self-contained (no server process to start/stop) while still
    exercising the full ASGI request/response flow.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as async_client:
        yield async_client
