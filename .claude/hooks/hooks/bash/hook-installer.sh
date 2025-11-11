#!/bin/bash
# Hook Installer Hook
# ===================
# Type: UserPromptSubmit
# Description: Detects when user wants to install hooks and automates the process
#
# This hook intercepts prompts about hook installation and automatically
# configures the appropriate hooks without manual menu navigation.

set -e

# Read hook data from stdin
HOOK_DATA=$(cat)
PROMPT=$(echo "$HOOK_DATA" | jq -r '.prompt // ""')
PROJECT_DIR=$(echo "$HOOK_DATA" | jq -r '.cwd // "."')

# Check if prompt is about installing hooks
if ! echo "$PROMPT" | grep -iE "(install|add|setup|configure).*(hook|hooks)" >/dev/null 2>&1; then
    # Not a hook installation request
    exit 0
fi

# Function to add hook to settings
add_hook_to_settings() {
    local settings_file=$1
    local event=$2
    local matcher=$3
    local command=$4
    local timeout=${5:-30}
    
    # Ensure settings file exists
    if [ ! -f "$settings_file" ]; then
        echo '{"hooks": {}}' > "$settings_file"
    fi
    
    # Use Python to safely modify JSON
    python3 << EOF
import json
import sys

with open('$settings_file', 'r') as f:
    settings = json.load(f)

if 'hooks' not in settings:
    settings['hooks'] = {}

if '$event' not in settings['hooks']:
    settings['hooks']['$event'] = []

hook_config = {
    'hooks': [{
        'type': 'command',
        'command': '$command'
    }]
}

if $timeout > 0:
    hook_config['hooks'][0]['timeout'] = $timeout

if '$matcher' and '$event' in ['PreToolUse', 'PostToolUse']:
    hook_config['matcher'] = '$matcher'

# Check for duplicates
duplicate = False
for existing in settings['hooks']['$event']:
    if existing.get('hooks', [{}])[0].get('command') == '$command':
        duplicate = True
        break

if not duplicate:
    settings['hooks']['$event'].append(hook_config)
    
    with open('$settings_file', 'w') as f:
        json.dump(settings, f, indent=2)
    
    print(f"✓ Added hook to $event")
else:
    print(f"⚠ Hook already exists in $event")
EOF
}

# Detect what type of hooks to install from prompt
install_type=""
if echo "$PROMPT" | grep -iE "logging|log.*commands|bash.*log" >/dev/null 2>&1; then
    install_type="logging"
elif echo "$PROMPT" | grep -iE "lint|format|quality" >/dev/null 2>&1; then
    install_type="quality"
elif echo "$PROMPT" | grep -iE "context|enhance|smart" >/dev/null 2>&1; then
    install_type="context"
elif echo "$PROMPT" | grep -iE "subagent|task" >/dev/null 2>&1; then
    install_type="subagent"
elif echo "$PROMPT" | grep -iE "test|coverage" >/dev/null 2>&1; then
    install_type="testing"
fi

# Determine settings file location
SETTINGS_FILE=""
if echo "$PROMPT" | grep -iE "user|global|all.*projects" >/dev/null 2>&1; then
    SETTINGS_FILE="$HOME/.claude/settings.json"
    mkdir -p "$HOME/.claude"
elif echo "$PROMPT" | grep -iE "local|this.*project|current" >/dev/null 2>&1; then
    SETTINGS_FILE="$PROJECT_DIR/.claude/settings.local.json"
    mkdir -p "$PROJECT_DIR/.claude"
else
    SETTINGS_FILE="$PROJECT_DIR/.claude/settings.json"
    mkdir -p "$PROJECT_DIR/.claude"
fi

