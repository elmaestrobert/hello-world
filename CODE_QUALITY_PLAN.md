# 2-Month Plan: Writing Cleaner, More Structured Code

A practical 8-week program for building the habits, tools, and judgment that produce clean, well-structured code. Each week has a **theme**, **concrete actions**, and a **checkpoint** so you can verify progress instead of just reading about it.

**Ground rule for the whole plan:** every week you write real code and apply the week's theme to it. Reading alone doesn't build the habit. Use one ongoing project (or this repo) as your workbench so improvements compound.

---

## Month 1 — Fundamentals & Tooling

### Week 1: Baseline and readability basics

**Goal:** Know what "clean" means concretely, and get an honest picture of your current habits.

- Pick (or start) a small project you'll evolve for the whole 8 weeks — e.g. a CLI tool, a small API, or a game. It should be big enough to have 5+ files by week 4.
- Read the first ~4 chapters of *Clean Code* (Robert C. Martin) **or** *A Philosophy of Software Design* (John Ousterhout — shorter and more modern; recommended).
- Learn and apply the core readability rules:
  - Names say what things *are* or *do* (`daysUntilExpiry`, not `d` or `temp2`).
  - Functions do one thing; if you need "and" to describe it, split it.
  - Keep functions short enough to read without scrolling (~20–30 lines is a decent early heuristic, not a law).
- Take one piece of old code you wrote and rewrite it applying only naming + function-size rules. Keep the before/after.

**Checkpoint:** You can look at the before/after diff and explain, in one sentence per change, why each change improves readability.

### Week 2: Automated formatting and linting

**Goal:** Stop spending willpower on style — machines enforce it.

- Set up for your main language:
  - **Python:** `ruff` (lint + format) or `black` + `ruff`
  - **JavaScript/TypeScript:** `prettier` + `eslint`
  - **Go:** `gofmt` + `golangci-lint` (formatting is built-in)
  - **Java:** `google-java-format` + `checkstyle` or `spotless`
- Add the formatter/linter to your editor so it runs on save.
- Add a pre-commit hook (`pre-commit` framework, or `husky` for JS) so nothing unformatted gets committed.
- Run the linter on your project, fix every warning once, then keep it at zero.

**Checkpoint:** A commit with a style violation is impossible on your machine — the hook blocks it.

### Week 3: Functions, modules, and separation of concerns

**Goal:** Structure code so each piece has one clear responsibility.

- Learn the key ideas: single responsibility, separation of concerns, pure functions vs. side effects, and "deep modules" (simple interface, substantial implementation — Ousterhout ch. 4–5).
- Restructure your project:
  - Separate I/O (reading files, HTTP, printing) from logic (calculations, decisions). Logic functions take data in, return data out.
  - Group related functions into modules/files with names that describe the domain (`billing.py`, `parser.ts`), not vague buckets (`utils`, `helpers`, `misc`).
  - Kill your `utils` file if you have one: every function in it belongs somewhere with a real name.
- Practice: for each module, write a one-sentence description of what it's responsible for. If you can't, split it.

**Checkpoint:** Someone could read your file/folder names alone and roughly guess how the program works.

### Week 4: Version control discipline

**Goal:** Small, coherent commits with messages that explain *why*.

- Adopt these rules for the rest of the plan:
  - One logical change per commit. If your diff does two things, split it (`git add -p` is your friend).
  - Commit messages: a short imperative summary line ("Add retry to payment client"), plus a body explaining *why* when it isn't obvious.
  - Work on branches; keep `master`/`main` always working.
- Read: "How to Write a Git Commit Message" (Chris Beams) and try Conventional Commits (`feat:`, `fix:`, `refactor:`) — useful even solo.
- Practice interactive rebase (`git rebase -i`) on a feature branch to squash "wip" commits into a clean story before merging.

**Checkpoint:** Run `git log --oneline -20` on your project. Every line should tell a coherent story; no "fix", "asdf", or "more changes".

---

## Month 2 — Design, Testing, and Sustained Quality

### Week 5: Testing as a design tool

**Goal:** Tests that catch regressions *and* push you toward better structure — hard-to-test code is usually badly structured code.

