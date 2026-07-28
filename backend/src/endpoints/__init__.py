from fastapi import APIRouter
import endpoints.base as base

api_router = APIRouter()

api_router.include_router(base.router, tags=["default"])
# Add more routes here
# api_router.include_router(base.router, prefix="/users", tags=["users"])