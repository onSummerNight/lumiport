# Brief: step 12, close v1 (MIT license, pre-public audit, v0.1.0 tag)

**Goal:** the repo is ready to go public as v0.1.0. It needs an MIT license, a clean audit of the working tree and the full git history, and a local annotated tag. Push and visibility are left for the user.

**Why now:** the user chose to close v1, use MIT and make the repo public (`docs/DECISIONS.md`, 2026-10-08).

## Steps
1. `LICENSE`: the standard MIT text, `Copyright (c) 2026 Luminous` (from `git config user.name`). In Result, ask the user to confirm the holder name. `pyproject.toml`: `license = {text = "MIT"}`. README: replace "Not decided yet" with MIT plus a link to `LICENSE`.
2. Audit the working tree and every commit (`git log -p --all`) for:
   - secrets and tokens (`gho_`, `ghp_`, `sk-`, `AKIA`, `BEGIN .* KEY`, `password`)
   - IP addresses, hostnames other than github.com, and email addresses other than the commit author's
   - any `.env` file ever committed

   List each match and its verdict in Result. Rewriting history is out of scope, so stop if anything real turns up.
3. Check that `pyproject.toml` and `__version__` both say `0.1.0`. Rewrite `docs/PROGRESS.md`:
   - Done: a short v1 summary
   - Now: "awaiting user: push, tag push, make public"
   - Later: Claude mode only
4. Commit, then `git tag -a v0.1.0 -m "LumiPort v0.1.0: ABL inventory, graph, migration order, report"`. Don't push the commit or the tag, and don't change the repo's visibility.
5. Run the full acceptance checks one last time: pytest on 3.14 and on a fresh 3.10 venv, the CLI-vs-`expected.json` check, and the `--report` diff.

## Acceptance check
All four checks from step 5 pass. `git tag -n v0.1.0` shows the tag on the new commit. The audit lists no real findings.

## Constraints
- No code changes. Don't edit `CONTEXT.md`.

## Out of scope
- `git push`, `gh repo edit --visibility public`, PyPI, CI, badges. The manager asks the user about these after review.

## Result

Done. Not pushed, visibility unchanged (repo still private).
- pytest: 3.10.20 `77 passed in 0.09s`; 3.14.7 `77 passed in 0.06s`. CLI JSON == `expected.json`; `--report` diff exit 0.
- Audit (20 commits, `git log -p --all`, 3,748 lines + working tree): no `gho_`/`ghp_`/`sk-`/`AKIA`/`BEGIN .* KEY`/`password` matches; no IPs; only URL is github.com/multica-ai/andrej-karpathy-skills (CLAUDE.md credit); no `.env`/key/db file ever committed.
- Emails: `luminous@lumidev.online` (all 20 commits, author = committer) and `noreply@anthropic.com` (Co-Authored-By). `@pytest`/`@app` matches are decorators.
- Version: `pyproject.toml` and `__version__` both `0.1.0`.

Decide: (1) confirm the LICENSE holder "Luminous" (from `git config user.name`). (2) `luminous@lumidev.online` becomes public in every commit once the repo flips; confirm that is fine. (3) Push of commits and tag, and the visibility flip, are yours.
