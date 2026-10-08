# LumiPort report

## Summary

- Files: 1 .cls, 3 .i, 7 .p
- Total loc: 77
- Units: 7
- Tables: 4
- Cycles: 1
- Missing targets: 0
- Unresolved dynamic calls: 1

## Migration order

### Step 1

| Path | Kind | Score | In cycle |
|---|---|---|---|
| common.i | i | 27 |  |
| price-calc.p | p | 15 |  |
| order-purge.p | p | 13 |  |
| util.i | i | 10 |  |
| consts.i | i | 7 |  |

### Step 2

| Path | Kind | Score | In cycle |
|---|---|---|---|
| order-create.p | p | 37 |  |
| a.p | p | 26 | yes |
| b.p | p | 25 | yes |
| ordermgr.cls | cls | 25 |  |
| report.p | p | 20 |  |

### Step 3

| Path | Kind | Score | In cycle |
|---|---|---|---|
| main.p | p | 26 |  |

## Cycles

- a.p -> b.p

## Missing targets

None

## Unresolved dynamic calls

- main.p: 1

## Tables

| Table | Readers | Writers |
|---|---|---|
| customer | main.p, order-create.p, report.p | - |
| item | price-calc.p | - |
| order | a.p, ordermgr.cls, report.p | order-create.p, order-purge.p |
| order-line | b.p, order-purge.p | order-create.p |

## Files

| Path | loc | blocks | branches | fan_in | fan_out | score |
|---|---|---|---|---|---|---|
| a.p | 4 | 0 | 1 | 2 | 2 | 26 |
| b.p | 6 | 1 | 1 | 1 | 2 | 25 |
| common.i | 2 | 0 | 0 | 5 | 0 | 27 |
| consts.i | 2 | 0 | 0 | 1 | 0 | 7 |
| main.p | 9 | 1 | 0 | 0 | 3 | 26 |
| order-create.p | 16 | 2 | 1 | 0 | 3 | 37 |
| order-purge.p | 6 | 1 | 0 | 1 | 0 | 13 |
| ordermgr.cls | 12 | 4 | 0 | 0 | 1 | 25 |
| price-calc.p | 6 | 1 | 1 | 1 | 0 | 15 |
| report.p | 11 | 2 | 0 | 0 | 1 | 20 |
| util.i | 3 | 1 | 0 | 1 | 0 | 10 |

## How the score is computed

`score = loc + 2*(branches + blocks) + 5*(fan_in + fan_out)`

- `loc`: lines with code after comments and strings are stripped.
- `blocks`: `END` keywords (not `END-KEY`, `END-ERROR` and similar).
- `branches`: `IF` keywords plus `WHEN` keywords.
- `fan_in` / `fan_out`: distinct other files on incoming / outgoing graph edges (RUN calls and includes).
