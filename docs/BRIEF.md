# Brief: step 2, synthetic sample app + golden expected.json

**Goal:** a hand-written ABL sample app in `samples/app/`, its expected inventory in `samples/expected.json`, and a golden test marked `xfail(strict=True)` until the scanner exists.

**Why now:** this fixes the output format and the success check before any scanner code is written.

## Steps
1. Write 8–12 synthetic files in `samples/app/` (`.p`, `.i`, `.cls`, generic retail-order theme). Make sure they cover: internal `PROCEDURE` and `FUNCTION`, a class `METHOD`, `{inc.i}` includes, `RUN x.p` calls with one cycle (a.p → b.p → a.p), one `RUN VALUE(...)`, `FOR EACH`/`FIND` (read), `CREATE`/`DELETE` (write), `DEFINE BUFFER b FOR t`, and nested `/* /* */ */` comments and strings that contain fake `RUN`/`FOR EACH` text, which must be ignored.
2. Write `samples/expected.json` by hand: `{"files": [...]}` sorted by path. Each file entry has `path` (relative to `samples/app`, using `/`), `kind` (`p|i|cls`), `units` (`[{"name","type":"procedure|function|method"}]`), `includes`, `runs` (resolved targets), `unresolved_runs` (count), and `tables` (`{name: "read"|"write"}`, where write wins and buffers resolve to their table). Every list is sorted.
3. Write `docs/SCHEMA.md` (about 20 lines), describing those fields and their rules.
4. `tests/test_golden.py`: run `scan` on `samples/app` with JSON output and compare it to `expected.json`. Mark it `xfail(strict=True, reason="scanner not built")`.

## Acceptance check
`.venv/bin/pytest -q` → 2 passed, 1 xfailed. You review `expected.json` against the sources by hand and describe in Result how you checked it.

## Constraints
- Clean room: invent every name. No real company, product or schema names.
- Don't change the CLI yet. The test may call a function that doesn't exist yet (that is the expected failure).

## Out of scope
- Graph, migration order and complexity score fields (a later brief adds them to the schema), the tokenizer, and any scanner code.

## Result
Done.
```
pytest -q: 2 passed, 1 xfailed in 0.02s
expected.json: 11 files, paths sorted, valid JSON
```
How checked: grepped every RUN / include / unit / FOR EACH / FIND / CREATE / DELETE / DEFINE BUFFER line in the sources and compared each to its entry by hand. No scanner output exists to compare against yet; please spot-check `expected.json` yourself.
Decide: (1) I chose the test entry point `lumiport.scanner.scan_dir(Path) -> dict`; the CLI JSON option comes later. (2) `RUN addLine` (internal, no `.p`) is ignored, not counted as unresolved; written into SCHEMA.md.
