#!/bin/bash
# Re-inject Grey Haven tooling conventions after context compaction
# Output goes to stdout and is added to Claude's context

cat <<'CONTEXT'
## Grey Haven Tooling Conventions (post-compaction reinject)

### JS/TS Package Management
- Use `bun` instead of npm/npx/yarn/pnpm
- `bun add <pkg>` not `npm install <pkg>`
- `bun test` not `npm test`
- `bunx <tool>` not `npx <tool>`
- `bun run <script>` not `npm run <script>`

### Python
- Use `uv` instead of pip/pip3/python3
- `uv run <script.py>` not `python3 <script.py>`
- `uv add <pkg>` not `pip install <pkg>`
- `uv venv` not `python3 -m venv`
- `uv run ruff` for linting, `uv run black` for formatting

### Environment Variables
- Use `doppler run -- <command>` to inject env vars at runtime
- Never read from .env files directly; Doppler is the source of truth
- `doppler secrets get <KEY>` to inspect individual secrets
CONTEXT
