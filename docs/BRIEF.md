# Brief: step 10, remaining extractor gaps

**Goal:** close the three gaps listed under Later. Include-argument references stop counting as includes, `FUNCTION ... IN handle` prototypes stop counting as units, and table names merge case-insensitively.

**Why now:** v1 is complete. These gaps make real-world scans over-count includes and units and split tables, so fixing them is what makes the output trustworthy. All three stay inside the locked scope.

## Steps
1. Includes: skip a `{...}` whose first token starts with a digit or `*`, i.e. include-argument references like `{1}` or `{*}`. `{&NAME}` is already skipped.
2. Units: skip a `FUNCTION` whose header, up to its first `:` or `.`, contains the keyword `IN` outside parentheses. That covers both `IN hProc` and `IN SUPER`. `INPUT`/`INPUT-OUTPUT` parameters must not trigger it.
3. Tables, within one file: in `extract_tables`, merge names case-insensitively and keep the spelling of the first occurrence in the source. Write still wins.
4. Tables, across files: in `render_report`, group the Tables section and the summary count case-insensitively, using the first spelling in path order. Update `docs/SCHEMA.md` with the rules from steps 1–4, and remove these gaps from the README Limitations and from Later in `docs/PROGRESS.md`.
5. Tests:
   - inline tests for `{1}` and `{*}`
   - `FUNCTION f RETURNS INT (INPUT p AS INT) IN hLib.`
   - `FUNCTION g RETURNS INT IN SUPER.`
   - a normal function with an `INPUT` parameter, still counted
   - `customer` plus `Customer` in one file giving one key
   - a report test with two files that spell a table differently

## Acceptance check
`.venv/bin/pytest -q` passes. The CLI-vs-`expected.json` and `--report` diff checks still exit 0, unchanged, because the samples have none of these cases.

## Constraints
- Standard library only. Don't edit `samples/`, `expected.json` or `expected-report.md`. If one of them needs to change, stop and report it in Result.

## Out of scope
- The O(files × edges) graph fix, `//` comments, keyword abbreviations, `PROCEDURE ... EXTERNAL`/`IN SUPER`, the cycle display format.

## Result

Done. `.venv/bin/pytest -q`: `76 passed in 0.05s`. CLI `--out` JSON == `expected.json`; `--report` diff vs `expected-report.md` exit 0. `samples/` and expected files untouched.

Decide: table spelling inside a file is "first occurrence in source" across reads and writes (position order), not read-first. 3.10 was not rerun for this step.
