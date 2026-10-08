def _table(header: list, rows: list) -> list:
    lines = ["| " + " | ".join(header) + " |", "|" + "|".join("---" for _ in header) + "|"]
    lines += ["| " + " | ".join(str(c) for c in row) + " |" for row in rows]
    return lines


def _list(items: list) -> list:
    return [f"- {i}" for i in items] if items else ["None"]


def render_report(inventory: dict) -> str:
    """Markdown report for a scan inventory (see docs/SCHEMA.md)."""
    files = inventory["files"]
    graph = inventory["graph"]
    by_path = {f["path"]: f for f in files}
    in_cycle = {p for cycle in graph["cycles"] for p in cycle}
    kinds: dict = {}
    for f in files:
        kinds[f["kind"]] = kinds.get(f["kind"], 0) + 1
    readers: dict = {}
    writers: dict = {}
    spelling: dict = {}  # lower-case name -> first spelling in path order
    for f in files:
        for table, mode in f["tables"].items():
            name = spelling.setdefault(table.lower(), table)
            (writers if mode == "write" else readers).setdefault(name, []).append(f["path"])
    tables = sorted(set(readers) | set(writers))
    unresolved = [f for f in files if f["unresolved_runs"]]

    out = ["# LumiPort report", "", "## Summary", ""]
    out += _list(
        [
            "Files: " + (", ".join(f"{n} .{k}" for k, n in sorted(kinds.items())) or "0"),
            f"Total loc: {sum(f['metrics']['loc'] for f in files)}",
            f"Units: {sum(len(f['units']) for f in files)}",
            f"Tables: {len(tables)}",
            f"Cycles: {len(graph['cycles'])}",
            f"Missing targets: {len(graph['missing'])}",
            f"Unresolved dynamic calls: {sum(f['unresolved_runs'] for f in files)}",
        ]
    )
    out += ["", "## Migration order", ""]
    if graph["order"]:
        for n, step in enumerate(graph["order"], 1):
            rows = sorted(
                ((p, by_path[p]["kind"], by_path[p]["metrics"]["score"], "yes" if p in in_cycle else "") for p in step),
                key=lambda r: (-r[2], r[0]),
            )
            out += [f"### Step {n}", ""] + _table(["Path", "Kind", "Score", "In cycle"], rows) + [""]
        out.pop()
    else:
        out.append("None")
    out += ["", "## Cycles", ""] + _list([" -> ".join(c) for c in graph["cycles"]])
    out += ["", "## Missing targets", ""] + _list([f"{src}: {dst}" for src, dst in graph["missing"]])
    out += ["", "## Unresolved dynamic calls", ""]
    out += _list([f"{f['path']}: {f['unresolved_runs']}" for f in unresolved])
    out += ["", "## Tables", ""]
    if tables:
        rows = [(t, ", ".join(readers.get(t, [])) or "-", ", ".join(writers.get(t, [])) or "-") for t in tables]
        out += _table(["Table", "Readers", "Writers"], rows)
    else:
        out.append("None")
    out += ["", "## Files", ""]
    if files:
        m = [(f["path"], *(f["metrics"][k] for k in ("loc", "blocks", "branches", "fan_in", "fan_out", "score"))) for f in files]
        out += _table(["Path", "loc", "blocks", "branches", "fan_in", "fan_out", "score"], m)
    else:
        out.append("None")
    out += [
        "",
        "## How the score is computed",
        "",
        "`score = loc + 2*(branches + blocks) + 5*(fan_in + fan_out)`",
        "",
        "- `loc`: lines with code after comments and strings are stripped.",
        "- `blocks`: `END` keywords (not `END-KEY`, `END-ERROR` and similar).",
        "- `branches`: `IF` keywords plus `WHEN` keywords.",
        "- `fan_in` / `fan_out`: distinct other files on incoming / outgoing graph edges (RUN calls and includes).",
        "",
    ]
    return "\n".join(out)
