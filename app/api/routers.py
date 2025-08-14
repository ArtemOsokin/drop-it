from fastapi import APIRouter

from .routes.auth import router as auth_router
from .routes.drops import router as drops_router
from .routes.health_check import router as health_router
from .routes.users import router as users_router

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(users_router, prefix="/users", tags=["users"])
v1_router.include_router(auth_router, prefix="/auth", tags=["auth"])
v1_router.include_router(drops_router, prefix="/drops", tags=["drops"])
v1_router.include_router(health_router, prefix="/health-check", tags=["health"])

api_router = APIRouter()
api_router.include_router(v1_router)
