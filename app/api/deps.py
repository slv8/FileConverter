from http import HTTPStatus

from fastapi import HTTPException, Request

from app.types import AccountId


async def require_auth(request: Request) -> AccountId:
    """
    Dependency that ensures the request is authenticated.

    This is just a demonstration of possible authorization logic and is not secure
    or sufficient for production. In a real application, should be replaced with proper
    authentication mechanism.
    """
    account_id = request.query_params.get("account_id")
    if account_id is None:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Forbidden")
    return int(account_id)
