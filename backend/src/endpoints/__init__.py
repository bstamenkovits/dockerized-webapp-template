from fastapi import APIRouter
import endpoints.base as base
import endpoints.auth as auth

api_router = APIRouter()

api_router.include_router(base.router, tags=["default"])
api_router.include_router(auth.router)
# Add more routes here
# api_router.include_router(base.router, prefix="/users", tags=["users"])