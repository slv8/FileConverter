from types import TracebackType
from typing import Self

from app.domain.services.conversion_service import ConversionService
from app.domain.services.file_service import FileService
from app.repositories.conversion_repository import ConversionRepository
from app.repositories.file_repository import FileRepository
from app.storage.db.db import engine


class UnitOfWork:
    def __init__(self):
        self.db_conn = None
        self.db_transaction = None

    async def __aenter__(self) -> Self:
        self.db_conn = await engine.connect()
        self.db_transaction = await self.db_conn.begin()
        self.conversion_repo = ConversionRepository(db_connection=self.db_conn)
        self.file_repo = FileRepository(db_connection=self.db_conn)
        self.conversion_service = ConversionService(conversion_repo=self.conversion_repo, file_repo=self.file_repo)
        self.file_service = FileService(file_repo=self.file_repo)
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException,
        exc_tb: TracebackType,
    ) -> None:
        if self.db_transaction:
            if exc_type:
                await self.db_transaction.rollback()
            else:
                await self.db_transaction.commit()
        if self.db_conn:
            await self.db_conn.close()
