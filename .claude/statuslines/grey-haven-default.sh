#!/bin/bash
# Grey Haven Studio default statusline
# Shows: Model | Git branch & status | Directory | Cost | Lines changed

set -euo pipefail

# Read JSON input from stdin
input=$(cat 2>/dev/null || echo '{}')

# Extract values using jq
MODEL=$(echo "$input" | jq -r '.model.display_name // "Unknown"')
DIR=$(basename "$(echo "$input" | jq -r '.workspace.current_dir // "."')")
COST=$(echo "$input" | jq -r '.cost.total_cost_usd // 0' | xargs printf "%.4f")
ADDED=$(echo "$input" | jq -r '.cost.total_lines_added // 0')
REMOVED=$(echo "$input" | jq -r '.cost.total_lines_removed // 0')

# Git status
GIT_INFO=""
if command -v git >/dev/null 2>&1 && git rev-parse --git-dir >/dev/null 2>&1; then
    BRANCH=$(git branch --show-current 2>/dev/null || echo "detached")
    
    # Check if working directory is clean
    if git diff --quiet 2>/dev/null && git diff --cached --quiet 2>/dev/null; then
        GIT_STATUS="✅"
    else
        # Count changes
        STAGED=$(git diff --cached --numstat 2>/dev/null | wc -l | tr -d ' ')
        UNSTAGED=$(git diff --numstat 2>/dev/null | wc -l | tr -d ' ')
        UNTRACKED=$(git ls-files --others --exclude-standard 2>/dev/null | wc -l | tr -d ' ')
        
        if [ "$STAGED" -gt 0 ]; then
            GIT_STATUS="🟡"  # Has staged changes
        elif [ "$UNSTAGED" -gt 0 ] || [ "$UNTRACKED" -gt 0 ]; then
            GIT_STATUS="🔴"  # Has unstaged changes
        else
            GIT_STATUS="✅"
        fi
    fi
    
    GIT_INFO=" | $GIT_STATUS $BRANCH"
fi

# Model emoji based on type
case "$MODEL" in
    "Opus") MODEL_EMOJI="🧠" ;;
    "Sonnet") MODEL_EMOJI="🎵" ;;
    "Haiku") MODEL_EMOJI="🍃" ;;
    *) MODEL_EMOJI="🤖" ;;
esac

# Cost indicator
if (( $(echo "$COST > 5.0" | bc -l) )); then
    COST_INDICATOR=" | 💸 \$$COST"
elif (( $(echo "$COST > 1.0" | bc -l) )); then
    COST_INDICATOR=" | 💵 \$$COST"
else
    COST_INDICATOR=" | 💰 \$$COST"
fi

# Lines changed (only show if non-zero)
LINES_INFO=""
if [ "$ADDED" -gt 0 ] || [ "$REMOVED" -gt 0 ]; then
    LINES_INFO=" | +$ADDED/-$REMOVED"
fi

# Compose the statusline
echo "🏰 $MODEL_EMOJI $MODEL$GIT_INFO | 📁 $DIR$COST_INDICATOR$LINES_INFO"