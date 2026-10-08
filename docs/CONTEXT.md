# Context: LumiPort

Status: LOCKED 2026-10-08

## Problem

Teams that want to move off Progress OpenEdge ABL don't know what they have: which procedures exist, what calls what, which tables each one touches, and what to migrate first.

## Users

Developers and technical leads who maintain ABL applications and plan a move to Python.

## Scope v1

- Tokenizer-level scanner for `.p`, `.i`, `.cls`: strips comments (nested `/* */`) and strings, then extracts `PROCEDURE` / `FUNCTION` / `METHOD` blocks, `{include}` references, `RUN name.p` calls, and table access (`FOR EACH`, `FIND`, `CREATE`, `DELETE`, `DEFINE BUFFER x FOR`) marked read/write
- Dynamic calls (`RUN VALUE(...)` etc.) flagged as unresolved, never guessed
- Dependency graph with cycle detection and a suggested migration order
- Complexity score: LOC + branch/block count + fan-in/fan-out, formula documented in the report
- CLI `lumiport scan <dir>` writing a JSON inventory and a Markdown report

## Non-goals

- A full ABL grammar or an automatic transpiler
- Claude / LLM mode (moved to Later)
- Database migration
- UI code (`.w`)
- Any real application code: the sample app is synthetic, written for this repo

## Success check

`pytest` golden test: `lumiport scan samples/` produces JSON identical to a hand-written `expected.json`. The synthetic sample app has 8–12 files and includes at least one call cycle and one dynamic RUN.

## Stack

Python 3.10+, Typer, pytest. No other dependencies.

## Constraints

Clean room: sample ABL is written from scratch for this repository. Nothing from any employer or client codebase.

## Open questions

- Deadline, public/portfolio repo, license: not yet decided
