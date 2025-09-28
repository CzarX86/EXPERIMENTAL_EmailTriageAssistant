from __future__ import annotations

import logging

import typer

from src.lib.json_logging import configure_json_logging

app = typer.Typer(add_completion=False, no_args_is_help=True)


@app.callback()
def _init_logging(verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable DEBUG logs")):
    configure_json_logging(level="DEBUG" if verbose else None)


@app.command()
def hello(name: str = typer.Argument("world")):
    logging.getLogger(__name__).info("cli-hello", extra={"who": name})
    typer.echo(f"Hello, {name}")


if __name__ == "__main__":
    app()
