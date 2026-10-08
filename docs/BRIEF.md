# Brief: step 1, project skeleton

**Goal:** an installable `lumiport` package with a `lumiport scan <dir>` command (stub) and one passing smoke test.

**Why now:** every later step (sample app, golden test, tokenizer) needs a package, a CLI entry point and a working pytest run.

## Steps
1. `pyproject.toml`: name `lumiport`, `requires-python = ">=3.10"`, dependency `typer`, optional `dev` extra with `pytest`, console script `lumiport = "lumiport.cli:app"`. Use a `src/` layout.
2. `src/lumiport/__init__.py` (with `__version__`) and `src/lumiport/cli.py`: a Typer app with a `scan` command that takes a directory, exits 2 with an error if it is not an existing directory, otherwise prints `scan: <dir> (not implemented)` and exits 0.
3. `tests/test_cli.py`: uses Typer's `CliRunner` to check `scan <tmp_path>` exits 0 and `scan <missing path>` exits non-zero.
4. Make sure `.venv/` stays ignored (it already is); add nothing else to `.gitignore` unless the build creates new artifacts.

## Acceptance check
```
python3 -m venv .venv && .venv/bin/pip install -e '.[dev]' && .venv/bin/pytest -q && .venv/bin/lumiport scan docs
```
pytest passes and the last command exits 0.

## Constraints
- Python 3.10+, Typer, pytest only. No other dependencies, linters or config files.
- Clean room. Small commit: `build: project skeleton with scan stub`.

## Out of scope
- Any scanning logic, sample ABL files, `expected.json`, tokenizer, output formats.

## Result
Done.
```
pytest -q: 2 passed in 0.01s
lumiport scan docs -> "scan: docs (not implemented)", exit 0
```
Nothing for the manager to decide. Note: Python here is 3.14.7; 3.10 compatibility not tested.
