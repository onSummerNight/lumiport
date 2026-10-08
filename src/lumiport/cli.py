import json
from pathlib import Path
from typing import Optional

import typer

from lumiport.scanner import scan_dir

app = typer.Typer(help="OpenEdge ABL inventory and Python migration assistant.")


@app.callback()
def main() -> None:
    """OpenEdge ABL inventory and Python migration assistant."""


@app.command()
def scan(
    directory: Path,
    out: Optional[Path] = typer.Option(None, "--out", help="Write JSON to FILE."),
) -> None:
    """Scan DIRECTORY for ABL sources."""
    if not directory.is_dir():
        typer.echo(f"error: not a directory: {directory}", err=True)
        raise typer.Exit(code=2)
    text = json.dumps(scan_dir(directory), indent=2)
    if out:
        out.write_text(text + "\n")
    else:
        typer.echo(text)
