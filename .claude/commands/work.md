---
description: "Worker: do the task in docs/BRIEF.md, verify it, save"
argument-hint: "[note]"
disable-model-invocation: true
---
Do the task in `docs/BRIEF.md`. Extra instruction from the user: $ARGUMENTS

1. Read `docs/BRIEF.md`, and `docs/CONTEXT.md` unless it is already in context. If there is no brief, or it already has a Result section, say so and stop.
2. If the brief is ambiguous or conflicts with the context, ask before writing code.
3. Make the smallest change that passes the acceptance check. Run the check and keep its real output.
4. Rewrite `docs/PROGRESS.md`, append to `docs/LOG.md`, and commit.
5. Append a `## Result` section to `docs/BRIEF.md`: done or not done, the check output in 5 lines at most, anything the manager must decide.
6. Reply in at most 5 lines.
