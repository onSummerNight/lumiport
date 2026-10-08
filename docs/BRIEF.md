# Brief: step 4b, extract table access and buffers

**Goal:** `lumiport.extract.extract_tables(code: str) -> dict`, which returns `{table: "read"|"write"}` for one stripped file, following `docs/SCHEMA.md`.

**Why now:** this is the second half of the extractors. After it, 4c can build `scan_dir` and turn the golden test green.

## Steps
1. Buffers first: collect every `DEFINE BUFFER b FOR t` in the file, wherever it appears, so a use before the definition still resolves. Alias lookup is case-insensitive and maps to `t` as written in the definition.
2. Read: `FOR EACH|FIRST|LAST name`, the `, EACH|FIRST|LAST name` join parts, and `FIND [FIRST|LAST|NEXT|PREV|CURRENT] name`. Write: `CREATE name` and `DELETE name`. Write wins over read.
3. Not tables: dynamic objects after `CREATE` (`QUERY`, `BUFFER`, `TEMP-TABLE`, `WIDGET-POOL`, `ALIAS`, `SERVER`, `SOCKET`, `X-DOCUMENT`, `X-NODEREF`) and after `DELETE` (`OBJECT`, `PROCEDURE`, `WIDGET`, `WIDGET-POOL`, `ALIAS`). Field references such as `order.num` or `order-line.order-num` are never access.
4. `tests/test_extract.py`: per sample file, parametrized, compare `tables` to `expected.json`. Add inline tests for lower-case keywords, `FOR EACH a, EACH b`, buffer used before its definition, `CREATE QUERY hQ`, `DELETE OBJECT h`, and `FIND CURRENT x EXCLUSIVE-LOCK`.

## Acceptance check
`.venv/bin/pytest -q`: all new tests pass, the existing 32 still pass, and the golden test stays xfailed.

## Constraints
- Standard library only. Change only `extract.py` and `test_extract.py`. If a sample disagrees with the schema, stop and report it in Result.

## Out of scope
- `scan_dir`, CLI output, `DEFINE BUFFER ... FOR TEMP-TABLE`, DB-qualified names (`db.table`), `ASSIGN`/field updates as write, and the 4a gaps listed under Later.

## Result
Done. `.venv/bin/pytest -q`:
```
....................................x.............                       [100%]
49 passed, 1 xfailed in 0.04s
```
All 11 sample files match `expected.json` tables; no schema conflicts. Nothing to decide.
