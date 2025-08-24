#!/bin/bash

# Setup Integrated Hooks, Commands, and Subagents Workflow
# This script configures your project with intelligent hook-command-subagent integration

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR=".claude"
CONFIG_FILE="$CLAUDE_DIR/settings.local.json"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔══════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     Claude Code Integrated Workflow Setup           ║${NC}"
echo -e "${BLUE}║   Hooks + Commands + Subagents = Intelligence      ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════╝${NC}"
echo

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to detect project type
detect_project_type() {
    local types=()
    
    [[ -f "package.json" ]] && types+=("javascript")
    [[ -f "pyproject.toml" || -f "requirements.txt" || -f "setup.py" ]] && types+=("python")
    [[ -f "Cargo.toml" ]] && types+=("rust")
    [[ -f "go.mod" ]] && types+=("go")
    
    echo "${types[@]}"
}

# Function to select workflow presets
select_workflows() {
    echo -e "${YELLOW}Select workflow presets to enable:${NC}"
    echo
    echo "1) Development Workflow (code analysis → TDD → refactoring → documentation)"
    echo "2) Security Workflow (security audit → issue creation → documentation)"
    echo "3) Documentation Workflow (git diff → tech docs → research)"
    echo "4) Quality Workflow (analysis → refactoring → testing)"
    echo "5) All Workflows (comprehensive integration)"
    echo "6) Custom Selection"
    echo
    read -p "Enter your choice (1-6): " choice
    
    case $choice in
        1) echo "development";;
        2) echo "security";;
        3) echo "documentation";;
        4) echo "quality";;
        5) echo "all";;
        6) echo "custom";;
        *) echo "development";;  # Default
    esac
}

# Function to create integrated configuration
create_integrated_config() {
    local workflow="$1"
    local config_content=""
    
    case $workflow in
        "development")
            config_content=$(cat <<'EOF'
{
  "description": "Development workflow with intelligent automation",
  "hooks": {
    "UserPromptSubmit": [{
      "hooks": [{
        "type": "command",
        "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/python/prompt-enhancer.py"
      }, {
        "type": "command",
        "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/python/agent-router.py"
      }]
    }],
    "PreToolUse": [{
      "matcher": "Task",
      "hooks": [{
        "type": "command",
        "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/python/agent-context-preparer.py"
      }]
    }],
    "PostToolUse": [{
      "matcher": "Edit|Write|MultiEdit",
      "hooks": [{
        "type": "command",
        "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/bash/test-runner.sh"
      }]
    }],
    "SubagentStop": [{
      "hooks": [{
        "type": "command",
        "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/python/agent-result-processor.py"
      }, {
        "type": "command",
        "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/python/agent-orchestrator.py"
      }]
    }]
  }
}
EOF
)
            ;;
        "security")
            config_content=$(cat <<'EOF'
{
  "description": "Security-focused workflow with audit automation",
  "hooks": {
    "SessionStart": [{
      "hooks": [{
        "type": "command",
        "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/python/security-scanner.py"
      }]
    }],
    "UserPromptSubmit": [{
      "hooks": [{
        "type": "command",
        "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/python/agent-router.py"
      }]
    }],
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/python/security-validator.py"
      }]
    }],
    "SubagentStop": [{
      "hooks": [{
        "type": "command",
        "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/python/agent-result-processor.py"
      }]
    }]
  }
}
EOF
)
            ;;
        "all")
            # Copy the complete integrated settings
            cp "$SCRIPT_DIR/.claude/templates/settings.integrated.json" "$CONFIG_FILE"
            return 0
            ;;
        *)
            # Minimal setup
            config_content=$(cat <<'EOF'
{
  "description": "Minimal hook-agent integration",
  "hooks": {
    "UserPromptSubmit": [{
      "hooks": [{
        "type": "command",
        "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/python/agent-router.py"
      }]
    }],
    "SubagentStop": [{
      "hooks": [{
        "type": "command",
        "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/python/agent-result-processor.py"
      }]
    }]
  }
}
EOF
)
            ;;
    esac
    
    echo "$config_content" > "$CONFIG_FILE"
}

