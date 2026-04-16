from fastapi import APIRouter

from app.api.public.v1 import v1_router

public_router = APIRouter(prefix="/api")
public_router.include_router(v1_router)

__all__ = ("public_router",)