# Install appropriate hooks based on type
case "$install_type" in
    logging)
        echo "Installing logging hooks to $SETTINGS_FILE..."
        add_hook_to_settings "$SETTINGS_FILE" "PreToolUse" "Bash" \
            'jq -r "\(.tool_input.command) - \(.tool_input.description // \"No description\")" >> ~/.claude/bash-command-log.txt' 0
        echo "Bash command logging hook installed!"
        ;;
        
    quality)
        echo "Installing quality assurance hooks to $SETTINGS_FILE..."
        add_hook_to_settings "$SETTINGS_FILE" "PostToolUse" "Edit|Write|MultiEdit" \
            "\$CLAUDE_PROJECT_DIR/.claude/hooks/bash/code-linter.sh" 30
        add_hook_to_settings "$SETTINGS_FILE" "PostToolUse" "Edit|Write|MultiEdit" \
            "\$CLAUDE_PROJECT_DIR/.claude/hooks/bash/auto-formatter.sh" 20
        add_hook_to_settings "$SETTINGS_FILE" "Stop" "" \
            "\$CLAUDE_PROJECT_DIR/.claude/hooks/python/work-completion-assistant.py" 20
        echo "Quality assurance hooks installed!"
        ;;
        
    context)
        echo "Installing context enhancement hooks to $SETTINGS_FILE..."
        add_hook_to_settings "$SETTINGS_FILE" "SessionStart" "" \
            "\$CLAUDE_PROJECT_DIR/.claude/hooks/bash/branch-context-loader.sh" 10
        add_hook_to_settings "$SETTINGS_FILE" "UserPromptSubmit" "" \
            "\$CLAUDE_PROJECT_DIR/.claude/hooks/python/prompt-enhancer.py" 10
        echo "Context enhancement hooks installed!"
        ;;
        
    subagent)
        echo "Installing subagent support hooks to $SETTINGS_FILE..."
        add_hook_to_settings "$SETTINGS_FILE" "PreToolUse" "Task" \
            "\$CLAUDE_PROJECT_DIR/.claude/hooks/python/subagent-context-preparer.py" 10
        add_hook_to_settings "$SETTINGS_FILE" "SubagentStop" "" \
            "\$CLAUDE_PROJECT_DIR/.claude/hooks/python/subagent-work-validator.py" 15
        echo "Subagent support hooks installed!"
        ;;
        
    testing)
        echo "Installing testing hooks to $SETTINGS_FILE..."
        add_hook_to_settings "$SETTINGS_FILE" "PostToolUse" "Edit|Write" \
            "\$CLAUDE_PROJECT_DIR/.claude/hooks/bash/test-runner.sh" 60
        add_hook_to_settings "$SETTINGS_FILE" "PostToolUse" "Edit|Write" \
            "\$CLAUDE_PROJECT_DIR/.claude/hooks/python/coverage-gap-finder.py" 30
        echo "Testing hooks installed!"
        ;;
        
    *)
        # Provide helpful context about available hooks
        cat << EOF

[Hook Installation Assistant]

I detected you want to install hooks. Here are the available hook categories:

1. **Logging Hooks** - Track commands and operations
   Example: "Install logging hooks to track bash commands"

2. **Quality Hooks** - Linting, formatting, and validation
   Example: "Install quality assurance hooks for this project"

3. **Context Hooks** - Smart context loading and prompt enhancement
   Example: "Install context enhancement hooks"

4. **Subagent Hooks** - Empower subagents with context
   Example: "Install subagent support hooks"

5. **Testing Hooks** - Automated test running and coverage
   Example: "Install testing hooks for the project"

Specify where to install:
- "user settings" or "global" - All projects
- "local" or "this project" - Current project only

Example: "Install quality hooks to local settings"

EOF
        ;;
esac

# If we installed hooks, provide additional context
if [ -n "$install_type" ]; then
    cat << EOF

[Hooks Installed Successfully]

Settings file: $SETTINGS_FILE

To verify installation:
1. Run: /hooks
2. Or check: cat $SETTINGS_FILE

To test the hooks:
- For logging: Run any bash command and check ~/.claude/bash-command-log.txt
- For quality: Edit a file and watch for linting/formatting
- For context: Start a new session or submit a prompt
- For subagents: Launch a Task tool
- For testing: Edit code files and watch tests run

EOF
fi

exit 0