from typing import Self

from pydantic import Field, HttpUrl

from app.api.models import PublicBaseModel, ResponseWithTimestamp
from app.domain.entities import Conversion
from app.enum import ConversionStatus, FileOutputExtension
from app.types import ConversionId, FileId
from settings import SITE_URL


class PublicConversion(PublicBaseModel):
    id: ConversionId = Field(description="Unique identifier of the conversion")
    status: ConversionStatus = Field(description="Current status of the conversion process")
    progress: int = Field(description="Progress percentage (0 to 100) of the conversion")
    original_file_url: HttpUrl = Field(description="Public URL to access the original uploaded file")
    converted_file_url: HttpUrl | None = Field(
        description="Public URL to access the converted file (if available)", default=None
    )

    @classmethod
    def from_conversion(cls, conversion: Conversion) -> Self:
        return cls(
            id=conversion.id,
            status=conversion.status,
            progress=conversion.progress,
            original_file_url=cls._build_file_url(conversion.original_file_id),
            converted_file_url=(
                cls._build_file_url(conversion.converted_file_id) if conversion.converted_file_id else None
            ),
        )

    @staticmethod
    def _build_file_url(file_id: FileId) -> str:
        return f"{SITE_URL}/api/v1/files/{file_id}/download/"


class GetConversionsResponse(ResponseWithTimestamp):
    data: list[PublicConversion]

    @classmethod
    def from_conversions(cls, conversions: list[Conversion]) -> Self:
        return cls(data=[PublicConversion.from_conversion(conversion=conversion) for conversion in conversions])


class GetConversionResponse(ResponseWithTimestamp):
    data: PublicConversion


class StartConversionResponse(ResponseWithTimestamp):
    data: PublicConversion


class StartConversionRequest(PublicBaseModel):
    file_id: FileId = Field(description="Unique identifier of the file")
    extension: FileOutputExtension = Field(description="Target file extension")
