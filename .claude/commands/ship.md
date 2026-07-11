---
description: Review, test, and commit the current change in one pass
---

Prepare the current working changes for shipping:

1. Show me `git status` and `git diff` so we both see the change.
2. Run the project's checks if they exist (tests, lint, build). Report results.
3. Review the diff for correctness and obvious cleanups (invoke `/code-review` for non-trivial changes).
4. If checks pass and the review is clean, stage the changes and propose a concise,
   descriptive commit message. Wait for my confirmation before committing.
5. Do NOT push or open a pull request unless I explicitly ask.
