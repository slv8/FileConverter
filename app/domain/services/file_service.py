from pathlib import Path

import aiofiles
from fastapi import UploadFile

from app.domain.entities.file import File
from app.enum import FileInputExtension
from app.exceptions import FileUploadError
from app.repositories.file_repository import FileRepository
from settings import FILES_UPLOAD_CHUNK_SIZE


class FileService:
    def __init__(self, file_repo: FileRepository):
        self.file_repo = file_repo

    async def upload_file(self, file_to_upload: UploadFile) -> File:
        if not self._can_upload_file(file=file_to_upload):
            raise FileUploadError(f"File {file_to_upload.filename} can't be uploaded")

        file = File(name=file_to_upload.filename)
        async with aiofiles.open(file.storage_path, "wb") as out_file:
            while chunk := await file_to_upload.read(FILES_UPLOAD_CHUNK_SIZE):
                await out_file.write(chunk)

        return await self.file_repo.insert(file)

    def _can_upload_file(self, file: UploadFile) -> bool:
        return bool(file.filename and Path(file.filename).suffix.lstrip(".") in FileInputExtension)
