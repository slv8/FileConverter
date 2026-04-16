from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Query

from app.api.public.v1.schemas.conversions import (
    GetConversionResponse,
    GetConversionsResponse,
    PublicConversion,
    StartConversionRequest,
    StartConversionResponse,
)
from app.context import app_context
from app.enum import ConversionStatus, FileOutputExtension
from app.types import ConversionId

router = APIRouter(prefix="/conversions")


@router.post(
    "/start",
    response_model=StartConversionResponse,
    description="Initiates a file conversion using file ID and target extension. Returns a conversion object.",
)
async def start_conversion(
    start_conversion_request: StartConversionRequest,
) -> StartConversionResponse:
    conversion = await app_context.conversion_service.start_conversion(
        file_id=start_conversion_request.file_id,
        file_extension=start_conversion_request.extension,
    )
    return StartConversionResponse(data=PublicConversion.from_conversion(conversion=conversion))


@router.get(
    "/{conversion_id}",
    response_model=GetConversionResponse,
    description="Retrieve the information of a specific conversion by its ID.",
)
async def get_conversion(conversion_id: ConversionId) -> GetConversionResponse:
    conversion = await app_context.conversion_repo.get_by_id(instance_id=conversion_id)
    if not conversion:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return GetConversionResponse(data=PublicConversion.from_conversion(conversion=conversion))


@router.get(
    "/",
    response_model=GetConversionsResponse,
    description="Retrieve a list of all file conversions with their current information.",
)
async def get_conversions(
    status: ConversionStatus | None = Query(default=None),
    extension: FileOutputExtension | None = Query(default=None, alias="format"),
    limit: int = Query(default=100, gt=0, le=1000),
    offset: int = Query(default=0, ge=0),
) -> GetConversionsResponse:
    conversions = await app_context.conversion_repo.get_all(
        status=status,
        extension=extension,
        limit=limit,
        offset=offset,
    )
    return GetConversionsResponse.from_conversions(conversions=conversions)
