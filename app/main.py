from fastapi import FastAPI

from app.api import routers
from app.middlewares.error_middleware import ErrorMiddleware


def make_app() -> FastAPI:
    app = FastAPI()
    app.add_middleware(ErrorMiddleware)
    for router in routers:
        app.include_router(router)
    return app


__all__ = ("make_app",)
