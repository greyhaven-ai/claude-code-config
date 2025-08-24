#!/bin/bash
# Context-aware statusline that changes based on what you're doing
# Adapts display based on file types, git status, and activity patterns

set -euo pipefail

input=$(cat 2>/dev/null || echo '{}')

# Extract base information
MODEL=$(echo "$input" | jq -r '.model.display_name // "Unknown"')
DIR=$(basename "$(echo "$input" | jq -r '.workspace.current_dir // "."')")
CWD=$(echo "$input" | jq -r '.workspace.current_dir // "."')
COST=$(echo "$input" | jq -r '.cost.total_cost_usd // 0' | xargs printf "%.3f")
ADDED=$(echo "$input" | jq -r '.cost.total_lines_added // 0')
REMOVED=$(echo "$input" | jq -r '.cost.total_lines_removed // 0')

# Detect context based on current directory and recent activity
CONTEXT=""
CONTEXT_EMOJI=""

# Check for specific file types in current directory
if ls *.py 2>/dev/null | head -1 >/dev/null; then
    CONTEXT="Python"
    CONTEXT_EMOJI="🐍"
elif ls *.js *.ts *.jsx *.tsx 2>/dev/null | head -1 >/dev/null; then
    CONTEXT="JavaScript"
    CONTEXT_EMOJI="📜"
elif ls *.rs 2>/dev/null | head -1 >/dev/null; then
    CONTEXT="Rust"
    CONTEXT_EMOJI="🦀"
elif ls *.go 2>/dev/null | head -1 >/dev/null; then
    CONTEXT="Go"
    CONTEXT_EMOJI="🐹"
elif ls *.java 2>/dev/null | head -1 >/dev/null; then
    CONTEXT="Java"
    CONTEXT_EMOJI="☕"
elif ls *.md 2>/dev/null | head -1 >/dev/null; then
    CONTEXT="Docs"
    CONTEXT_EMOJI="📝"
elif ls Dockerfile docker-compose.yml 2>/dev/null | head -1 >/dev/null; then
    CONTEXT="Docker"
    CONTEXT_EMOJI="🐳"
elif [ -f "package.json" ]; then
    CONTEXT="Node"
    CONTEXT_EMOJI="📦"
elif [ -f "requirements.txt" ] || [ -f "pyproject.toml" ]; then
    CONTEXT="Python"
    CONTEXT_EMOJI="🐍"
elif [ -f "Cargo.toml" ]; then
    CONTEXT="Rust"
    CONTEXT_EMOJI="🦀"
else
    CONTEXT="Code"
    CONTEXT_EMOJI="💻"
fi

# Detect what kind of work is being done based on metrics
ACTIVITY=""
if [ "$ADDED" -gt 100 ]; then
    ACTIVITY=" | 🔥 Heavy coding"
elif [ "$ADDED" -gt 50 ]; then
    ACTIVITY=" | ✨ Creating"
elif [ "$ADDED" -gt 10 ]; then
    ACTIVITY=" | 📝 Writing"
elif [ "$REMOVED" -gt "$ADDED" ] && [ "$REMOVED" -gt 10 ]; then
    ACTIVITY=" | 🧹 Refactoring"
elif [ "$REMOVED" -gt 0 ]; then
    ACTIVITY=" | ✂️ Editing"
else
    ACTIVITY=" | 👀 Reading"
fi

# Git context
GIT_CONTEXT=""
if command -v git >/dev/null 2>&1 && git rev-parse --git-dir >/dev/null 2>&1; then
    BRANCH=$(git branch --show-current 2>/dev/null || echo "")
    
    # Detect type of branch
    if [[ "$BRANCH" == feature/* ]]; then
        GIT_CONTEXT=" | 🚀 Feature"
    elif [[ "$BRANCH" == fix/* ]] || [[ "$BRANCH" == bugfix/* ]]; then
        GIT_CONTEXT=" | 🐛 Bugfix"
    elif [[ "$BRANCH" == hotfix/* ]]; then
        GIT_CONTEXT=" | 🔥 Hotfix"
    elif [[ "$BRANCH" == release/* ]]; then
        GIT_CONTEXT=" | 📦 Release"
    elif [[ "$BRANCH" == main ]] || [[ "$BRANCH" == master ]]; then
        GIT_CONTEXT=" | 🌳 Main"
    elif [ -n "$BRANCH" ]; then
        GIT_CONTEXT=" | 🌿 $BRANCH"
    fi
    
    # Check merge status
    if git status | grep -q "You have unmerged paths"; then
        GIT_CONTEXT="$GIT_CONTEXT ⚠️ MERGING"
    elif git status | grep -q "rebase in progress"; then
        GIT_CONTEXT="$GIT_CONTEXT ♻️ REBASING"
    fi
fi

# Time-based context
HOUR=$(date +%H)
TIME_CONTEXT=""
if [ "$HOUR" -ge 6 ] && [ "$HOUR" -lt 12 ]; then
    TIME_CONTEXT="☕"  # Morning
elif [ "$HOUR" -ge 12 ] && [ "$HOUR" -lt 17 ]; then
    TIME_CONTEXT="☀️"  # Afternoon
elif [ "$HOUR" -ge 17 ] && [ "$HOUR" -lt 21 ]; then
    TIME_CONTEXT="🌅"  # Evening
else
    TIME_CONTEXT="🌙"  # Night
fi

# Performance indicator based on cost
PERF=""
if (( $(echo "$COST < 0.01" | bc -l) )); then
    PERF="⚡"  # Very efficient
elif (( $(echo "$COST < 0.1" | bc -l) )); then
    PERF="✅"  # Good
elif (( $(echo "$COST < 1.0" | bc -l) )); then
    PERF="💵"  # Normal
else
    PERF="💸"  # Expensive
fi

# Special contexts
SPECIAL=""
if [[ "$CWD" == */.claude* ]]; then
    SPECIAL=" | 🎯 Claude Config"
elif [[ "$CWD" == */test* ]] || [[ "$CWD" == */__tests__* ]]; then
    SPECIAL=" | 🧪 Testing"
elif [[ "$CWD" == */docs* ]] || [[ "$CWD" == */documentation* ]]; then
    SPECIAL=" | 📚 Documentation"
elif [[ "$CWD" == */.github* ]]; then
    SPECIAL=" | 🐙 GitHub"
fi

# Build the context-aware statusline
echo "$TIME_CONTEXT [$MODEL] $CONTEXT_EMOJI $CONTEXT$GIT_CONTEXT$ACTIVITY$SPECIAL | $PERF \$$COST"