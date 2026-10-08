# Progress

## Done
- Scaffold created
- Context agreed and LOCKED 2026-10-08
- Repo on GitHub (private): onSummerNight/lumiport
- Step 1: project skeleton, `lumiport scan` stub, 2 smoke tests pass (2026-10-08)
- Step 2: 11-file sample app, `samples/expected.json`, `docs/SCHEMA.md`, xfail golden test (2026-10-08)
- Step 3: `tokenizer.strip_code` + 13 tests (2026-10-08)
- Step 4a: `extract.extract_calls` (units, includes, runs) + tests (2026-10-08)
- Step 4b: `extract.extract_tables` (read/write, buffers) + 17 tests (2026-10-08)
- Step 4c: `scanner.scan_dir`, `lumiport scan [--out]` JSON, golden test green (2026-10-08)

## Now
- Awaiting brief for step 5 (dependency graph, cycles, migration order)

## Next
- Graph + cycles + migration order, complexity score, Markdown report

## Later
- Claude mode: draft Python for one procedure from its inventory facts
- Decide deadline, public/portfolio repo, license
- Extractor gaps: `PROCEDURE x PRIVATE:` not matched; `{1}` include args counted as includes; `FUNCTION ... IN handle` counted as unit; table names differing only in case are separate keys

## Blockers
- None
