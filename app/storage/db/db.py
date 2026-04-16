from contextlib import asynccontextmanager
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncConnection, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from settings import DB_URI


class Base(AsyncAttrs, DeclarativeBase):
    pass  # noqa: WPS604


engine = create_async_engine(url=DB_URI)


@asynccontextmanager
async def get_db_connection() -> AsyncIterator[AsyncConnection]:
    async with engine.begin() as db_connection:
        yield db_connection
