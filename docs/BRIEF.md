# Brief: step 7, Markdown report

**Goal:** `lumiport.report.render_report(inventory: dict) -> str` turns the scan JSON into a Markdown report, and `lumiport scan <dir> --report FILE.md` writes it. This finishes the last v1 scope item.

**Why now:** the inventory, graph and metrics are complete and pinned. The report only formats data that already exists.

## Steps
1. `src/lumiport/report.py`, a pure function of the inventory dict. Sections, in this order:
   - **Summary:** files per kind, total loc, units, tables, cycles, missing targets, total unresolved RUNs.
   - **Migration order:** one table per step with path, kind and score, sorted by score (highest first) then path. Mark files that are in a cycle.
   - **Cycles**, **Missing targets** and **Unresolved dynamic calls**: one line each per file, or "None".
   - **Tables:** one row per table with its readers and its writers.
   - **Files:** one row per file with loc, blocks, branches, fan_in, fan_out and score.
   - **How the score is computed:** the formula and what each input counts, taken from SCHEMA.md.
2. `cli.py`: add `--report FILE`. It works alongside `--out`, and stdout JSON stays the same when neither option is given.
3. `samples/expected-report.md`: generate it from `samples/expected.json`, then check every number in it against `expected.json` by hand. In Result, list the summary numbers and how you checked them.
4. `tests/test_report.py`: `render_report(expected.json) == expected-report.md`. Add an inline test that an empty inventory renders "None" sections without crashing. Add a CLI test that `--report` writes the file.

## Acceptance check
`.venv/bin/pytest -q`: all pass. `.venv/bin/lumiport scan samples/app --report /tmp/r.md && diff /tmp/r.md samples/expected-report.md` exits 0.

## Constraints
- Standard library only. Plain GitHub Markdown, no HTML. Change no other modules, `expected.json` or `SCHEMA.md`.

## Out of scope
- Graph diagrams (mermaid/dot), HTML output, README/usage docs (the next brief).

## Result

Done. `.venv/bin/pytest -q`: 66 passed. `lumiport scan samples/app --report r.md && diff r.md samples/expected-report.md`: exit 0.

Summary numbers: 11 files (7 .p, 3 .i, 1 .cls), loc 77, units 7, tables 4, cycles 1, missing 0, unresolved 1. Checked by recomputing from `expected.json` with a separate script (loc sum, units, distinct tables, readers/writers per table, unresolved) and units against the sample source by eye.

Decide: with `--report` alone, JSON still prints to stdout (only `--out` redirects it). A table both read and written by one file shows that file under Writers only (write wins, per SCHEMA).
