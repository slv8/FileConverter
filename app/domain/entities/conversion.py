import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from app.enum import ConversionStatus, FileOutputExtension
from app.types import ConversionId, FileId


class Conversion(BaseModel):
    id: ConversionId = Field(default_factory=uuid.uuid4)

    status: ConversionStatus = ConversionStatus.PENDING
    progress: int = 0
    extension: FileOutputExtension

    original_file_id: FileId
    converted_file_id: FileId | None = None

    started_at: datetime | None = None
    completed_at: datetime | None = None
