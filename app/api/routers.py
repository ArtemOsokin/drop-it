from fastapi import APIRouter

from .views.auth import router as auth_router
from .views.drops import router as drops_router
from .views.users import router as users_router

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(users_router, prefix="/users", tags=["users"])
v1_router.include_router(auth_router, prefix="/auth", tags=["auth"])
v1_router.include_router(drops_router, prefix="/drops", tags=["drops"])

api_router = APIRouter()
api_router.include_router(v1_router)