# Main setup flow
main() {
    # Check if we're in a git repository
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        echo -e "${YELLOW}Warning: Not in a git repository${NC}"
    fi
    
    # Detect project type
    echo -e "${BLUE}Detecting project type...${NC}"
    project_types=($(detect_project_type))
    if [ ${#project_types[@]} -gt 0 ]; then
        echo -e "${GREEN}Detected: ${project_types[*]}${NC}"
    else
        echo -e "${YELLOW}No specific project type detected${NC}"
    fi
    echo
    
    # Check for existing .claude directory
    if [ -d "$CLAUDE_DIR" ]; then
        echo -e "${YELLOW}Found existing .claude directory${NC}"
        read -p "Merge with existing configuration? (y/n): " merge_choice
        if [[ ! "$merge_choice" =~ ^[Yy]$ ]]; then
            echo -e "${RED}Setup cancelled${NC}"
            exit 1
        fi
    else
        echo -e "${BLUE}Creating .claude directory...${NC}"
        mkdir -p "$CLAUDE_DIR"
    fi
    
    # Copy hook and agent files
    echo -e "${BLUE}Installing hooks and agents...${NC}"
    cp -r "$SCRIPT_DIR/.claude/hooks" "$CLAUDE_DIR/" 2>/dev/null || true
    cp -r "$SCRIPT_DIR/.claude/agents" "$CLAUDE_DIR/" 2>/dev/null || true
    cp -r "$SCRIPT_DIR/.claude/docs" "$CLAUDE_DIR/" 2>/dev/null || true
    cp -r "$SCRIPT_DIR/.claude/templates" "$CLAUDE_DIR/" 2>/dev/null || true
    
    # Create necessary directories
    mkdir -p "$CLAUDE_DIR/context"
    mkdir -p "$CLAUDE_DIR/agent-results"
    mkdir -p "$CLAUDE_DIR/logs"
    
    # Select and configure workflows
    echo
    workflow=$(select_workflows)
    echo -e "${BLUE}Configuring $workflow workflow...${NC}"
    create_integrated_config "$workflow"
    
    # Make scripts executable
    echo -e "${BLUE}Setting permissions...${NC}"
    find "$CLAUDE_DIR/hooks" -type f \( -name "*.sh" -o -name "*.py" \) -exec chmod +x {} \;
    
    # Check for required tools
    echo
    echo -e "${BLUE}Checking requirements...${NC}"
    missing_tools=()
    
    if [[ " ${project_types[@]} " =~ " python " ]]; then
        command_exists uv || missing_tools+=("uv")
        command_exists python || command_exists python3 || missing_tools+=("python")
    fi
    
    if [[ " ${project_types[@]} " =~ " javascript " ]]; then
        command_exists bun || command_exists npm || missing_tools+=("bun/npm")
    fi
    
    command_exists git || missing_tools+=("git")
    
    if [ ${#missing_tools[@]} -gt 0 ]; then
        echo -e "${YELLOW}Missing tools: ${missing_tools[*]}${NC}"
        echo "Please install missing tools for full functionality"
    else
        echo -e "${GREEN}All requirements met!${NC}"
    fi
    
    # Create a README for the setup
    cat > "$CLAUDE_DIR/INTEGRATION.md" << 'EOF'
# Hook-Agent Integration Active

This project has intelligent hook-agent integration configured.

## Active Components

### Hooks
- **Agent Router**: Suggests appropriate agents based on prompts
- **Context Preparer**: Prepares optimal context for agents
- **Result Processor**: Processes agent outputs and suggests next steps
- **Orchestrator**: Manages multi-agent workflows

### Agents
See `.claude/agents/` for available specialized agents.

## How It Works

1. When you type a prompt, hooks analyze it and suggest relevant agents
2. Before agents run, hooks prepare context to enhance their performance
3. After agents complete, hooks process results and orchestrate follow-ups
4. Workflows can chain multiple agents automatically

## Quick Commands

- View available agents: `/agents`
- Check hook configuration: `cat .claude/settings.local.json`
- View workflow state: `cat .claude/workflow-state.json`
- Check agent results: `ls .claude/agent-results/`

## Customization

Edit `.claude/settings.local.json` to customize hook-agent integration.
EOF
    
    echo
    echo -e "${GREEN}╔══════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║         Setup Complete! 🎉                          ║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════════════════╝${NC}"
    echo
    echo -e "${BLUE}What's been configured:${NC}"
    echo "  ✅ Intelligent agent routing based on prompts"
    echo "  ✅ Automatic context preparation for agents"
    echo "  ✅ Agent result processing and workflow orchestration"
    echo "  ✅ Multi-agent workflow chains"
    echo
    echo -e "${YELLOW}Next steps:${NC}"
    echo "  1. Start Claude Code in this directory"
    echo "  2. Your prompts will automatically suggest relevant agents"
    echo "  3. Agents will work together in intelligent workflows"
    echo
    echo -e "${BLUE}Example prompts to try:${NC}"
    echo '  - "Implement user authentication with TDD"'
    echo '  - "Perform a security audit of the codebase"'
    echo '  - "Refactor this code for better readability"'
    echo '  - "Document the recent changes"'
    echo
    echo -e "${GREEN}Integration guide available at: .claude/INTEGRATION.md${NC}"
}

# Run main setup
main "$@"