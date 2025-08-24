#!/bin/bash
# Tamagotchi-style statusline for Claude Code
# Your AI pet that evolves based on your coding activity!

set -euo pipefail

# Read JSON input from stdin
input=$(cat 2>/dev/null || echo '{}')

# Extract values
MODEL=$(echo "$input" | jq -r '.model.display_name // "Unknown"')
DIR=$(basename "$(echo "$input" | jq -r '.workspace.current_dir // "."')")
COST=$(echo "$input" | jq -r '.cost.total_cost_usd // 0')
DURATION=$(echo "$input" | jq -r '.cost.total_duration_ms // 0')
ADDED=$(echo "$input" | jq -r '.cost.total_lines_added // 0')
REMOVED=$(echo "$input" | jq -r '.cost.total_lines_removed // 0')
SESSION_ID=$(echo "$input" | jq -r '.session_id // "unknown"')

# State file for persistence (unique per session)
STATE_FILE="/tmp/claude-tamagotchi-${SESSION_ID}.state"

# Initialize or read state
if [ -f "$STATE_FILE" ]; then
    source "$STATE_FILE"
else
    # Initial state
    HAPPINESS=50
    ENERGY=100
    EXPERIENCE=0
    LEVEL=1
    LAST_UPDATE=$(date +%s)
    FOOD_COUNT=0
    PET_NAME="Claude"
fi

# Current time
NOW=$(date +%s)
TIME_DIFF=$((NOW - LAST_UPDATE))

# Calculate changes based on activity
MINUTES=$((DURATION / 60000))

# Happiness changes based on lines of code written
if [ "$ADDED" -gt 100 ]; then
    HAPPINESS=$((HAPPINESS + 10))
    EXPERIENCE=$((EXPERIENCE + 20))
elif [ "$ADDED" -gt 50 ]; then
    HAPPINESS=$((HAPPINESS + 5))
    EXPERIENCE=$((EXPERIENCE + 10))
elif [ "$ADDED" -gt 10 ]; then
    HAPPINESS=$((HAPPINESS + 2))
    EXPERIENCE=$((EXPERIENCE + 5))
elif [ "$ADDED" -gt 0 ]; then
    HAPPINESS=$((HAPPINESS + 1))
    EXPERIENCE=$((EXPERIENCE + 2))
fi

# Energy decreases over time (needs rest)
if [ "$TIME_DIFF" -gt 3600 ]; then
    # More than an hour since last update
    ENERGY=$((ENERGY - 30))
elif [ "$TIME_DIFF" -gt 1800 ]; then
    # More than 30 minutes
    ENERGY=$((ENERGY - 15))
elif [ "$TIME_DIFF" -gt 300 ]; then
    # More than 5 minutes
    ENERGY=$((ENERGY - 5))
fi

# Energy recovers with breaks
if [ "$TIME_DIFF" -gt 7200 ]; then
    # More than 2 hours - had a good rest!
    ENERGY=100
    HAPPINESS=$((HAPPINESS + 10))
fi

# Cost affects mood (feeding the pet)
if (( $(echo "$COST > 0.01" | bc -l) )); then
    FOOD_COUNT=$((FOOD_COUNT + 1))
    ENERGY=$((ENERGY + 5))
fi

# Git activity affects happiness
if command -v git >/dev/null 2>&1 && git rev-parse --git-dir >/dev/null 2>&1; then
    if ! git diff --quiet 2>/dev/null; then
        # Has uncommitted changes - pet is worried
        HAPPINESS=$((HAPPINESS - 2))
    fi
    
    # Check for recent commits
    RECENT_COMMITS=$(git log --since="1 hour ago" --oneline 2>/dev/null | wc -l | tr -d ' ')
    if [ "$RECENT_COMMITS" -gt 0 ]; then
        HAPPINESS=$((HAPPINESS + 5))
        EXPERIENCE=$((EXPERIENCE + 10))
    fi
fi

# Level up based on experience
if [ "$EXPERIENCE" -ge 100 ]; then
    LEVEL=$((LEVEL + 1))
    EXPERIENCE=$((EXPERIENCE - 100))
    HAPPINESS=100  # Level up bonus!
fi

# Constrain values
HAPPINESS=$((HAPPINESS > 100 ? 100 : HAPPINESS < 0 ? 0 : HAPPINESS))
ENERGY=$((ENERGY > 100 ? 100 : ENERGY < 0 ? 0 : ENERGY))
EXPERIENCE=$((EXPERIENCE > 100 ? 100 : EXPERIENCE < 0 ? 0 : EXPERIENCE))

