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
- Step 8: `README.md` (install, usage, limitations, clean room), verified in a fresh clone (2026-10-08)
- Step 9: tested on Python 3.10 and 3.14 (69 passed each); `PROCEDURE x PRIVATE:` recognised (2026-10-08)
- Step 10: include args, `FUNCTION ... IN`, case-insensitive tables (per file and in report), 76 tests pass (2026-10-08)
- Step 11: linear-time adjacency in `build_graph`, 5,000-file scale test, 77 tests pass (2026-10-08)
- Step 12: MIT `LICENSE`, pre-public audit clean (secrets, IPs, hosts, emails, .env), tag v0.1.0 (2026-10-08)
- **v1 done:** `lumiport scan <dir> [--out] [--report]` gives inventory, graph, cycles, migration order, complexity score and Markdown report; 77 tests on Python 3.10 and 3.14

## Now
- Awaiting user: push, tag push, make public

## Next
- Nothing queued

## Later
- Claude mode: draft Python for one procedure from its inventory facts

## Blockers
- None
