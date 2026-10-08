from pathlib import Path

from lumiport.extract import extract_calls, extract_tables
from lumiport.graph import build_graph
from lumiport.metrics import file_metrics
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
    metrics = {}
    for rel, path in found:
        code = strip_code(_read(path))
        calls = extract_calls(code)
        metrics[rel] = file_metrics(code)
        files.append(
            {
                "path": rel,
                "kind": path.suffix.lower().lstrip("."),
                **calls,
                "tables": extract_tables(code),
            }
        )
    graph = build_graph(files)
    fan_in = {rel: set() for rel in metrics}
    fan_out = {rel: set() for rel in metrics}
    for src, dst, _ in graph["edges"]:
        if src != dst:
            fan_out[src].add(dst)
            fan_in[dst].add(src)
    for f in files:
        m = metrics[f["path"]]
        m["fan_in"] = len(fan_in[f["path"]])
        m["fan_out"] = len(fan_out[f["path"]])
        m["score"] = m["loc"] + 2 * (m["branches"] + m["blocks"]) + 5 * (m["fan_in"] + m["fan_out"])
        f["metrics"] = m
    return {"files": files, "graph": graph}