# Choose pet appearance based on state
if [ "$ENERGY" -lt 20 ]; then
    # Tired
    PET="😴"
    MOOD="sleepy"
elif [ "$HAPPINESS" -gt 80 ] && [ "$ENERGY" -gt 50 ]; then
    # Very happy and energetic
    case "$LEVEL" in
        1) PET="🐣" ;;  # Baby
        2) PET="🐥" ;;  # Young
        3) PET="🐤" ;;  # Growing
        4) PET="🐦" ;;  # Adult
        5) PET="🦅" ;;  # Advanced
        6) PET="🦜" ;;  # Expert
        7) PET="🦚" ;;  # Master
        8) PET="🐉" ;;  # Dragon form!
        *) PET="👑" ;;  # Legendary
    esac
    MOOD="happy"
elif [ "$HAPPINESS" -gt 50 ]; then
    # Content
    case "$LEVEL" in
        1|2) PET="🐣" ;;
        3|4) PET="🐦" ;;
        *) PET="🦉" ;;
    esac
    MOOD="content"
elif [ "$HAPPINESS" -gt 20 ]; then
    # Okay
    PET="😐"
    MOOD="meh"
else
    # Sad
    PET="😢"
    MOOD="sad"
fi

# Activity indicator
ACTIVITY=""
if [ "$ADDED" -gt 0 ]; then
    ACTIVITY="✨"  # Creating
elif [ "$REMOVED" -gt 0 ]; then
    ACTIVITY="🧹"  # Cleaning
elif git diff --quiet 2>/dev/null; then
    ACTIVITY="💭"  # Thinking
else
    ACTIVITY="🔧"  # Working
fi

# Health bars
HAPPINESS_BAR=""
ENERGY_BAR=""
EXP_BAR=""

# Create visual bars (5 segments each)
for i in 1 2 3 4 5; do
    if [ $((i * 20)) -le "$HAPPINESS" ]; then
        HAPPINESS_BAR="${HAPPINESS_BAR}❤️"
    else
        HAPPINESS_BAR="${HAPPINESS_BAR}🤍"
    fi
    
    if [ $((i * 20)) -le "$ENERGY" ]; then
        ENERGY_BAR="${ENERGY_BAR}⚡"
    else
        ENERGY_BAR="${ENERGY_BAR}💤"
    fi
    
    if [ $((i * 20)) -le "$EXPERIENCE" ]; then
        EXP_BAR="${EXP_BAR}⭐"
    else
        EXP_BAR="${EXP_BAR}☆"
    fi
done

# Special events
EVENT=""
if [ "$LEVEL" -gt "$(($(cat "$STATE_FILE" 2>/dev/null | grep "LEVEL=" | cut -d= -f2) + 0))" ]; then
    EVENT=" 🎉 LEVEL UP!"
elif [ "$FOOD_COUNT" -eq 10 ]; then
    EVENT=" 🍰 Well fed!"
elif [ "$HAPPINESS" -eq 100 ]; then
    EVENT=" 💕 MAX JOY!"
elif [ "$ENERGY" -lt 10 ]; then
    EVENT=" 😫 Need rest!"
fi

# Save state
cat > "$STATE_FILE" << EOF
HAPPINESS=$HAPPINESS
ENERGY=$ENERGY
EXPERIENCE=$EXPERIENCE
LEVEL=$LEVEL
LAST_UPDATE=$NOW
FOOD_COUNT=$FOOD_COUNT
PET_NAME="$PET_NAME"
EOF

# Choose output format based on level
if [ "$LEVEL" -lt 3 ]; then
    # Simple format for beginners
    echo "$PET Lv.$LEVEL $ACTIVITY [$MODEL] 📁 $DIR | Mood: $MOOD$EVENT"
elif [ "$LEVEL" -lt 6 ]; then
    # Intermediate format with bars
    echo "$PET Lv.$LEVEL $HAPPINESS_BAR $ENERGY_BAR | [$MODEL] 📁 $DIR$EVENT"
else
    # Advanced format with all stats
    echo "$PET Lv.$LEVEL HP:$HAPPINESS_BAR EN:$ENERGY_BAR XP:$EXP_BAR | [$MODEL] $ACTIVITY $DIR$EVENT"
fi