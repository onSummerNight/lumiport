# Brief: step 5, dependency graph, cycles, migration order

**Goal:** `scan_dir` output gains a top-level `graph` with `edges`, `missing`, `cycles` and `order`, following the 2026-10-08 entry in `docs/DECISIONS.md`. The golden test covers it.

**Why now:** the inventory is done. Graph and order are the next v1 scope item, and the complexity score and report build on them.

## Steps
1. `docs/SCHEMA.md`: add `graph` with these fields:
   - `edges`: `[[from, to, "run"|"include"]]`, sorted.
   - `missing`: sorted `[[from, target]]` for targets that don't resolve.
   - `cycles`: each cycle's files sorted, cycles themselves sorted. Only components with more than one file, or a file that calls itself.
   - `order`: `[[paths...], ...]` steps.
2. `src/lumiport/graph.py`: `build_graph(files: list) -> dict`. Resolve each target by exact relative path (case-insensitive), else by unique basename, else put it in `missing`. Find strongly connected components iteratively (no recursion limit issues). Each step contains every component whose dependencies all sit in earlier steps.
3. `scanner.scan_dir` returns `{"files": [...], "graph": build_graph(files)}`.
4. Update `samples/expected.json` by hand. My hand computation, for you to confirm or contradict:
   - Steps: 1 = common.i, consts.i, order-purge.p, price-calc.p, util.i; 2 = a.p, b.p, order-create.p, ordermgr.cls, report.p; 3 = main.p.
   - One cycle: [a.p, b.p]. No missing targets.
5. `tests/test_graph.py`: inline tests for a self-call, a missing target, a diamond, basename resolution, an ambiguous basename (goes to `missing`), and a 3-file cycle.

## Acceptance check
`.venv/bin/pytest -q`: all pass, 0 xfailed. The CLI-vs-`expected.json` check from step 4c still exits 0.

## Constraints
- Standard library only. Don't change `tokenizer.py` or `extract.py`. Edit `expected.json` only to add `graph`.

## Out of scope
- Complexity score, Markdown report, any graph drawing (dot/mermaid).

## Result
Done. Hand computation confirmed (3 steps, one cycle [a.p, b.p], no missing).
- `.venv/bin/pytest -q`: 57 passed, 0 xfailed
- CLI `scan samples/app --out` vs `expected.json`: exit 0, identical
- Also edited `tests/test_cli.py` (empty-dir expectation now includes `graph`), not listed in the brief.
Decide: a basename match uses the target's last path segment; a self-edge is kept in `edges` and `cycles`.
