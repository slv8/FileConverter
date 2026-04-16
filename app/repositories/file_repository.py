from typing import Any

from sqlalchemy import Row

from app.domain.entities.file import File
from app.repositories.base_repository import BaseRepository
from app.storage.db.tables import FileModel
from app.types import FileId


class FileRepository(BaseRepository[File, FileId]):
    @property
    def model(self) -> type[FileModel]:
        return FileModel

    def to_dict(self, instance: File) -> dict[str, Any]:
        return instance.model_dump(exclude_none=True)

    def to_entity(self, row: Row) -> File:
        return File(**row._mapping)
