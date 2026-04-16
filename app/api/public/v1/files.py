from http import HTTPStatus

from fastapi import APIRouter, HTTPException, UploadFile
from fastapi.responses import FileResponse

from app.api.public.v1.schemas.files import UploadFileResponse
from app.context import app_context
from app.types import FileId

router = APIRouter(prefix="/files")


@router.post(
    "/upload",
    response_model=UploadFileResponse,
    description="Upload a file for conversion. Returns a file ID that can be used to start a conversion later.",
)
async def upload_file(file: UploadFile) -> UploadFileResponse:
    uploaded_file = await app_context.file_service.upload_file(file_to_upload=file)
    return UploadFileResponse.from_file(file=uploaded_file)


@router.get(
    "/{file_id}/download",
    response_class=FileResponse,
    responses={
        HTTPStatus.OK: {
            "content": {"application/octet-stream": {}},
        }
    },
    description="Download the converted or original file by its file ID.",
)
async def download_file(file_id: FileId) -> FileResponse:
    # todo: not production ready, download from cloud storage directly
    file = await app_context.file_repo.get_by_id(instance_id=file_id)
    if not file:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return FileResponse(path=file.storage_path, filename=file.name, media_type="application/octet-stream")
