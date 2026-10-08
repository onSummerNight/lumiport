# Brief: step 11, linear-time graph build + scale check

**Goal:** `build_graph` scales linearly. The adjacency list is built in one pass over the edges instead of one pass per file. A synthetic scale test guards against regressions.

**Why now:** this is the last in-scope item under Later. Real ABL codebases have thousands of files, and right now the adjacency build costs files × edges.

## Steps
1. `graph.py`: build `adj` with one pass over `edges` (for example a `defaultdict(set)`, sorted per node afterwards) so the iteration order and output stay identical. Change nothing else unless a profile shows another quadratic spot. If it does, name it in Result.
2. `tests/test_graph.py`: generate 5,000 synthetic file dicts in memory. Each gets 3 runs to deterministic other files (for example `i+1`, `i*7 % n` and `i*13 % n`) and 1 include into 50 shared `.i` files. Assert that `build_graph` finishes in under 5 s and that `order` covers every file exactly once.
3. Measure only, assert nothing: time `scan_dir` on a temporary folder of 2,000 generated `.p` files of about 30 lines each. Report the seconds in Result together with the before and after times of `build_graph` on the 5,000-file set.
4. Remove the graph item from Later in `docs/PROGRESS.md`.

## Acceptance check
`.venv/bin/pytest -q` passes, including the scale test. The CLI-vs-`expected.json` and `--report` diff checks still exit 0.

## Constraints
- Standard library only. The output must stay byte-for-byte identical on the samples. Don't edit `samples/`, `expected.json` or `expected-report.md`.

## Out of scope
- Speeding up the tokenizer or `scan_dir`. Report their timing; if it is slow, I'll brief it separately.
- Parallelism, caching, the CLI.

## Result

Done. `.venv/bin/pytest -q`: `77 passed in 0.06s`; CLI JSON == `expected.json`, `--report` diff exit 0.
- `build_graph`, 5,000 files (4,950 `.p` + 50 `.i`, 19,800 edges): before 1.9 s, after 0.02 s.
- `scan_dir`, 2,000 generated `.p` files (about 21 lines each, plus 1 `.i`): 0.2 s. No slow spot found.

No other quadratic spot named. Nothing to decide. Timing assert in the test is 5 s as briefed.
