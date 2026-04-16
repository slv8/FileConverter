import uuid
from pathlib import Path

from pydantic import BaseModel, Field

from app.types import FileId
from settings import FILES_STORAGE_PATH


class File(BaseModel):
    id: FileId = Field(default_factory=uuid.uuid4)

    name: str = Field(max_length=100)

    @property
    def extension(self) -> str:
        return Path(self.name).suffix.lstrip(".")

    @property
    def storage_path(self) -> Path:
        return FILES_STORAGE_PATH / f"{self.id}.{self.extension}"

    @property
    def stem(self) -> str:
        return Path(self.name).stem
