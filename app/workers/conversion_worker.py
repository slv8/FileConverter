import asyncio
import logging
from typing import Any

from app.context import app_context
from app.domain.entities import Conversion
from app.domain.entities.file import File
from app.enum import ConversionStatus
from app.exceptions import NotFoundFileError
from app.unit_of_work import UnitOfWork
from app.utils import utcnow
from app.workers.base_worker import BaseWorker
from settings import CONVERSION_TIMEOUT

logger = logging.getLogger(__name__)


SLEEP_TIME = 0.1


class ConversionWorker(BaseWorker):
    name = "conversion"

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, sleep_time=SLEEP_TIME, **kwargs)

    async def _run_main_logic(self) -> None:
        async with UnitOfWork() as uow:
            conversion = await uow.conversion_service.claim_conversion_for_processing()
            if not conversion:
                return None

        original_file = await app_context.file_repo.get_by_id(instance_id=conversion.original_file_id)
        if not original_file:
            raise NotFoundFileError(f"File {conversion.original_file_id} not found")

        output_file = File(name=f"{original_file.stem}.{conversion.extension}")
        try:
            await asyncio.wait_for(
                app_context.conversion_service.run_conversion(
                    original_file=original_file,
                    output_file=output_file,
                    conversion=conversion,
                ),
                timeout=CONVERSION_TIMEOUT,
            )
        except Exception:
            logger.exception("Error while running conversion `%s`:", conversion.id)
            await self._handle_conversion_failed(conversion=conversion)
        else:
            await self._handle_conversion_success(conversion=conversion, output_file=output_file)

    async def _handle_conversion_failed(self, conversion: Conversion) -> Conversion:
        return await app_context.conversion_repo.update_by_id(
            instance_id=conversion.id,
            data={"status": ConversionStatus.FAILED, "completed_at": utcnow()},
        )

    async def _handle_conversion_success(self, conversion: Conversion, output_file: File) -> None:
        async with UnitOfWork() as uow:
            await uow.file_repo.insert(instance=output_file)
            await uow.conversion_repo.update_by_id(
                instance_id=conversion.id,
                data={
                    "status": ConversionStatus.COMPLETED,
                    "completed_at": utcnow(),
                    "converted_file_id": output_file.id,
                },
            )
