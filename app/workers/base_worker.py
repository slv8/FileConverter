import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Any, Self

logger = logging.getLogger(__name__)


class BaseWorker(ABC):
    name: str

    _registry = {}

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        cls._registry[cls.name] = cls

    def __init__(self, stop_event: asyncio.Event, sleep_time: float = 0.5, shutdown_timeout: int = 5):
        self.stop_event = stop_event
        self.shutdown_timeout = shutdown_timeout
        self.sleep_time = sleep_time
        self._task: asyncio.Task | None = None

    @classmethod
    def get_worker_cls(cls, name: str) -> type[Self] | None:
        return cls._registry.get(name)

    async def start(self) -> None:
        logger.info("Starting worker `%s`...", self.name)
        self._task = asyncio.create_task(self._run_loop())

    async def stop(self) -> None:
        logger.info("Stopping worker `%s`...", self.name)
        if not self._task:
            return

        try:
            await asyncio.wait_for(self._task, timeout=self.shutdown_timeout)
        except asyncio.TimeoutError:
            pass

    async def _run_loop(self) -> None:
        while not self.stop_event.is_set():
            await self._run_main_logic()
            await asyncio.sleep(self.sleep_time)

    @abstractmethod
    async def _run_main_logic(self) -> Any:
        pass
