# Inventory schema (v1, draft)

`lumiport scan <dir>` JSON: `{"files": [ ... ]}`, sorted by `path`. Every list is sorted (plain string order); no duplicates.

| Field | Type | Rule |
|---|---|---|
| `path` | string | Relative to the scanned dir, `/` separators. |
| `kind` | `p` \| `i` \| `cls` | From the file extension. |
| `units` | `[{name, type}]` | `PROCEDURE` -> `procedure`, `FUNCTION` -> `function`, class `METHOD` -> `method`. Sorted by name. Includes in `.i` files count for that file. |
| `includes` | `[string]` | Names in `{name.i}`, as written. |
| `runs` | `[string]` | Literal `RUN name.p` targets, as written. |
| `unresolved_runs` | int | Count of dynamic calls (`RUN VALUE(...)`). Never guessed into `runs`. |
| `tables` | `{table: "read"\|"write"}` | Keys sorted. |

Rules:
- Comments (nested `/* */`) and string literals (`"..."`, `'...'`) are stripped first; keywords inside them are ignored.
- `RUN` of a name without `.p` (an internal procedure) is not a file call: not in `runs`, not counted unresolved.
- `FOR EACH` and `FIND` mark a table `read`; `CREATE` and `DELETE` mark it `write`. Write wins over read.
- `DEFINE BUFFER b FOR t` makes `b` an alias: access through `b` counts for table `t`.
- Table and unit names keep the case used in the source.
- Not in v1 of the schema: graph, cycles, migration order, complexity score.
