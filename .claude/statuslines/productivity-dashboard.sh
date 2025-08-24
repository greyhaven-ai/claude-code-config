#!/bin/bash
# Productivity Dashboard statusline
# Shows comprehensive metrics about your coding session

set -euo pipefail

# Read JSON input
input=$(cat 2>/dev/null || echo '{}')

# Extract all metrics
MODEL=$(echo "$input" | jq -r '.model.display_name // "Unknown"' | cut -c1-3)
DIR=$(basename "$(echo "$input" | jq -r '.workspace.current_dir // "."')")
COST=$(echo "$input" | jq -r '.cost.total_cost_usd // 0')
DURATION=$(echo "$input" | jq -r '.cost.total_duration_ms // 0')
API_DURATION=$(echo "$input" | jq -r '.cost.total_api_duration_ms // 0')
ADDED=$(echo "$input" | jq -r '.cost.total_lines_added // 0')
REMOVED=$(echo "$input" | jq -r '.cost.total_lines_removed // 0')

# Calculate productivity metrics
MINUTES=$((DURATION / 60000))
HOURS=$((MINUTES / 60))
MINS=$((MINUTES % 60))

# Lines per minute (productivity rate)
if [ "$MINUTES" -gt 0 ]; then
    LPM=$((ADDED / MINUTES))
else
    LPM=0
fi

# Cost per line
if [ "$ADDED" -gt 0 ]; then
    CPL=$(echo "scale=4; $COST / $ADDED" | bc)
else
    CPL="0"
fi

# API efficiency percentage
if [ "$DURATION" -gt 0 ]; then
    API_PERF=$((API_DURATION * 100 / DURATION))
else
    API_PERF=0
fi

# Net lines (growth)
NET=$((ADDED - REMOVED))

# Productivity score (0-100)
SCORE=50  # Base score

# Adjust based on metrics
if [ "$LPM" -gt 10 ]; then
    SCORE=$((SCORE + 20))
elif [ "$LPM" -gt 5 ]; then
    SCORE=$((SCORE + 10))
fi

if (( $(echo "$CPL < 0.001" | bc -l) )); then
    SCORE=$((SCORE + 10))
elif (( $(echo "$CPL < 0.01" | bc -l) )); then
    SCORE=$((SCORE + 5))
fi

if [ "$API_PERF" -lt 10 ]; then
    SCORE=$((SCORE + 10))
fi

if [ "$NET" -gt 100 ]; then
    SCORE=$((SCORE + 10))
elif [ "$NET" -gt 50 ]; then
    SCORE=$((SCORE + 5))
fi

# Cap at 100
SCORE=$((SCORE > 100 ? 100 : SCORE))

# Choose emoji based on productivity score
if [ "$SCORE" -gt 80 ]; then
    EMOJI="🚀"
    RATING="EXCELLENT"
elif [ "$SCORE" -gt 60 ]; then
    EMOJI="⚡"
    RATING="GOOD"
elif [ "$SCORE" -gt 40 ]; then
    EMOJI="✅"
    RATING="OK"
else
    EMOJI="🐌"
    RATING="SLOW"
fi

# Time display
if [ "$HOURS" -gt 0 ]; then
    TIME_STR="${HOURS}h${MINS}m"
else
    TIME_STR="${MINS}m"
fi

# Create visual score bar (10 segments)
SCORE_BAR=""
for i in $(seq 1 10); do
    if [ $((i * 10)) -le "$SCORE" ]; then
        SCORE_BAR="${SCORE_BAR}█"
    else
        SCORE_BAR="${SCORE_BAR}░"
    fi
done

# Format cost with appropriate precision
if (( $(echo "$COST < 0.01" | bc -l) )); then
    COST_STR=$(printf "%.4f" "$COST")
else
    COST_STR=$(printf "%.2f" "$COST")
fi

# Build the statusline
echo "$EMOJI $RATING [$SCORE_BAR] | $MODEL | 📊 +$ADDED/-$REMOVED (Δ$NET) | ⏱️ $TIME_STR | 💰\$$COST_STR | ⚡${LPM}L/min | 📁 $DIR"