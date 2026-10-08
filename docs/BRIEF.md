# Brief: step 6, complexity score per file

**Goal:** each file entry in the scan output gains `metrics: {loc, blocks, branches, fan_in, fan_out, score}`, using the formula in `docs/DECISIONS.md` (2026-10-08, "graph details and complexity score formula"). The golden test pins it.

**Why now:** it's the last inventory number v1 needs. The Markdown report (step 7) only formats data that already exists.

## Steps
1. `docs/SCHEMA.md`: add `metrics` (after `tables`) with the rules below and the score formula.
2. `src/lumiport/metrics.py`: `file_metrics(code: str) -> dict` works on stripped code.
   - `loc`: lines that contain any non-whitespace character.
   - `blocks`: `END` keywords, case-insensitive, not part of `END-KEY`, `END-ERROR` and similar.
   - `branches`: `IF` keywords plus `WHEN` keywords.
3. In `scan_dir`, after `build_graph`, add `fan_in`/`fan_out`: the number of distinct *other* files on incoming/outgoing edges, so self-edges don't count. Then compute `score = loc + 2*(branches + blocks) + 5*(fan_in + fan_out)`.
4. Update `samples/expected.json` by hand for all 11 files. In Result, show your working for `order-create.p` and `report.p`.
5. `tests/test_metrics.py`: inline tests for blank lines only, `END-ERROR` not counted, lower-case `if`, `CASE ... WHEN ... WHEN`, a comment-only line (loc 0 after stripping), and a self-call that doesn't add to fan_in/fan_out.

## Acceptance check
`.venv/bin/pytest -q`: all pass. The CLI-vs-`expected.json` check still exits 0.

## Constraints
- Standard library only. Don't change `tokenizer.py`, `extract.py` or `graph.py`, except to expose edges if needed. Edit `expected.json` only to add `metrics`.

## Out of scope
- Markdown report, sorting the order by score, per-unit metrics, the O(files × edges) graph fix.

## Result

Done. `.venv/bin/pytest -q`: 63 passed; CLI output == `samples/expected.json` (exit 0).

Working (hand-counted from the sample source, then matched by the code):
- `order-create.p`: loc 16 (lines 2,3,5,7,8,10,11,13,14,16-19,21-23); blocks 2 (END PROCEDURE, END FUNCTION); branches 1 (IF); fan_out 3 (common.i, util.i, price-calc.p); fan_in 0 -> 16 + 2*3 + 5*3 = **37**
- `report.p`: loc 11 (comment lines 1-4 blank after stripping); blocks 2 (END., END PROCEDURE); branches 0; fan_out 1 (common.i); fan_in 0 -> 11 + 4 + 5 = **20**

Decide: `IF` is counted for inline `IF ... THEN ... ELSE` expressions too (price-calc.p), per "IF keywords". Also `END` is counted in `END CLASS`/`END METHOD`.
