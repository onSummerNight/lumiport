import re

_NAME = r"[A-Za-z_][\w\-]*"
_B = r"(?<![\w-])"  # keyword start: not inside DYNAMIC-FUNCTION and the like

_PROC = re.compile(_B + r"(END\s+)?PROCEDURE\s+(" + _NAME + r")\s*:", re.I)
_FUNC = re.compile(_B + r"(END\s+)?FUNCTION\s+(" + _NAME + r")", re.I)
_METHOD = re.compile(_B + r"(END\s+)?METHOD(?![\w-])", re.I)
_INCLUDE = re.compile(r"\{\s*([^\s{}]+)")
_RUN = re.compile(_B + r"RUN\s+(?:(VALUE\s*\()|([\w\-./]+\.p)\b)", re.I)


def extract_calls(code: str) -> dict:
    """Units, includes and RUN calls of one file; `code` is already stripped."""
    units = set()
    for m in _PROC.finditer(code):
        if not m.group(1):
            units.add((m.group(2), "procedure"))
    for m in _FUNC.finditer(code):
        if m.group(1):
            continue
        header = re.split(r"[:.]", code[m.end() :], maxsplit=1)[0]
        if not re.search(r"(?<![\w-])FORWARD(?![\w-])", header, re.I):
            units.add((m.group(2), "function"))
    for m in _METHOD.finditer(code):
        if m.group(1):
            continue
        paren = code.find("(", m.end())
        tokens = code[m.end() : paren].split() if paren >= 0 else []
        if len(tokens) >= 2 and re.fullmatch(_NAME, tokens[-1]):
            units.add((tokens[-1], "method"))

    includes = {
        m.group(1) for m in _INCLUDE.finditer(code) if not m.group(1).startswith("&")
    }

    runs = set()
    unresolved = 0
    for m in _RUN.finditer(code):
        if m.group(1):
            unresolved += 1
        else:
            runs.add(m.group(2))

    return {
        "units": [{"name": n, "type": t} for n, t in sorted(units)],
        "includes": sorted(includes),
        "runs": sorted(runs),
        "unresolved_runs": unresolved,
    }
