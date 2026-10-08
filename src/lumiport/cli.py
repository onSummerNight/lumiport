from pathlib import Path

import typer

app = typer.Typer(help="OpenEdge ABL inventory and Python migration assistant.")


@app.callback()
def main() -> None:
    """OpenEdge ABL inventory and Python migration assistant."""


@app.command()
def scan(directory: Path) -> None:
    """Scan DIRECTORY for ABL sources."""
    if not directory.is_dir():
        typer.echo(f"error: not a directory: {directory}", err=True)
        raise typer.Exit(code=2)
    typer.echo(f"scan: {directory} (not implemented)")
