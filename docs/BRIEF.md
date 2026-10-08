# Brief: step 4c, scan_dir + CLI JSON (golden test goes green)

**Goal:** `lumiport.scanner.scan_dir(Path) -> dict` produces the full inventory from `docs/SCHEMA.md`, and `lumiport scan <dir>` outputs it as JSON. The golden test passes for real.

**Why now:** this ties the tokenizer and both extractors together and meets the v1 success check for the inventory.

## Steps
1. `src/lumiport/scanner.py`: walk `<dir>` recursively for `.p`, `.i` and `.cls`, matching the extension case-insensitively, sorted by relative path with `/`. Decode each file as UTF-8, falling back to latin-1. Run `strip_code`, then `extract_calls` and `extract_tables`. Build `{"files": [...]}` with the field order `path, kind, units, includes, runs, unresolved_runs, tables`. `kind` is the lowercased extension.
2. `cli.py`: `scan <dir>` prints the JSON (indent 2) to stdout. `--out FILE` writes it to a file instead. Keep the exit-2 check for a directory that doesn't exist. Remove the "not implemented" text.
3. `tests/test_golden.py`: remove the `xfail` marker. Add a CLI test: `scan samples/app --out tmp.json` produces a file equal to `expected.json`.
4. Update `tests/test_cli.py` if the old stub output assertion breaks. Add one test that an empty directory gives `{"files": []}`.

## Acceptance check
`.venv/bin/pytest -q` → all passed, 0 xfailed. Also `.venv/bin/lumiport scan samples/app | python3 -c "import json,sys; assert json.load(sys.stdin)==json.load(open('samples/expected.json'))"` exits 0.

## Constraints
- Standard library + Typer only. Don't change `tokenizer.py`, `extract.py`, `expected.json` or `SCHEMA.md`. If the golden test fails because an extractor is wrong, stop and report it in Result rather than patching around it.

## Out of scope
- Dependency graph, cycles, migration order, complexity score, Markdown report (the next briefs), and `.w` files.

## Result
Done. `.venv/bin/pytest -q`: `51 passed in 0.04s` (0 xfailed).
`lumiport scan samples/app | python3 -c "...assert == expected.json"` exit=0.
Empty-dir test is the existing `test_scan_existing_dir`, now asserting `{"files": []}`. Nothing to decide.
