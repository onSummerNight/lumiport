# LumiPort

Inventory tool for Progress OpenEdge ABL code, aimed at teams planning a move to Python.
It scans `.p`, `.i` and `.cls` files and reports what exists, what calls what, which
tables each file touches, and a suggested migration order with a complexity score.

## Install

Python 3.10+ (see Limitations).

```sh
python3 -m venv .venv
.venv/bin/pip install -e '.[dev]'
```

## Usage

```sh
.venv/bin/lumiport scan samples/app                      # JSON inventory on stdout
.venv/bin/lumiport scan samples/app --out inventory.json # JSON to a file
.venv/bin/lumiport scan samples/app --report report.md   # also write a Markdown report
.venv/bin/pytest -q                                      # run the tests
```

`--report` still prints the JSON to stdout unless `--out` is given.
The JSON format is in [docs/SCHEMA.md](docs/SCHEMA.md). The score formula is in the
report's last section and under `metrics` in the schema.

Excerpt of the report for the sample app (full file: [samples/expected-report.md](samples/expected-report.md)):

```markdown
## Summary

- Files: 1 .cls, 3 .i, 7 .p
- Total loc: 77
- Cycles: 1
- Unresolved dynamic calls: 1

## Cycles

- a.p -> b.p
```

## Limitations

- It is a tokenizer-level scanner, not a parser. It strips comments and strings, then matches keywords.
- Dynamic calls such as `RUN VALUE(...)` are counted as unresolved, never resolved.
- Known extractor gaps: `{1}` include arguments are counted as includes; `FUNCTION ... IN handle` is counted as a unit; table names that differ only in case are separate tables.
- `//` line comments and keyword abbreviations are not handled.
- `.w` files are skipped.
- Tested on Python 3.10 and 3.14.

## Clean room

The sample ABL in `samples/` is synthetic, written for this repository. Nothing in it comes from an employer or client.

## License

Not decided yet. There is no LICENSE file.
