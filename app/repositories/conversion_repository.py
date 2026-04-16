from typing import Any

from sqlalchemy import Row, and_, select

from app.domain.entities.conversion import Conversion
from app.enum import ConversionStatus, FileOutputExtension
from app.repositories.base_repository import BaseRepository
from app.storage.db.tables.conversion import ConversionModel
from app.types import FileId


class ConversionRepository(BaseRepository):
    @property
    def model(self) -> type[ConversionModel]:
        return ConversionModel

    def to_dict(self, instance: Conversion) -> dict[str, Any]:
        return instance.model_dump(exclude_none=True)

    def to_entity(self, row: Row) -> Conversion:
        return Conversion(**row._mapping)

    async def get_all(
        self,
        status: ConversionStatus | None = None,
        extension: FileOutputExtension | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Conversion]:
        stmt = select(self.model).offset(offset).limit(limit).order_by(self.model.created_at)
        if status:
            stmt = stmt.where(self.model.status == status)
        if extension:
            stmt = stmt.where(self.model.extension == extension)

        result = await self.execute_stmt(stmt)
        return [self.to_entity(row) for row in result]

    async def get_by_original_file_id_and_extension(
        self,
        original_file_id: FileId,
        extension: FileOutputExtension,
    ) -> Conversion | None:
        stmt = select(self.model).where(
            and_(
                self.model.original_file_id == original_file_id,
                self.model.extension == extension,
            )
        )

        result = await self.execute_stmt(stmt)
        row = result.fetchone()
        return self.to_entity(row) if row else None

    async def get_next_pending_conversion(self) -> Conversion | None:
        stmt = (
            select(self.model)
            .where(self.model.status == ConversionStatus.PENDING)
            .order_by(self.model.created_at)
            .limit(1)
            .with_for_update(skip_locked=True)
        )

        result = await self.execute_stmt(stmt)
        row = result.fetchone()
        return self.to_entity(row) if row else None
