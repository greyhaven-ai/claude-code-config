#!/bin/bash
# Hook Installation Script for Claude Code
# =========================================
# This script automates the installation and configuration of Claude Code hooks
# without requiring manual menu navigation.

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOOKS_SOURCE_DIR="$SCRIPT_DIR/.claude/hooks"
PROJECT_HOOKS_DIR=".claude/hooks"
PROJECT_SETTINGS_FILE=".claude/settings.json"
PROJECT_LOCAL_SETTINGS_FILE=".claude/settings.local.json"
USER_SETTINGS_FILE="$HOME/.claude/settings.json"

# Function to print colored output
print_color() {
    local color=$1
    shift
    echo -e "${color}$@${NC}"
}

# Function to print section headers
print_header() {
    echo ""
    print_color "$PURPLE" "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    print_color "$PURPLE" "$1"
    print_color "$PURPLE" "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

# Function to detect project type
detect_project_type() {
    local project_types=()
    
    [[ -f "package.json" ]] && project_types+=("JavaScript/TypeScript")
    [[ -f "pyproject.toml" ]] && project_types+=("Python")
    [[ -f "go.mod" ]] && project_types+=("Go")
    [[ -f "Cargo.toml" ]] && project_types+=("Rust")
    [[ -f "pom.xml" ]] && project_types+=("Java")
    
    if [ ${#project_types[@]} -eq 0 ]; then
        echo "Generic"
    else
        echo "${project_types[*]}"
    fi
}

# Function to create settings JSON with proper escaping
create_settings_json() {
    local settings_file=$1
    local settings_type=$2  # "minimal", "recommended", "advanced", "custom"
    
    case "$settings_type" in
        minimal)
            cat > "$settings_file" << 'EOF'
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write|MultiEdit",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/bash/code-linter.sh"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/python/work-completion-assistant.py"
          }
        ]
      }
    ]
  }
}
EOF
            ;;
            
        recommended)
            cat > "$settings_file" << 'EOF'
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/bash/branch-context-loader.sh",
            "timeout": 10
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/python/prompt-enhancer.py",
            "timeout": 10
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write|MultiEdit",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/bash/code-linter.sh",
            "timeout": 30
          },
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/bash/auto-formatter.sh",
            "timeout": 20
          },
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/bash/test-runner.sh",
            "timeout": 60
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Task",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/python/subagent-context-preparer.py",
            "timeout": 10
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/python/work-completion-assistant.py",
            "timeout": 20
          }
        ]
      }
    ]
  }
}
EOF
            ;;
            
        advanced)
            cp "$HOOKS_SOURCE_DIR/examples/advanced-workflow-settings.json" "$settings_file"
            ;;
            
        custom)
            # Will be populated by user selections
            echo '{"hooks": {}}' > "$settings_file"
            ;;
    esac
}

# Function to add a hook to settings
add_hook_to_settings() {
    local settings_file=$1
    local event=$2
    local matcher=$3
    local command=$4
    local timeout=$5
    
    # Use jq to add the hook if available, otherwise use Python
    if command -v jq >/dev/null 2>&1; then
        # Complex jq manipulation - build it step by step
        if [ -n "$matcher" ] && [ "$matcher" != "*" ]; then
            jq --arg event "$event" \
               --arg matcher "$matcher" \
               --arg command "$command" \
               --arg timeout "$timeout" \
               '.hooks[$event] = ((.hooks[$event] // []) + [{
                   matcher: $matcher,
                   hooks: [{
                       type: "command",
                       command: $command,
                       timeout: ($timeout | tonumber)
                   }]
               }])' "$settings_file" > "$settings_file.tmp" && mv "$settings_file.tmp" "$settings_file"
        else
            jq --arg event "$event" \
               --arg command "$command" \
               --arg timeout "$timeout" \
               '.hooks[$event] = ((.hooks[$event] // []) + [{
                   hooks: [{
                       type: "command",
                       command: $command,
                       timeout: ($timeout | tonumber)
                   }]
               }])' "$settings_file" > "$settings_file.tmp" && mv "$settings_file.tmp" "$settings_file"
        fi
    else
        # Fallback to Python
        python3 -c "
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

