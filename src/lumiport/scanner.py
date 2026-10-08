from pathlib import Path

from lumiport.extract import extract_calls, extract_tables
from lumiport.tokenizer import strip_code

_KINDS = {".p", ".i", ".cls"}


def _read(path: Path) -> str:
    data = path.read_bytes()
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return data.decode("latin-1")


def scan_dir(directory: Path) -> dict:
    """Inventory of every .p/.i/.cls file under `directory` (see docs/SCHEMA.md)."""
    found = sorted(
        (p.relative_to(directory).as_posix(), p)
        for p in directory.rglob("*")
        if p.is_file() and p.suffix.lower() in _KINDS
    )
    files = []
    for rel, path in found:
        code = strip_code(_read(path))
        calls = extract_calls(code)
        files.append(
            {
                "path": rel,
                "kind": path.suffix.lower().lstrip("."),
                **calls,
                "tables": extract_tables(code),
            }
        )
    return {"files": files}
