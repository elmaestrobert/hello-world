# Claude Mastery Plan

A comprehensive plan for getting the most out of Claude across coding, writing,
research, and automation. The core idea: treat Claude as a **system you
configure, delegate to, and improve over time** — not a per-question tool.
Advanced use is less about better prompts and more about better context, better
guardrails, and better delegation.

## Area 1 — Coding with Claude Code

**Context engineering (highest leverage)**
- `CLAUDE.md` is a living spec, not a readme. Put build/test/lint commands,
  architecture, conventions, and *anti-patterns* ("never do X"). Every correction
  you make should become a line here — that's the compounding loop.
- Use **nested `CLAUDE.md`** files in subdirectories for module-specific rules;
  they load contextually.
- Keep a `.claude/` directory of **custom slash commands** for repeated workflows
  (e.g. a `/ship` that runs review → test → commit).

**Workflow discipline**
- **Plan mode by default** for anything multi-file. Approve the approach before
  any edit — catches wrong turns when they're cheap.
- **Delegate breadth to subagents**: `Explore` for "where/how" searches, `Plan`
  for architecture, parallel agents for independent workstreams.
- **Verify, don't trust**: `/code-review` on the diff, `/security-review` for
  sensitive changes, `/verify` to actually run the app. For high-stakes work, use
  adversarial review (multiple agents trying to *refute* a change).
- **One concern per session.** Fresh sessions for unrelated tasks.

**Permissions & friction**
- `fewer-permission-prompts` skill → scan history, pre-allow safe commands.

## Area 2 — Chat / writing / thinking (claude.ai)

- **Projects** with custom instructions + knowledge files = a persistent expert.
  Set one up per recurring domain (writing voice, a client, a codebase, a topic).
- **Model selection as a habit**: Opus for hard reasoning/ambiguity, Sonnet for
  speed/volume, Haiku for cheap bulk.
- **Artifacts** for anything you'll iterate on (docs, code, diagrams).
- **Prompt patterns that scale**: role + goal + constraints + examples of
  good/bad output. For writing, give a sample of *your* voice.
- **Use Claude as a thinking partner**: ask it to steelman the opposing view, find
  the weakest part of your argument, or list what you're not considering.

## Area 3 — Research & analysis

- The **`deep-research` skill**: fan-out web search → fetch sources →
  adversarially verify → cited report. Use it for any costly-to-be-wrong decision.
- **Insist on citations and verification**; have Claude flag low-confidence claims.
- For document analysis, pull source material directly from connected
  **Drive/Dropbox** rather than pasting.
- **Comparison tables** for any multi-option decision.

## Area 4 — Automation & integrations

Connected MCP servers: **GitHub, Google Drive, Dropbox, Spotify.**
- **PR autopilot**: after a PR exists, subscribe to its activity — Claude
  auto-fixes CI failures and answers review comments while you're away.
- **Hooks** for deterministic automation: `SessionStart` (prep env),
  `PostToolUse` (auto-format/lint), `Stop` (notify when done). The harness runs
  these, not Claude — so they're reliable.
- **Scheduled & recurring work**: `/loop` for polling, background tasks for
  long-running jobs, cron for periodic runs.
- **Cross-tool workflows**: e.g. "summarize this Drive doc → open a GitHub issue."
- **Web environment tuning**: right network policy + setup script.

## Meta-layer — the compounding system

1. **Externalize context** — every preference, convention, and correction lives in
   a file, not in your head or one chat.
2. **Delegate by default** — subagents/background tasks over serial work.
3. **Verify adversarially** — for anything that matters, a second agent whose job
   is to find the flaw.
4. **Capture learnings** — when Claude gets something wrong, fix the *system* (a
   rule, a hook, a command) so it can't recur.

## Rollout order

| When | Do |
|---|---|
| **Now** | `/init` → `CLAUDE.md`; `SessionStart` hook; permissions allowlist |
| **This week** | 1–2 claude.ai Projects; 2–3 custom slash commands |
| **Ongoing** | Plan-mode + subagent + verify habits; capture corrections into config |
| **As needed** | PR autopilot, hooks, scheduled tasks, cross-MCP workflows |

---

*This repo now includes a starter `CLAUDE.md`, a `SessionStart` hook
(`.claude/hooks/session-start.sh`), a permissions allowlist
(`.claude/settings.json`), and a `/ship` command (`.claude/commands/ship.md`) as
the Phase 1 foundation.*
