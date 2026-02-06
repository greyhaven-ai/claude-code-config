#!/bin/bash
# Auto-format code after edits using Grey Haven tooling conventions
# Reads tool_input from stdin JSON (Claude Code hooks API)
# Uses: bunx prettier (JS/TS), uvx ruff (Python)

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

if [ -z "$FILE_PATH" ] || [ ! -f "$FILE_PATH" ]; then
  exit 0
fi

case "$FILE_PATH" in
  *.ts|*.tsx|*.js|*.jsx|*.json|*.css|*.scss|*.html|*.md|*.yaml|*.yml)
    if command -v bun &>/dev/null; then
      bunx prettier --write "$FILE_PATH" 2>/dev/null
    fi
    ;;
  *.py)
    if command -v uvx &>/dev/null; then
      # uvx runs ruff without needing it in project dependencies
      uvx ruff format "$FILE_PATH" 2>/dev/null
      uvx ruff check --fix "$FILE_PATH" 2>/dev/null
    elif command -v uv &>/dev/null; then
      # Fallback: try uv run if ruff is a project dependency
      uv run ruff format "$FILE_PATH" 2>/dev/null
      uv run ruff check --fix "$FILE_PATH" 2>/dev/null
    fi
    ;;
esac

exit 0
