# Brief: step 8, README and usage

**Goal:** a `README.md` that lets a new user install LumiPort, scan a folder, and understand the JSON and the report, including what the scanner does not understand.

**Why now:** all v1 scope items are built and pinned by tests. Without a README nobody can use them, and the v1 review needs it.

## Steps
1. `README.md` (about 80 lines max):
   - What it is (2–3 lines).
   - Install: venv + `pip install -e '.[dev]'`, Python 3.10+.
   - Usage: `lumiport scan <dir>`, `--out`, `--report`.
   - A short excerpt of `samples/expected-report.md`.
   - Links to `docs/SCHEMA.md` and to the score formula.
2. A **Limitations** section, in plain words:
   - tokenizer-level scanning, not a parser
   - `RUN VALUE(...)` counted, not resolved
   - the extractor gaps listed under Later in PROGRESS
   - `//` comments and keyword abbreviations not handled
   - `.w` files skipped
   - Python 3.10 not yet tested (only 3.14)
3. A **Clean room** note: the samples are synthetic, written for this repo.
4. State that the license is not decided yet. Don't add a LICENSE file.
5. Run every command shown in the README from a fresh clone (`git clone . <tmpdir>`, new venv) and paste the outcome into Result.

## Acceptance check
Every README command runs successfully in the fresh clone, and `.venv/bin/pytest -q` still passes there.

## Constraints
- Docs only: no code changes, and don't edit `CONTEXT.md` or `SCHEMA.md`. Claim nothing the tests don't show.

## Out of scope
- LICENSE, badges or CI, publishing to PyPI, making the repo public.

## Result

Done. Fresh clone (`git clone . <tmp>`, new venv, README added to the clone):
- `pip install -e '.[dev]'` exit 0; `scan samples/app` (stdout JSON), `--out`, `--report` all exit 0
- `diff report.md samples/expected-report.md` exit 0; `--out` JSON == `expected.json`
- `pytest -q`: 66 passed (Python 3.14.7 only)

Decide: README is 59 lines. Install uses `.venv/bin/...` paths instead of activating the venv. License still undecided, as stated in the README.
