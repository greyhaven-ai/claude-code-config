# Claude Code Statusline Configurations

This directory contains various statusline scripts for Claude Code. Each script provides different information and visual styles.

## Available Statuslines

### 🏰 grey-haven-default.sh
**Description**: Grey Haven Studio's default statusline with comprehensive information  
**Shows**: Model, Git branch & status, Directory, Cost, Lines changed  
**Best for**: General development with git integration

### 🎮 tamagotchi.sh
**Description**: A virtual pet that evolves based on your coding activity!  
**Shows**: Pet status, mood, level, health bars, activity indicators  
**Best for**: Fun and engaging coding sessions, gamification

### 📊 productivity-dashboard.sh
**Description**: Comprehensive productivity metrics dashboard  
**Shows**: Productivity score, lines/minute, cost/line, time tracking  
**Best for**: Tracking coding efficiency and performance

### ⚡ minimalist.sh
**Description**: Ultra-minimal display with just essentials  
**Shows**: Model initial and current directory  
**Best for**: Distraction-free coding, maximum screen space

### 🎯 context-aware.sh
**Description**: Adapts display based on current context and activity  
**Shows**: Language context, git workflow, time of day, activity type  
**Best for**: Developers working across multiple projects and languages

## Installation

1. Make the script executable:
```bash
chmod +x ~/.claude/statuslines/[script-name].sh
```

2. Add to your `.claude/settings.json`:
```json
{
  "statusLine": {
    "type": "command",
    "command": "~/.claude/statuslines/grey-haven-default.sh",
    "padding": 0
  }
}
```

## Quick Setup Commands

```bash
# Set Grey Haven default
echo '{"statusLine":{"type":"command","command":"~/.claude/statuslines/grey-haven-default.sh","padding":0}}' > ~/.claude/settings.json

# Set Tamagotchi
echo '{"statusLine":{"type":"command","command":"~/.claude/statuslines/tamagotchi.sh","padding":0}}' > ~/.claude/settings.json

# Set Productivity Dashboard
echo '{"statusLine":{"type":"command","command":"~/.claude/statuslines/productivity-dashboard.sh","padding":0}}' > ~/.claude/settings.json

# Set Context-Aware
echo '{"statusLine":{"type":"command","command":"~/.claude/statuslines/context-aware.sh","padding":0}}' > ~/.claude/settings.json

# Set Minimalist
echo '{"statusLine":{"type":"command","command":"~/.claude/statuslines/minimalist.sh","padding":0}}' > ~/.claude/settings.json
```

## Inline Statuslines (No Script File Needed)

You can also define statuslines directly in `settings.json`:

### Simple Model + Directory
```json
{
  "statusLine": {
    "type": "command",
    "command": "bash -c 'input=$(cat); echo \"[$(echo \"$input\" | jq -r \".model.display_name\")] $(basename $(echo \"$input\" | jq -r \".workspace.current_dir\"))\"'",
    "padding": 0
  }
}
```

### With Git Branch
```json
{
  "statusLine": {
    "type": "command",
    "command": "bash -c 'input=$(cat); MODEL=$(echo \"$input\" | jq -r \".model.display_name\"); DIR=$(basename $(echo \"$input\" | jq -r \".workspace.current_dir\")); BRANCH=$(git branch --show-current 2>/dev/null || echo \"\"); if [ -n \"$BRANCH\" ]; then BRANCH=\" | 🌿 $BRANCH\"; fi; echo \"[$MODEL] 📁 $DIR$BRANCH\"'",
    "padding": 0
  }
}
```

## Customization Tips

### Adding Colors
Use ANSI color codes in your scripts:
```bash
# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RESET='\033[0m'

echo -e "${GREEN}✅ Success${RESET}"
```

### Using Emojis
Most terminals support emojis. Common ones for statuslines:
- Models: 🧠 (Opus), 🎵 (Sonnet), 🍃 (Haiku)
- Git: 🌿 (branch), ✅ (clean), 🔴 (dirty)
- Files: 📁 (directory), 📄 (file), 📝 (editing)
- Status: ⚡ (fast), 💰 (cost), ⏱️ (time)
- Alerts: ⚠️ (warning), 🔥 (hot), 💸 (expensive)

### Performance Considerations
- Keep scripts under 300ms execution time
- Cache expensive operations (git status, file counts)
- Use `timeout` for external commands
- Avoid network calls unless cached

## Testing Your Statusline

Test with mock JSON input:
```bash
echo '{
  "model": {"display_name": "Opus"},
  "workspace": {"current_dir": "/home/user/project"},
  "cost": {
    "total_cost_usd": 0.15,
    "total_lines_added": 150,
    "total_lines_removed": 20
  }
}' | ~/.claude/statuslines/grey-haven-default.sh
```

## Creating Your Own

1. Create a new script in `~/.claude/statuslines/`
2. Read JSON from stdin: `input=$(cat)`
3. Extract data with jq: `MODEL=$(echo "$input" | jq -r '.model.display_name')`
4. Output to stdout: `echo "Your statusline text"`
5. Make executable: `chmod +x your-script.sh`
6. Add to settings.json

## Available JSON Fields

```json
{
  "hook_event_name": "Status",
  "session_id": "unique-session-id",
  "transcript_path": "/path/to/transcript.json",
  "cwd": "/current/working/directory",
  "model": {
    "id": "claude-opus-4-1",
    "display_name": "Opus"
  },
  "workspace": {
    "current_dir": "/current/working/directory",
    "project_dir": "/original/project/directory"
  },
  "version": "1.0.80",
  "output_style": {
    "name": "default"
  },
  "cost": {
    "total_cost_usd": 0.01234,
    "total_duration_ms": 45000,
    "total_api_duration_ms": 2300,
    "total_lines_added": 156,
    "total_lines_removed": 23
  }
}
```

## Troubleshooting

### Statusline not appearing
- Check script is executable: `ls -la ~/.claude/statuslines/`
- Verify path in settings.json is correct
- Test script manually with mock input

### Errors or wrong output
- Check jq is installed: `which jq`
- Ensure output goes to stdout, not stderr
- Add error handling: `2>/dev/null`

### Performance issues
- Profile your script: `time ./your-script.sh < test-input.json`
- Cache expensive operations
- Reduce external command calls