import asyncio
import logging

from app.domain.entities import Conversion
from app.domain.entities.file import File
from app.enum import ConversionStatus, FileInputExtension, FileOutputExtension, UnfinishedConversionStatuses
from app.exceptions import ConversionFailedError, InvalidFileExtensionError, NotFoundFileError
from app.repositories.conversion_repository import ConversionRepository
from app.repositories.file_repository import FileRepository
from app.types import FileId
from app.utils import utcnow
from settings import CONVERSION_SCRIPT_PATH, CONVERSION_SCRIPT_SUCCESS_RETURN_CODE

logger = logging.getLogger(__name__)


class ConversionService:
    def __init__(self, conversion_repo: ConversionRepository, file_repo: FileRepository):
        self.conversion_repo = conversion_repo
        self.file_repo = file_repo

    async def start_conversion(self, file_id: FileId, file_extension: FileOutputExtension) -> Conversion:
        file = await self.file_repo.get_by_id(instance_id=file_id)
        if not file:
            raise NotFoundFileError(f"File with id `{file_id}` is not found")

        if file.extension not in FileInputExtension:  # just in case
            raise InvalidFileExtensionError(f"Wrong file extension of file {file.extension}")

        conversion = await self.conversion_repo.get_by_original_file_id_and_extension(
            original_file_id=file.id,
            extension=file_extension,
        )
        if conversion and conversion.status in UnfinishedConversionStatuses:
            return conversion

        return await self.conversion_repo.insert(
            instance=Conversion(
                original_file_id=file.id,
                extension=file_extension,
            )
        )

    async def run_conversion(self, original_file: File, output_file: File, conversion: Conversion) -> None:
        logger.info("Starting conversion %s...", conversion.id)

        process = await asyncio.create_subprocess_exec(
            CONVERSION_SCRIPT_PATH,
            original_file.storage_path,
            output_file.storage_path,
            conversion.extension,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
        )

        async for line in process.stdout:
            decoded = line.decode().strip()
            if decoded.startswith("progress:"):
                try:
                    progress = int(decoded.split(":")[1])
                except Exception:
                    logger.exception("Error while parsing progress value:")
                    continue

                await self.conversion_repo.update_by_id(instance_id=conversion.id, data={"progress": progress})

        await process.wait()
        logger.info("Conversion %s finished", conversion.id)

        if process.returncode != CONVERSION_SCRIPT_SUCCESS_RETURN_CODE:
            raise ConversionFailedError(f"Conversion finished with code `{process.returncode}`")

    async def claim_conversion_for_processing(self) -> Conversion | None:
        conversion = await self.conversion_repo.get_next_pending_conversion()
        if not conversion:
            return None

        return await self.conversion_repo.update_by_id(
            instance_id=conversion.id,
            data={"status": ConversionStatus.IN_PROGRESS, "started_at": utcnow()},
        )
