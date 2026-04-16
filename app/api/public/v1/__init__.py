from fastapi import APIRouter

from app.api.public.v1.conversions import router as conversions_router
from app.api.public.v1.files import router as files_router

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(conversions_router)
v1_router.include_router(files_router)

__all__ = ("v1_router",)
