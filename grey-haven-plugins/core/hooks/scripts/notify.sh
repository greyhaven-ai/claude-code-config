#!/bin/bash
# Desktop notification when Claude Code needs attention
# Cross-platform: macOS (osascript), Linux (notify-send)

TITLE="Claude Code"
MSG="Claude Code needs your attention"

if command -v osascript &>/dev/null; then
  osascript -e "display notification \"$MSG\" with title \"$TITLE\"" 2>/dev/null
elif command -v notify-send &>/dev/null; then
  notify-send "$TITLE" "$MSG" 2>/dev/null
fi

exit 0
