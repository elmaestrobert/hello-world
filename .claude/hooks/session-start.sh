#!/usr/bin/env bash
# SessionStart hook — runs when a Claude Code session begins.
# Keeps remote/web sessions ready without failing on a bare repo.
# Add real setup (dependency install, env checks) as the project grows.
set -euo pipefail

# Conditionally install dependencies only if a manifest exists.
if [ -f package-lock.json ]; then
  npm ci --silent || echo "session-start: npm ci failed (non-fatal)"
elif [ -f package.json ]; then
  npm install --silent || echo "session-start: npm install failed (non-fatal)"
fi

if [ -f requirements.txt ]; then
  pip install -q -r requirements.txt || echo "session-start: pip install failed (non-fatal)"
fi

echo "session-start: environment ready ($(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo 'no-branch'))"
