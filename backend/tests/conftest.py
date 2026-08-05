from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient

FRONTEND_DIST_ASSETS = Path(__file__).resolve().parents[2] / "frontend" / "dist" / "assets"
FRONTEND_DIST_ASSETS.mkdir(parents=True, exist_ok=True)

from app import app


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
