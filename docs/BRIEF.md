# Brief: step 4a, extract units, includes and RUN calls

**Goal:** `lumiport.extract.extract_calls(code: str) -> dict`, which returns `units`, `includes`, `runs` and `unresolved_runs` for one file (input already passed through `strip_code`), following `docs/SCHEMA.md`.

**Why now:** this is the first half of the extractors. Tables and buffers come in 4b, then `scan_dir` + CLI in 4c.

## Steps
1. `src/lumiport/extract.py`. Keywords are case-insensitive; names keep their source case.
2. Units: `PROCEDURE name:` → procedure; `FUNCTION name` → function (skip `... FORWARD.` declarations); `METHOD <modifiers> <type> name(` → method. `END PROCEDURE/FUNCTION/METHOD` is never a unit.
3. Includes: `{name.i ...}`, using the first token inside the braces. Skip `{&NAME}` preprocessor references and `{}`.
4. RUN: `RUN x.p` (path allowed, e.g. `dir/x.p`) goes into `runs`. `RUN VALUE(` adds 1 to `unresolved_runs`. Any other `RUN name` is internal and ignored. Lists are sorted with no duplicates.
5. `tests/test_extract.py`: a test per sample file, parametrized, comparing those 4 fields to `samples/expected.json`. Add small inline tests for lower-case keywords, `FORWARD`, `{&X}`, and `RUN x.p PERSISTENT SET h`.

## Acceptance check
`.venv/bin/pytest -q`: all new tests pass, the existing 15 still pass, and the golden test stays xfailed.

## Constraints
- Standard library only (`re` is fine here, because the input is already stripped). Don't change `tokenizer.py`, `expected.json` or `SCHEMA.md`. If a sample disagrees with the schema, stop and report it in Result.

## Out of scope
- Tables and buffers, `scan_dir`, CLI output, graph and complexity, ABL keyword abbreviations (`PROC`, `FUNC`), `//` line comments.

## Result
Done.
```
pytest -q: 32 passed, 1 xfailed in 0.03s
(11 sample files match expected.json on units/includes/runs/unresolved_runs; 6 inline tests)
```
No sample disagreed with the schema. Known gaps left alone: `{1}` include-argument refs would count as includes; `FUNCTION ... IN handle.` is treated as a unit; `PROCEDURE x PRIVATE:` is not matched (colon must follow the name).