if '$timeout':
    hook_config['hooks'][0]['timeout'] = int('$timeout')

if '$matcher' and '$matcher' != '*':
    hook_config['matcher'] = '$matcher'

settings['hooks']['$event'].append(hook_config)

with open('$settings_file', 'w') as f:
    json.dump(settings, f, indent=2)
"
    fi
}

# Function to install hook files
install_hook_files() {
    print_header "Installing Hook Files"
    
    # Create .claude directory if it doesn't exist
    mkdir -p "$PROJECT_HOOKS_DIR"
    
    # Copy hook files
    if [ -d "$HOOKS_SOURCE_DIR" ]; then
        print_color "$BLUE" "Copying hooks from $HOOKS_SOURCE_DIR..."
        cp -r "$HOOKS_SOURCE_DIR"/* "$PROJECT_HOOKS_DIR/" 2>/dev/null || true
        
        # Make all hooks executable
        find "$PROJECT_HOOKS_DIR" -type f \( -name "*.sh" -o -name "*.py" -o -name "*.js" \) -exec chmod +x {} \;
        
        print_color "$GREEN" "✓ Hook files installed to $PROJECT_HOOKS_DIR"
    else
        print_color "$RED" "✗ Source hooks directory not found at $HOOKS_SOURCE_DIR"
        exit 1
    fi
}

# Function to select hooks interactively
select_hooks_interactive() {
    local settings_file=$1
    
    print_header "Interactive Hook Selection"
    
    # Define available hooks
    declare -A hook_descriptions=(
        ["branch-context-loader.sh"]="Load context based on git branch (SessionStart)"
        ["prompt-enhancer.py"]="Enhance prompts with relevant context (UserPromptSubmit)"
        ["code-linter.sh"]="Run appropriate linters after edits (PostToolUse)"
        ["auto-formatter.sh"]="Format code automatically (PostToolUse)"
        ["test-runner.sh"]="Run affected tests (PostToolUse)"
        ["incremental-type-checker.sh"]="Check types incrementally (PostToolUse)"
        ["work-completion-assistant.py"]="Ensure work is complete (Stop)"
        ["subagent-context-preparer.py"]="Prepare context for subagents (PreToolUse:Task)"
        ["subagent-work-validator.py"]="Validate subagent work (SubagentStop)"
        ["security-validator.py"]="Validate security issues (PreToolUse)"
        ["pre-commit-runner.sh"]="Run pre-commit hooks (PostToolUse)"
    )
    
    declare -A hook_events=(
        ["branch-context-loader.sh"]="SessionStart"
        ["prompt-enhancer.py"]="UserPromptSubmit"
        ["code-linter.sh"]="PostToolUse"
        ["auto-formatter.sh"]="PostToolUse"
        ["test-runner.sh"]="PostToolUse"
        ["incremental-type-checker.sh"]="PostToolUse"
        ["work-completion-assistant.py"]="Stop"
        ["subagent-context-preparer.py"]="PreToolUse"
        ["subagent-work-validator.py"]="SubagentStop"
        ["security-validator.py"]="PreToolUse"
        ["pre-commit-runner.sh"]="PostToolUse"
    )
    
    declare -A hook_matchers=(
        ["code-linter.sh"]="Edit|Write|MultiEdit"
        ["auto-formatter.sh"]="Edit|Write|MultiEdit"
        ["test-runner.sh"]="Edit|Write"
        ["incremental-type-checker.sh"]="Edit|Write|MultiEdit"
        ["subagent-context-preparer.py"]="Task"
        ["security-validator.py"]="Edit|Write"
        ["pre-commit-runner.sh"]="Edit|Write|MultiEdit"
    )
    
    echo '{"hooks": {}}' > "$settings_file"
    
    print_color "$YELLOW" "Select hooks to install (y/n for each):"
    echo ""
    
    for hook in "${!hook_descriptions[@]}"; do
        echo -n "Install ${hook_descriptions[$hook]}? (y/n): "
        read -r response
        
        if [[ "$response" =~ ^[Yy]$ ]]; then
            local event="${hook_events[$hook]}"
            local matcher="${hook_matchers[$hook]:-}"
            local lang=$(echo "$hook" | grep -oE '\.(sh|py|js)$' | cut -d. -f2)
            local command_path="\$CLAUDE_PROJECT_DIR/.claude/hooks/$lang/$hook"
            
            add_hook_to_settings "$settings_file" "$event" "$matcher" "$command_path" "30"
            print_color "$GREEN" "  ✓ Added $hook"
        fi
    done
}

# Main installation function
main() {
    print_header "Claude Code Hook Installer"
    
    # Check if we're in a git repository or project directory
    if [ ! -d ".git" ] && [ ! -f "package.json" ] && [ ! -f "pyproject.toml" ]; then
        print_color "$YELLOW" "⚠️  Warning: Not in a recognized project directory"
        echo -n "Continue anyway? (y/n): "
        read -r response
        [[ ! "$response" =~ ^[Yy]$ ]] && exit 0
    fi
    
    # Detect project type
    local project_type=$(detect_project_type)
    print_color "$BLUE" "Project type detected: $project_type"
    
    # Install hook files
    install_hook_files
    
    # Choose installation mode
    print_header "Choose Installation Mode"
    echo "1) Minimal - Basic linting and completion checks"
    echo "2) Recommended - Context, enhancement, quality checks"
    echo "3) Advanced - Full workflow automation"
    echo "4) Custom - Select individual hooks"
    echo "5) Skip settings - Just install hook files"
    echo ""
    echo -n "Select mode (1-5): "
    read -r mode
    
    local settings_file="$PROJECT_LOCAL_SETTINGS_FILE"
    
    case "$mode" in
        1)
            print_color "$BLUE" "Installing minimal hook configuration..."
            create_settings_json "$settings_file" "minimal"
            ;;
        2)
            print_color "$BLUE" "Installing recommended hook configuration..."
            create_settings_json "$settings_file" "recommended"
            ;;
        3)
            print_color "$BLUE" "Installing advanced hook configuration..."
            create_settings_json "$settings_file" "advanced"
            ;;
        4)
            select_hooks_interactive "$settings_file"
            ;;
        5)
            print_color "$YELLOW" "Skipping settings configuration"
            settings_file=""
            ;;
        *)
            print_color "$RED" "Invalid selection"
            exit 1
            ;;
    esac
    
    # Create example user hooks if requested
    print_header "Additional Setup"
    echo -n "Create example user-level hooks in ~/.claude/settings.json? (y/n): "
    read -r response
    
    if [[ "$response" =~ ^[Yy]$ ]]; then
        mkdir -p "$HOME/.claude"
        
        if [ ! -f "$USER_SETTINGS_FILE" ]; then
            echo '{"hooks": {}}' > "$USER_SETTINGS_FILE"
        fi
        
        # Add simple logging hook
        add_hook_to_settings "$USER_SETTINGS_FILE" "PreToolUse" "Bash" \
            'jq -r "\(.tool_input.command) - \(.tool_input.description // \"No description\")" >> ~/.claude/bash-command-log.txt' ""
        
        print_color "$GREEN" "✓ Added example logging hook to user settings"
    fi
    
    # Final instructions
    print_header "Installation Complete!"
    
    print_color "$GREEN" "✓ Hooks installed to: $PROJECT_HOOKS_DIR"
    [ -n "$settings_file" ] && print_color "$GREEN" "✓ Settings saved to: $settings_file"
    
    echo ""
    print_color "$YELLOW" "Next steps:"
    echo "1. Review the installed hooks in $PROJECT_HOOKS_DIR"
    echo "2. Test hooks with: claude --debug"
    echo "3. View current hooks in Claude Code with: /hooks"
    echo "4. Customize settings in: $settings_file"
    
    if [ "$project_type" == "Python" ]; then
        echo ""
        print_color "$YELLOW" "Python users: Make sure you have 'uv' installed for Python hooks"
    fi
    
    if [[ "$project_type" == *"JavaScript"* ]]; then
        echo ""
        print_color "$YELLOW" "JavaScript users: Hooks support both npm and bun"
    fi
    
    echo ""
    print_color "$PURPLE" "Happy coding with intelligent hooks! 🚀"
}

# Run main function
main "$@"