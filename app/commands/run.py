import asyncio
import signal
from typing import Any

import click
import uvicorn

from app import app as app_to_run
from app.workers.base_worker import BaseWorker


@click.group()
def run() -> None:
    pass


@run.command("runserver", help="Run web server via uvicorn.")
@click.option("--host", default="0.0.0.0", type=str, help="Host")  # noqa: S104
@click.option("--port", default=8000, type=int, help="Port")
def run_server(host: str, port: int) -> None:
    uvicorn.run(app_to_run, host=host, port=port, log_config=None)


@run.command("runworker", help="Run worker.")
@click.argument("name", type=str, required=True)  # noqa: S104
def run_worker(name: str) -> None:
    worker_cls = BaseWorker.get_worker_cls(name=name)
    if not worker_cls:
        click.echo(f"Worker with name {name} not found")
        raise click.Abort()

    asyncio.run(_run_worker(worker_cls))


async def _run_worker(worker_cls: type[BaseWorker]) -> None:
    def _handle_stop_signal(*args: Any, **kwargs: Any):
        stop_event.set()

    stop_event = asyncio.Event()

    loop = asyncio.get_running_loop()
    loop.add_signal_handler(signal.SIGINT, _handle_stop_signal, signal.SIGTERM)
    loop.add_signal_handler(signal.SIGTERM, _handle_stop_signal, signal.SIGTERM)

    worker = worker_cls(stop_event=stop_event)
    try:
        await worker.start()
        await stop_event.wait()
    finally:
        stop_event.set()
        await worker.stop()
