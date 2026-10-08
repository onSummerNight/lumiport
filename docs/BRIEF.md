# Brief: step 3, tokenizer (strip comments and strings)

**Goal:** `lumiport.tokenizer.strip_code(text: str) -> str` blanks out comments and string literals, so later extractors only see real code.

**Why now:** every extractor (units, RUN, includes, tables) depends on it. `report.p` already contains decoys it has to defeat.

## Steps
1. `src/lumiport/tokenizer.py`: one pass, character by character. Replace every character inside a comment or string with a space, but keep newlines so line numbers and offsets still match the source. Quotes and comment markers are blanked as well.
2. Rules: `/* */` nests to any depth. Strings use `"` or `'`. Inside a string, `~` escapes the next character and a doubled quote (`""` / `''`) does not end it. `/*` inside a string is plain text, and a quote inside a comment is plain text. An unterminated comment or string blanks everything to the end of the file (no exception).
3. `tests/test_tokenizer.py`: one small test per rule above. Add one test on `samples/app/report.p` showing that `ghost`, `phantom`, `fake.p`, `decoy` and `ghost-row` are gone while `printLine` and `FOR EACH order` remain.
4. Check that output length and newline count equal the input's, on every sample file.

## Acceptance check
`.venv/bin/pytest -q`: all tokenizer tests pass, the existing 2 still pass, and the golden test stays xfailed.

## Constraints
- Standard library only. No regex-based comment stripping, because nesting needs a counter.
- Don't touch `expected.json` or `SCHEMA.md`.

## Out of scope
- Extracting units, RUN calls, includes or tables. Keyword case-folding. Preprocessor (`&SCOPED-DEFINE`, `{&NAME}`) handling.
- `{include.i}` braces are code, not comments: leave them.

## Result
Done.
```
pytest -q: 15 passed, 1 xfailed in 0.03s
(13 tokenizer tests incl. report.p decoys and length/newline check on all 11 samples; golden still xfailed)
```
Nothing to decide. Choice: `\r` is kept like `\n`; a `~` escaping a newline keeps that newline.
