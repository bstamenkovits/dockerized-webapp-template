from pathlib import Path

from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# ---------------------------------------------------------------------------
# API routes
#
# Everything the frontend talks to lives under /api so it never collides with
# the client-side (React Router) routes below. Register these BEFORE the SPA
# catch-all so they always win.
# ---------------------------------------------------------------------------
api_router = APIRouter()


@api_router.get("/health")
async def health():
    return {"status": "ok"}


@api_router.get("/hello")
async def hello():
    return {"message": "Hello World"}


app.include_router(api_router, prefix="/api")


# ---------------------------------------------------------------------------
# Serve the built frontend (single-page app)
#
# app.py lives at backend/src/app.py, so the repo root is three levels up and
# the Vite build output is at <repo>/frontend/dist.
# ---------------------------------------------------------------------------
DIST_DIR = Path(__file__).resolve().parents[2] / "frontend" / "dist"

# Vite emits hashed JS/CSS/image bundles under dist/assets. Serve them directly.
app.mount("/assets", StaticFiles(directory=DIST_DIR / "assets"), name="assets")


@app.get("/{full_path:path}")
async def spa_fallback(full_path: str):
    """Serve the SPA for any non-API path.

    A real file in dist/ (favicon, manifest, robots.txt, ...) is returned
    as-is. Anything else returns index.html so that deep links and page
    refreshes on nested client routes (e.g. /dashboard/settings) load the app
    and let React Router resolve the route in the browser.
    """

    # Keep unknown /api/* paths as JSON 404s instead of silently handing back
    # index.html.
    if full_path == "api" or full_path.startswith("api/"):
        raise HTTPException(status_code=404, detail="Not found")

    candidate = DIST_DIR / full_path
    if full_path and candidate.is_file():
        return FileResponse(candidate)

    return FileResponse(DIST_DIR / "index.html")