- Learn your language's standard test framework (`pytest`, `jest`/`vitest`, `go test`, `JUnit`).
- Write tests for the pure-logic modules you separated in week 3 — notice how easy they are to test *because* you separated them. That's the feedback loop.
- Learn the Arrange–Act–Assert pattern and give tests names that describe behavior: `test_expired_token_is_rejected`, not `test_1`.
- Try TDD for one small feature (test first, then code). You don't have to adopt it forever — the point is feeling how it forces small, focused functions.
- Aim for meaningful coverage of core logic, not a coverage percentage. Error paths and edge cases matter more than happy paths.

**Checkpoint:** You can refactor a core module and know within seconds whether you broke something.

### Week 6: Refactoring patterns and code smells

**Goal:** Recognize bad structure on sight and know the standard fix.

- Read *Refactoring* (Martin Fowler) ch. 1–3, or work through the catalog at refactoring.guru.
- Learn to spot the most common smells and their fixes:
  - **Duplicated code** → extract function/module
  - **Long parameter list** → introduce a parameter object / config struct
  - **Deep nesting** → guard clauses / early returns
  - **Boolean flags changing behavior** → split into two functions
  - **Feature envy** (function mostly uses another module's data) → move it there
- Do one refactoring session on your project: pick the ugliest file, list its smells, fix them one at a time **with tests passing after each step and one commit per step**. This combines weeks 3–5.

**Checkpoint:** A refactoring branch with 5+ small commits, each one a named refactoring, tests green throughout.

### Week 7: Design and architecture at project scale

**Goal:** Structure above the function level — how files, layers, and dependencies fit together.

- Learn layered thinking: domain logic at the center, I/O (web, DB, CLI) at the edges, dependencies pointing inward. You don't need full hexagonal architecture — just the instinct that *business logic shouldn't import the web framework*.
- Learn to use interfaces/protocols/abstract types at boundaries so you can swap implementations (real DB vs. in-memory fake in tests).
- Write a short `ARCHITECTURE.md` for your project: the layers, what depends on what, and where a new feature would go. If it's hard to write, that's a finding — restructure until it's easy.
- Skim 2–3 well-regarded open-source projects in your language and study their folder structure and module boundaries. Steal what's good.

**Checkpoint:** Given a hypothetical new feature, you can name the file it goes in and what new files it needs — in under a minute.

### Week 8: Code review, CI, and making it stick

**Goal:** External feedback loops so quality doesn't depend on daily discipline.

- Set up CI (GitHub Actions is free for this repo): on every push, run the formatter check, linter, and tests. A red ❌ on your own PR is a great teacher.
- Adopt a PR workflow even solo: branch → PR → self-review the diff in the GitHub UI → merge. Reading your own diff as a reviewer catches an astonishing amount.
- Get human review if you can: a colleague, a friend, or contribute a small PR to an open-source project and absorb the review feedback.
- Write a personal `CODING_STANDARDS.md`: the 10–15 rules from these 8 weeks that made the biggest difference for you. This becomes your durable checklist.
- Retrospective: diff week-1 code against week-8 code. Write down the three biggest changes in how you work.

**Checkpoint:** A PR merged with green CI, and your personal standards doc committed to the repo.

---

## Ongoing habits after the 8 weeks

- **Boy Scout Rule:** every time you touch a file, leave it slightly cleaner.
- **Refactor in the open:** small refactoring commits alongside feature work, not "big cleanup someday."
- Re-read your `CODING_STANDARDS.md` monthly and prune/update it.
- Once a quarter, read one more chapter of Fowler or Ousterhout and apply it deliberately.

## Recommended resources (in priority order)

1. *A Philosophy of Software Design* — John Ousterhout (best effort-to-insight ratio)
2. *Refactoring*, 2nd ed. — Martin Fowler (ch. 1–3 + catalog as reference)
3. *Clean Code* — Robert C. Martin (good on naming/functions; take the dogma with salt)
4. refactoring.guru — free catalog of smells and refactorings
5. Your language's official style guide (PEP 8, Effective Go, Google style guides)

## Weekly rhythm (suggested)

- **~3 focused sessions/week**: two building/refactoring sessions, one reading/study session.
- End each week by writing 3–5 bullet points: what you changed about how you code. Small, named lessons stick; vague intentions don't.
