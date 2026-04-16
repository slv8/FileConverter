from typing import Any

import click

from app.commands import run


@click.command(cls=click.CommandCollection, sources=[run])
def cli():
    pass


if __name__ == "__main__":
    cli()
