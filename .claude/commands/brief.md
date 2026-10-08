---
description: "Review the last result, pick the next task, write it to docs/BRIEF.md"
argument-hint: "[task]"
disable-model-invocation: true
---
Act as the manager for this turn: do not edit source code, write only inside `docs/`.
Instruction from the user, if any: $ARGUMENTS

1. Read `docs/PROGRESS.md` and `docs/BRIEF.md` if it exists. Read `docs/CONTEXT.md` only if it is not already in this session's context. Run `git log --oneline -5` and `git diff --stat HEAD~1` (skip the diff if there are fewer than two commits).
2. If the brief has a Result section, review it in at most 4 lines: did the acceptance check pass, is anything out of scope or risky. Append one line to `docs/LOG.md` recording that brief's goal and outcome. If the work is not done or the check failed, the next brief fixes that first.
3. Choose the next task:
   - If the user gave an instruction, use it. If it is outside `docs/CONTEXT.md`, say so and stop.
   - If one next step is clearly right (usually the top item under Next in PROGRESS), take it without asking.
   - If there is a real choice, offer at most 3 options, one line each, your recommendation first and marked as recommended, with the reason in a few words. Use the AskUserQuestion tool when it is available so the user can pick one or type their own; otherwise print a numbered list and wait.
4. Overwrite `docs/BRIEF.md`, 25 lines at most: Goal, Why now, Steps (5 at most), Acceptance check (a command or test), Constraints, Out of scope.
   One task per brief. If it needs more than 5 steps, split it and brief the first part.
5. Reply in at most 6 lines: the review, the new Goal and Acceptance check, then "Worker terminal: /work".
