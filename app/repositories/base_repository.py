from abc import abstractmethod
from typing import Any, Generic, TypeVar

from sqlalchemy import CursorResult, Row, insert, select, update
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.sql.expression import Delete, Insert, Select, Update

from app.exceptions import RowNotFoundError
from app.storage.db import Base
from app.storage.db.db import get_db_connection

StmtType = Insert | Select | Update | Delete
T_ID = TypeVar("T_ID")
T = TypeVar("T")


class BaseRepository(Generic[T, T_ID]):
    def __init__(self, db_connection: AsyncConnection | None = None):
        self.db_connection = db_connection

    @property
    @abstractmethod
    def model(self) -> type[Base]:
        pass

    @abstractmethod
    def to_dict(self, instance: T) -> dict[str, Any]:
        pass

    @abstractmethod
    def to_entity(self, row: Row) -> T:
        pass

    async def execute_stmt(self, stmt: StmtType) -> CursorResult[Any]:
        if self.db_connection:
            return await self.db_connection.execute(stmt)

        async with get_db_connection() as db_conn:
            return await db_conn.execute(stmt)

    async def get_by_id(self, instance_id: T_ID) -> T | None:
        stmt = select(self.model).where(self.model.id == instance_id)  # type: ignore
        result = await self.execute_stmt(stmt)
        row = result.fetchone()
        return self.to_entity(row) if row else None

    async def insert(self, instance: T) -> T:
        instance_data = self.to_dict(instance)
        stmt = insert(self.model).values(instance_data).returning(self.model)
        result = await self.execute_stmt(stmt)
        row = result.fetchone()
        if not row:
            raise RowNotFoundError
        return self.to_entity(row)

    async def update_by_id(self, instance_id: T_ID, data: dict[str, Any]) -> T:
        stmt = (
            update(self.model).where(self.model.id == instance_id).values(**data).returning(self.model)  # type: ignore
        )
        result = await self.execute_stmt(stmt)
        row = result.fetchone()
        if not row:
            raise RowNotFoundError
        return self.to_entity(row)
