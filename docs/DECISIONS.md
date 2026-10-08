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

## 2026-10-08: dependency graph and migration order shape
- Decision: edges are RUN calls and includes (both are dependencies to port first). Targets resolve by exact relative path (case-insensitive), else by unique basename, else go to `missing`. Cycles (strongly connected components) migrate together. `order` is a list of steps (levels): a file's step comes after all of its dependencies' steps; each step is sorted.
- Why: levels are deterministic with no tie-break rule, and they show what can be ported in parallel. Includes become shared Python modules, so they belong in the order.
- Rejected: one flat topological list (needs an arbitrary tie-break); RUN-only edges (would hide the coupling that includes create).

## 2026-10-08: graph details and complexity score formula
- Decision: basename resolution uses the target's last path segment; a self-call stays in `edges` and `cycles`. Per-file `metrics`: `loc` (lines with code after stripping), `blocks` (`END` keywords), `branches` (`IF` + `WHEN`), `fan_in`/`fan_out` (distinct other files on graph edges). `score = loc + 2*(branches + blocks) + 5*(fan_in + fan_out)`.
- Why: every input is countable by hand on the samples, so the golden test can pin it; coupling is weighted more than size because it decides migration risk.
- Rejected: cyclomatic complexity per unit (needs real parsing); unweighted sum (lets long, flat files dominate).
