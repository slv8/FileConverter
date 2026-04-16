from typing import Self

from pydantic import Field

from app.api.models import PublicBaseModel, ResponseWithTimestamp
from app.domain.entities.file import File
from app.types import FileId


class UploadFileResponseData(PublicBaseModel):
    id: FileId = Field(description="Unique identifier of the file")


class UploadFileResponse(ResponseWithTimestamp):
    data: UploadFileResponseData

    @classmethod
    def from_file(cls, file: File) -> Self:
        return cls(data=UploadFileResponseData(id=file.id))
