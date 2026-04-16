import logging
from http import HTTPStatus

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import JSONResponse

from app.exceptions import ClientError
from settings import STAGING_MODE

logger = logging.getLogger(__name__)


class ErrorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        try:
            response = await call_next(request)
        except ClientError as err:
            logger.debug("Client error: `%s: %s`", err.__class__.__name__, str(err))
            response = JSONResponse(
                status_code=HTTPStatus.BAD_REQUEST, content={"detail": str(err) if STAGING_MODE else "Bad request"}
            )
        except Exception as err:
            logger.exception("Internal server error:")
            response = JSONResponse(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                content={"detail": str(err) if STAGING_MODE else "Internal server error"},
            )
        return response
