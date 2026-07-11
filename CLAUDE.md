# CLAUDE.md

Guidance for Claude Code when working in this repository. Keep this file current —
every correction you find yourself repeating belongs here as a rule.

## Project

`hello-world` — a sandbox repo. Update this section with the real purpose,
stack, and entry points once the project takes shape.

## Commands

<!-- Fill in as the project grows. Examples: -->
<!-- - Install:  npm install -->
<!-- - Test:     npm test -->
<!-- - Lint:     npm run lint -->
<!-- - Build:    npm run build -->
<!-- - Run:      npm start -->

## Conventions

- Match the style of surrounding code (naming, comments, structure).
- Small, focused commits with clear messages.
- Prefer editing existing files over adding new ones unless a new file is warranted.

## Anti-patterns (never do these)

<!-- Capture hard "don't"s here as you discover them. Examples: -->
<!-- - Never commit secrets or .env files. -->
<!-- - Never push directly to main. -->

## Workflow expectations

- Use plan mode for any multi-file change; get the approach approved before editing.
- Run available checks (tests/lint) before considering a change done.
- For risky or wide changes, review the diff (`/code-review`) before committing.

## Notes

- This file loads automatically into context. Nested `CLAUDE.md` files in
  subdirectories add module-specific rules.
