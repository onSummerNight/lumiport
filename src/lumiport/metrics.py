import re

_END = re.compile(r"(?<![\w-])END(?![\w-])", re.IGNORECASE)
_BRANCH = re.compile(r"(?<![\w-])(?:IF|WHEN)(?![\w-])", re.IGNORECASE)


def file_metrics(code: str) -> dict:
    """loc, blocks and branches of comment/string-stripped code (see docs/SCHEMA.md)."""
    return {
        "loc": sum(1 for line in code.splitlines() if line.strip()),
        "blocks": len(_END.findall(code)),
        "branches": len(_BRANCH.findall(code)),
    }
