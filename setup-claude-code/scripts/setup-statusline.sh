#!/bin/bash
# Setup script for Claude Code statuslines
# This script helps you install and configure a statusline for Claude Code

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RESET='\033[0m'

# Claude directory
CLAUDE_DIR="$HOME/.claude"
STATUSLINES_DIR="$CLAUDE_DIR/statuslines"
SETTINGS_FILE="$CLAUDE_DIR/settings.json"
REPO_STATUSLINES_DIR="$(dirname "$0")/.claude/statuslines"

echo -e "${BLUE}╔════════════════════════════════════════╗${RESET}"
echo -e "${BLUE}║   Claude Code Statusline Setup        ║${RESET}"
echo -e "${BLUE}║   🏰 Grey Haven Studio                 ║${RESET}"
echo -e "${BLUE}╚════════════════════════════════════════╝${RESET}"
echo

# Create directories if they don't exist
echo -e "${CYAN}Setting up directories...${RESET}"
mkdir -p "$STATUSLINES_DIR"

# Copy statusline scripts
echo -e "${CYAN}Installing statusline scripts...${RESET}"
if [ -d "$REPO_STATUSLINES_DIR" ]; then
    cp -r "$REPO_STATUSLINES_DIR"/*.sh "$STATUSLINES_DIR/" 2>/dev/null || true
    chmod +x "$STATUSLINES_DIR"/*.sh 2>/dev/null || true
    echo -e "${GREEN}✓ Statusline scripts installed${RESET}"
else
    echo -e "${YELLOW}⚠ Statusline scripts directory not found. Skipping copy.${RESET}"
fi

# Function to display statusline options
show_options() {
    echo -e "\n${CYAN}Available Statuslines:${RESET}"
    echo
    echo -e "${GREEN}1)${RESET} 🏰 Grey Haven Default"
    echo "   Shows: Model, Git status, Directory, Cost, Lines changed"
    echo
    echo -e "${GREEN}2)${RESET} 🎮 Tamagotchi"
    echo "   A virtual pet that evolves with your coding!"
    echo
    echo -e "${GREEN}3)${RESET} 📊 Productivity Dashboard"
    echo "   Comprehensive metrics and productivity scoring"
    echo
    echo -e "${GREEN}4)${RESET} 🎯 Context Aware"
    echo "   Adapts based on language and current activity"
    echo
    echo -e "${GREEN}5)${RESET} ⚡ Minimalist"
    echo "   Just model and directory - clean and simple"
    echo
    echo -e "${GREEN}6)${RESET} 📝 Simple Inline (no script file)"
    echo "   Basic model and directory display"
    echo
    echo -e "${GREEN}7)${RESET} 🌿 Git Inline (no script file)"
    echo "   Model, directory, and git branch"
    echo
    echo -e "${GREEN}8)${RESET} 💰 Cost Tracker Inline (no script file)"
    echo "   Model and session cost"
    echo
    echo -e "${GREEN}9)${RESET} 🎨 Colorful Inline (no script file)"
    echo "   Model and directory with colors"
    echo
    echo -e "${GREEN}10)${RESET} 🕐 Time-based Inline (no script file)"
    echo "   Shows time with day/night emoji"
    echo
    echo -e "${GREEN}0)${RESET} ❌ None (remove statusline)"
    echo
}

# Function to apply statusline configuration
apply_statusline() {
    local choice=$1
    local config=""
    
    case $choice in
        1)
            config='{"statusLine":{"type":"command","command":"~/.claude/statuslines/grey-haven-default.sh","padding":0}}'
            echo -e "${GREEN}✓ Grey Haven Default statusline configured${RESET}"
            ;;
        2)
            config='{"statusLine":{"type":"command","command":"~/.claude/statuslines/tamagotchi.sh","padding":0}}'
            echo -e "${GREEN}✓ Tamagotchi statusline configured${RESET}"
            echo -e "${YELLOW}Tip: Your pet will evolve as you code!${RESET}"
            ;;
        3)
            config='{"statusLine":{"type":"command","command":"~/.claude/statuslines/productivity-dashboard.sh","padding":0}}'
            echo -e "${GREEN}✓ Productivity Dashboard configured${RESET}"
            ;;
        4)
            config='{"statusLine":{"type":"command","command":"~/.claude/statuslines/context-aware.sh","padding":0}}'
            echo -e "${GREEN}✓ Context Aware statusline configured${RESET}"
            ;;
        5)
            config='{"statusLine":{"type":"command","command":"~/.claude/statuslines/minimalist.sh","padding":0}}'
            echo -e "${GREEN}✓ Minimalist statusline configured${RESET}"
            ;;
        6)
            config='{"statusLine":{"type":"command","command":"bash -c '\''input=$(cat); echo \"[$(echo \"$input\" | jq -r \".model.display_name\")] 📁 $(basename $(echo \"$input\" | jq -r \".workspace.current_dir\"))\"'\''","padding":0}}'
            echo -e "${GREEN}✓ Simple inline statusline configured${RESET}"
            ;;
        7)
            config='{"statusLine":{"type":"command","command":"bash -c '\''input=$(cat); MODEL=$(echo \"$input\" | jq -r \".model.display_name\"); DIR=$(basename $(echo \"$input\" | jq -r \".workspace.current_dir\")); BRANCH=$(git branch --show-current 2>/dev/null || echo \"\"); if [ -n \"$BRANCH\" ]; then BRANCH=\" | 🌿 $BRANCH\"; fi; echo \"[$MODEL] 📁 $DIR$BRANCH\"'\''","padding":0}}'
            echo -e "${GREEN}✓ Git inline statusline configured${RESET}"
            ;;
        8)
            config='{"statusLine":{"type":"command","command":"bash -c '\''input=$(cat); MODEL=$(echo \"$input\" | jq -r \".model.display_name\"); COST=$(echo \"$input\" | jq -r \".cost.total_cost_usd // 0\" | xargs printf \"%.4f\"); echo \"[$MODEL] 💰 \\$$COST\"'\''","padding":0}}'
            echo -e "${GREEN}✓ Cost tracker inline statusline configured${RESET}"
            ;;
        9)
            config='{"statusLine":{"type":"command","command":"bash -c '\''input=$(cat); MODEL=$(echo \"$input\" | jq -r \".model.display_name\"); DIR=$(basename $(echo \"$input\" | jq -r \".workspace.current_dir\")); echo -e \"\\033[1;36m[$MODEL]\\033[0m \\033[1;33m📁 $DIR\\033[0m\"'\''","padding":0}}'
            echo -e "${GREEN}✓ Colorful inline statusline configured${RESET}"
            ;;
        10)
            config='{"statusLine":{"type":"command","command":"bash -c '\''input=$(cat); MODEL=$(echo \"$input\" | jq -r \".model.display_name\"); HOUR=$(date +%H); if [ $HOUR -ge 6 ] && [ $HOUR -lt 12 ]; then EMOJI=\"☕\"; elif [ $HOUR -ge 12 ] && [ $HOUR -lt 17 ]; then EMOJI=\"☀️\"; elif [ $HOUR -ge 17 ] && [ $HOUR -lt 21 ]; then EMOJI=\"🌅\"; else EMOJI=\"🌙\"; fi; echo \"$EMOJI [$MODEL] $(date +%H:%M)\"'\''","padding":0}}'
            echo -e "${GREEN}✓ Time-based inline statusline configured${RESET}"
            ;;
        0)
            config='{}'
            echo -e "${GREEN}✓ Statusline removed${RESET}"
            ;;
        *)
            echo -e "${RED}Invalid choice${RESET}"
            return 1
            ;;
    esac
    
    # Check if settings file exists and has content
    if [ -f "$SETTINGS_FILE" ] && [ -s "$SETTINGS_FILE" ]; then
        # Backup existing settings
        cp "$SETTINGS_FILE" "$SETTINGS_FILE.backup"
        echo -e "${CYAN}Backed up existing settings to $SETTINGS_FILE.backup${RESET}"
        
        # Merge with existing settings (requires jq)
        if command -v jq >/dev/null 2>&1; then
            # Merge configurations
            existing=$(cat "$SETTINGS_FILE")
            merged=$(echo "$existing" | jq ". + $config")
            echo "$merged" > "$SETTINGS_FILE"
        else
            # Without jq, replace the file
            echo "$config" > "$SETTINGS_FILE"
            echo -e "${YELLOW}Note: Replaced settings file (jq not found for merging)${RESET}"
        fi
    else
        # Create new settings file
        echo "$config" > "$SETTINGS_FILE"
    fi
}

# Main menu
show_options

echo -n -e "${CYAN}Choose a statusline (0-10): ${RESET}"
read -r choice

apply_statusline "$choice"

echo
echo -e "${BLUE}═══════════════════════════════════════${RESET}"
echo -e "${GREEN}Setup complete!${RESET}"
echo
echo -e "${CYAN}Your statusline is now configured.${RESET}"
echo -e "${CYAN}Restart Claude Code or open a new session to see changes.${RESET}"
echo
echo -e "${YELLOW}Tips:${RESET}"
echo -e "• Run this script again to change your statusline"
echo -e "• Edit $SETTINGS_FILE to customize further"
echo -e "• Check $STATUSLINES_DIR for script files"
echo -e "• Test statuslines with: ${CYAN}echo '{\"model\":{\"display_name\":\"Test\"}}' | ~/.claude/statuslines/[script].sh${RESET}"
echo
echo -e "${BLUE}🏰 Happy coding with Grey Haven Studio!${RESET}"