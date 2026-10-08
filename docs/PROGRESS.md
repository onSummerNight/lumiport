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
- Step 5: `graph.build_graph` (edges, missing, cycles, order), golden + 6 graph tests (2026-10-08)
- Step 6: `metrics.file_metrics`, per-file `metrics` + score in scan output, 63 tests pass (2026-10-08)
- Step 7: `report.render_report`, `scan --report FILE`, `samples/expected-report.md`, 66 tests pass (2026-10-08)

## Now
- Step 7 done, awaiting manager review (`docs/BRIEF.md` Result)

## Next
- README/usage docs

## Later
- Claude mode: draft Python for one procedure from its inventory facts
- Decide deadline, public/portfolio repo, license
- Extractor gaps: `PROCEDURE x PRIVATE:` not matched; `{1}` include args counted as includes; `FUNCTION ... IN handle` counted as unit; table names differing only in case are separate keys
- graph.py builds adjacency in O(files × edges): fine for samples, slow on large repos

## Blockers
- None
