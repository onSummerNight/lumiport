# Decisions

Append-only. Date, decision, why, alternatives rejected.


## 2026-10-08: v1 scope locked
- Decision: tokenizer-level scanner (no grammar), dynamic RUN flagged as unresolved, golden JSON test as success check, Python 3.10+ / Typer / pytest only. Claude mode moved to Later.
- Why: a verifiable first version with no API dependency or secrets; the inventory is useful by itself.
- Rejected: full ABL grammar (too big for v1); Claude mode in v1 (output not testable, adds secrets handling).

## 2026-10-08: scanner entry point and internal RUN
- Decision: golden test calls `lumiport.scanner.scan_dir(Path) -> dict`. `RUN name` without `.p` is an internal call: not in `runs`, not counted as unresolved.
- Why: a pure function is testable without the CLI; internal calls are not file dependencies.
- Rejected: testing via CLI JSON output only (CLI option not built yet); counting internal RUNs as unresolved (would inflate the metric).
