# Brief: step 9, Python 3.10 check + `PROCEDURE x PRIVATE:`

**Goal:** prove the test suite passes on Python 3.10, the declared minimum, and recognise `PROCEDURE name PRIVATE:` as a procedure unit.

**Why now:** v1 is built and the success check passes. These are the two cheapest honest gaps to close: one is an untested promise in `pyproject.toml`/README, the other is the most common real-world unit form we miss.

## Steps
1. Python 3.10: create a venv with `uv venv --python 3.10 <scratch dir>`, install with `uv pip install --python <that venv> -e '.[dev]'`, then run its pytest. If anything fails, fix only what is needed for 3.10, using the smallest change that works.
2. `extract.py`: `_PROC` accepts an optional `PRIVATE` (case-insensitive) between the name and `:`. Nothing else changes, and `END PROCEDURE` is still never a unit.
3. `tests/test_extract.py`: add inline tests for `PROCEDURE p PRIVATE:`, lower-case `procedure p private:`, and `END PROCEDURE.` not matching.
4. Remove the PRIVATE gap from the README Limitations and from Later in `docs/PROGRESS.md`. Replace the README line "Only tested on Python 3.14" with the versions actually tested.
5. Paste both pytest outputs (3.10 and 3.14) into Result.

## Acceptance check
`.venv/bin/pytest -q` passes, the same suite passes under the 3.10 venv, and the CLI-vs-`expected.json` and `--report` diff checks still exit 0.

## Constraints
- Don't edit `samples/`, `expected.json` or `expected-report.md`. Don't commit the 3.10 venv: keep it outside the repo.

## Out of scope
- The other extractor gaps (`{1}` args, `FUNCTION ... IN handle`, table-name case), `PROCEDURE ... EXTERNAL`/`IN SUPER`, CI, LICENSE.

## Result

Done. No 3.10 fixes were needed (venv kept outside the repo, via uv).
- Python 3.10.20: `pytest -q` -> `69 passed in 0.09s`
- Python 3.14.7: `pytest -q` -> `69 passed in 0.04s`
- CLI `--out` JSON == `expected.json`; `--report` diff vs `expected-report.md` exit 0

Nothing to decide.
