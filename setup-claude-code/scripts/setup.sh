#!/bin/bash

# Grey Haven Claude Code Configuration Setup Script
# This script helps install Claude Code hooks, agents, and configs in any project
# Supports both Python (uv) and JavaScript/TypeScript (bunx/npx) environments

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Get the directory where this script is located (repo root)
REPO_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
CLAUDE_TEMPLATE_DIR="$REPO_ROOT/.claude"
PROJECT_DIR="${1:-$(pwd)}"

echo -e "${PURPLE}🚀 Grey Haven Claude Code Configuration Setup${NC}"
echo -e "${PURPLE}=============================================${NC}"
echo ""
echo -e "${BLUE}Repository: $REPO_ROOT${NC}"
echo -e "${BLUE}Target Project: $PROJECT_DIR${NC}"
echo ""

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Detect project type
detect_project_type() {
    local project_type="unknown"
    
    if [ -f "$PROJECT_DIR/package.json" ]; then
        project_type="javascript"
    elif [ -f "$PROJECT_DIR/requirements.txt" ] || [ -f "$PROJECT_DIR/pyproject.toml" ] || [ -f "$PROJECT_DIR/setup.py" ]; then
        project_type="python"
    elif [ -f "$PROJECT_DIR/Cargo.toml" ]; then
        project_type="rust"
    elif [ -f "$PROJECT_DIR/go.mod" ]; then
        project_type="go"
    fi
    
    echo "$project_type"
}

PROJECT_TYPE=$(detect_project_type)

echo -e "${YELLOW}📋 Project type detected: ${PROJECT_TYPE}${NC}"
echo ""

# Check prerequisites based on project type
echo -e "${YELLOW}📋 Checking prerequisites...${NC}"

MISSING_DEPS=()
OPTIONAL_MISSING=()

# Common tools
if ! command_exists git; then
    MISSING_DEPS+=("git")
    echo -e "${RED}  ✗ git not found${NC}"
else
    echo -e "${GREEN}  ✓ git installed${NC}"
fi

if ! command_exists rg; then
    MISSING_DEPS+=("ripgrep")
    echo -e "${RED}  ✗ ripgrep not found${NC}"
else
    echo -e "${GREEN}  ✓ ripgrep installed${NC}"
fi

if ! command_exists jq; then
    OPTIONAL_MISSING+=("jq")
    echo -e "${YELLOW}  ⚠ jq not found (optional but recommended)${NC}"
else
    echo -e "${GREEN}  ✓ jq installed${NC}"
fi

# Python environment
if [ "$PROJECT_TYPE" = "python" ] || [ "$PROJECT_TYPE" = "unknown" ]; then
    if ! command_exists uv; then
        OPTIONAL_MISSING+=("uv")
        echo -e "${YELLOW}  ⚠ uv not found (needed for Python hooks)${NC}"
    else
        echo -e "${GREEN}  ✓ uv installed${NC}"
    fi
fi

# JavaScript/TypeScript environment
if [ "$PROJECT_TYPE" = "javascript" ]; then
    if command_exists bun; then
        echo -e "${GREEN}  ✓ bun installed (will use bunx)${NC}"
        JS_RUNNER="bunx"
    elif command_exists npm; then
        echo -e "${GREEN}  ✓ npm installed (will use npx)${NC}"
        JS_RUNNER="npx"
    else
        MISSING_DEPS+=("npm or bun")
        echo -e "${RED}  ✗ Neither bun nor npm found${NC}"
    fi
fi

# If missing critical dependencies, provide installation instructions
if [ ${#MISSING_DEPS[@]} -gt 0 ]; then
    echo ""
    echo -e "${RED}Missing required dependencies!${NC}"
    echo ""
    echo "Please install the following:"
    
    for dep in "${MISSING_DEPS[@]}"; do
        case $dep in
            "git")
                echo -e "${YELLOW}  Install git:${NC}"
                echo "    macOS:  brew install git"
                echo "    Ubuntu: apt-get install git"
                ;;
            "ripgrep")
                echo -e "${YELLOW}  Install ripgrep:${NC}"
                echo "    macOS:  brew install ripgrep"
                echo "    Ubuntu: apt-get install ripgrep"
                ;;
            "npm or bun")
                echo -e "${YELLOW}  Install bun (recommended) or npm:${NC}"
                echo "    Bun:  curl -fsSL https://bun.sh/install | bash"
                echo "    Node: https://nodejs.org/"
                ;;
        esac
    done
    
    echo ""
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Show optional dependencies
if [ ${#OPTIONAL_MISSING[@]} -gt 0 ]; then
    echo ""
    echo -e "${YELLOW}Optional dependencies not found:${NC}"
    
    for dep in "${OPTIONAL_MISSING[@]}"; do
        case $dep in
            "uv")
                echo -e "${YELLOW}  Install uv for Python hooks:${NC}"
                echo "    curl -LsSf https://astral.sh/uv/install.sh | sh"
                ;;
            "jq")
                echo -e "${YELLOW}  Install jq for JSON processing:${NC}"
                echo "    macOS:  brew install jq"
                echo "    Ubuntu: apt-get install jq"
                ;;
        esac
    done
fi

echo ""
echo -e "${YELLOW}📁 Setting up Claude Code configuration in: $PROJECT_DIR${NC}"

# Create .claude directory if it doesn't exist
mkdir -p "$PROJECT_DIR/.claude"

# Check what to install
echo ""
echo -e "${BLUE}What would you like to install?${NC}"
echo "  1) Hooks only"
echo "  2) Agents only"
echo "  3) Everything (hooks + agents + configs)"
echo "  4) Custom selection"
read -p "Enter choice [1-4]: " -n 1 -r INSTALL_CHOICE
echo ""

INSTALL_HOOKS=false
INSTALL_AGENTS=false
INSTALL_CONFIGS=false

case $INSTALL_CHOICE in
    1)
        INSTALL_HOOKS=true
        ;;
    2)
        INSTALL_AGENTS=true
        ;;
    3)
        INSTALL_HOOKS=true
        INSTALL_AGENTS=true
        INSTALL_CONFIGS=true
        ;;
    4)
        read -p "Install hooks? (y/N) " -n 1 -r
        echo
        [[ $REPLY =~ ^[Yy]$ ]] && INSTALL_HOOKS=true
        
        read -p "Install agents? (y/N) " -n 1 -r
        echo
        [[ $REPLY =~ ^[Yy]$ ]] && INSTALL_AGENTS=true
        
        read -p "Install configs? (y/N) " -n 1 -r
        echo
        [[ $REPLY =~ ^[Yy]$ ]] && INSTALL_CONFIGS=true
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac

# Check if settings.json already exists
SETTINGS_FILE="$PROJECT_DIR/.claude/settings.json"
if [ -f "$SETTINGS_FILE" ]; then
    echo -e "${YELLOW}⚠  Found existing .claude/settings.json${NC}"
    read -p "Do you want to backup and replace it? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cp "$SETTINGS_FILE" "$SETTINGS_FILE.backup.$(date +%Y%m%d_%H%M%S)"
        echo -e "${GREEN}  ✓ Backup created${NC}"
    else
        echo -e "${YELLOW}  Keeping existing settings. You'll need to manually merge configurations.${NC}"
        KEEP_EXISTING=true
    fi
fi

# Install hooks
if [ "$INSTALL_HOOKS" = true ]; then
    echo ""
    echo -e "${BLUE}📦 Installing Hooks...${NC}"
    
    HOOKS_DIR="$CLAUDE_TEMPLATE_DIR/implementations/hooks"
    
    # Generate hooks configuration
    if [ -z "$KEEP_EXISTING" ]; then
        echo -e "${YELLOW}  Generating hooks configuration...${NC}"
        
        # Determine which hooks to use based on project type
        if [ "$PROJECT_TYPE" = "javascript" ]; then
            TEST_RUNNER="$HOOKS_DIR/javascript/test-runner.js"
            TYPE_CHECKER="$HOOKS_DIR/javascript/incremental-type-checker.js"
            IMPORT_ORGANIZER="$HOOKS_DIR/javascript/import-organizer.js"
            COVERAGE_FINDER="$HOOKS_DIR/javascript/coverage-gap-finder.js"
        else
            TEST_RUNNER="$HOOKS_DIR/bash/test-runner.sh"
            TYPE_CHECKER="$HOOKS_DIR/bash/incremental-type-checker.sh"
            IMPORT_ORGANIZER="$HOOKS_DIR/python/import-organizer.py"
            COVERAGE_FINDER="$HOOKS_DIR/python/coverage-gap-finder.py"
        fi
        
        # Create settings.json with appropriate paths
        cat > "$SETTINGS_FILE" << EOF
{
  "hooks": {
    "sessionStart": [
      "$HOOKS_DIR/bash/branch-context-loader.sh",
      "$HOOKS_DIR/python/migration-assistant.py"
    ],
    "userPromptSubmit": [
      "$HOOKS_DIR/python/smart-context-injector.py",
      "$HOOKS_DIR/python/test-data-generator.py"
    ],
    "preToolUse": [
      {
        "command": "$HOOKS_DIR/bash/pre-commit-runner.sh",
        "tools": ["Edit", "Write", "MultiEdit"]
      },
      {
        "command": "$HOOKS_DIR/python/auto-documentation-fetcher.py",
        "tools": ["Edit", "Write", "Read"]
      },
      {
        "command": "$HOOKS_DIR/python/dependency-impact-analyzer.py",
        "tools": ["Edit", "Write", "MultiEdit"]
      },
      {
        "command": "$HOOKS_DIR/python/api-contract-validator.py",
        "tools": ["Edit", "Write", "MultiEdit"]
      },
      {
        "command": "$HOOKS_DIR/python/database-query-analyzer.py",
        "tools": ["Bash"]
      }
    ],
    "postToolUse": [
      {
        "command": "$HOOKS_DIR/python/similar-code-finder.py",
        "tools": ["Edit", "Write", "MultiEdit"]
      },
      {
        "command": "$TEST_RUNNER",
        "tools": ["Edit", "Write", "MultiEdit"]
      },
      {
        "command": "$TYPE_CHECKER",
        "tools": ["Edit", "Write", "MultiEdit"]
      },
      {
        "command": "$HOOKS_DIR/python/performance-regression-detector.py",
        "tools": ["Edit", "Write"]
      },
      {
        "command": "$HOOKS_DIR/python/code-narrator.py",
        "tools": ["Edit", "Write", "MultiEdit"]
      },
      {
        "command": "$IMPORT_ORGANIZER",
        "tools": ["Edit", "Write", "MultiEdit"]
      },
      {
        "command": "$HOOKS_DIR/bash/code-linter.sh",
        "tools": ["Edit", "Write", "MultiEdit"]
      }
    ],
    "stop": [
      "$COVERAGE_FINDER"
    ]
  }
}
EOF
    fi
    
    # Make hooks executable
    chmod +x "$HOOKS_DIR"/python/*.py 2>/dev/null || true
    chmod +x "$HOOKS_DIR"/bash/*.sh 2>/dev/null || true
    chmod +x "$HOOKS_DIR"/javascript/*.js 2>/dev/null || true
    
    echo -e "${GREEN}  ✓ Hooks installed${NC}"
fi

# Install agents
if [ "$INSTALL_AGENTS" = true ]; then
    echo ""
    echo -e "${BLUE}📦 Installing Agents...${NC}"
    
    # Copy agents directory
    if [ -d "$CLAUDE_TEMPLATE_DIR/agents" ]; then
        cp -r "$CLAUDE_TEMPLATE_DIR/agents" "$PROJECT_DIR/.claude/"
        echo -e "${GREEN}  ✓ Agents copied${NC}"
    else
        echo -e "${YELLOW}  ⚠ No agents found in template${NC}"
    fi
fi

# Install configs
if [ "$INSTALL_CONFIGS" = true ]; then
    echo ""
    echo -e "${BLUE}📦 Installing Configurations...${NC}"
    
    # Copy config files
    if [ -f "$CLAUDE_TEMPLATE_DIR/CLAUDE.md" ]; then
        cp "$CLAUDE_TEMPLATE_DIR/CLAUDE.md" "$PROJECT_DIR/.claude/"
        echo -e "${GREEN}  ✓ CLAUDE.md copied${NC}"
    fi
    
    # Create or update .claud_session_context if needed
    if [ ! -f "$PROJECT_DIR/.claude/.claud_session_context" ]; then
        cat > "$PROJECT_DIR/.claude/.claud_session_context" << EOF
# Claude Code Session Context
# This file is auto-loaded at the start of each session

## Project Type: $PROJECT_TYPE

## Available Commands
- Use \`$JS_RUNNER\` for JavaScript package execution
- Use \`uv run\` for Python package execution

## Grey Haven Hooks Installed
- Run \`/hooks\` to see active hooks
- Configuration in \`.claude/settings.json\`
EOF
        echo -e "${GREEN}  ✓ Session context created${NC}"
    fi
fi

# Create package.json for JS/TS projects to handle hook dependencies
if [ "$PROJECT_TYPE" = "javascript" ] && [ "$INSTALL_HOOKS" = true ]; then
    echo ""
    echo -e "${BLUE}📦 Setting up JavaScript hook support...${NC}"
    
    HOOKS_PACKAGE_JSON="$PROJECT_DIR/.claude/hooks-package.json"
    cat > "$HOOKS_PACKAGE_JSON" << EOF
{
  "name": "claude-code-hooks-deps",
  "private": true,
  "description": "Dependencies for Grey Haven Claude Code hooks in JS/TS environment",
  "dependencies": {
    "typescript": "^5.0.0",
    "eslint": "^8.0.0",
    "prettier": "^3.0.0",
    "@types/node": "^20.0.0"
  },
  "devDependencies": {
    "vitest": "^1.0.0",
    "jest": "^29.0.0"
  }
}
EOF
    
    echo -e "${YELLOW}  Installing JavaScript dependencies...${NC}"
    if [ "$JS_RUNNER" = "bunx" ]; then
        (cd "$PROJECT_DIR/.claude" && bun install --package-lock=false) > /dev/null 2>&1 || true
    else
        (cd "$PROJECT_DIR/.claude" && npm install --no-save --no-package-lock) > /dev/null 2>&1 || true
    fi
    echo -e "${GREEN}  ✓ JavaScript support configured${NC}"
fi

# Test installation
echo ""
echo -e "${YELLOW}🧪 Testing installation...${NC}"

if [ "$INSTALL_HOOKS" = true ]; then
    if echo '{"prompt": "test"}' | "$HOOKS_DIR/python/smart-context-injector.py" > /dev/null 2>&1; then
        echo -e "${GREEN}  ✓ Python hooks working${NC}"
    else
        echo -e "${YELLOW}  ⚠ Python hooks need dependencies (will install on first run)${NC}"
    fi
    
    if [ -f "$HOOKS_DIR/bash/branch-context-loader.sh" ]; then
        echo -e "${GREEN}  ✓ Bash hooks ready${NC}"
    fi
fi

# Create README for the project
cat > "$PROJECT_DIR/.claude/README.md" << EOF
# Claude Code Configuration

This project has been configured with Grey Haven Claude Code enhancements.

## Installed Components

$([ "$INSTALL_HOOKS" = true ] && echo "✅ **Hooks**: Automated workflow enhancements")
$([ "$INSTALL_AGENTS" = true ] && echo "✅ **Agents**: Specialized AI assistants")
$([ "$INSTALL_CONFIGS" = true ] && echo "✅ **Configs**: Project configurations")

## Project Information

- **Type**: $PROJECT_TYPE
- **Package Runner**: ${JS_RUNNER:-uv}
- **Configuration**: \`.claude/settings.json\`

## Quick Commands

### Test a Hook
\`\`\`bash
echo '{"prompt": "test"}' | $HOOKS_DIR/python/smart-context-injector.py
\`\`\`

### Update Grey Haven Tools
\`\`\`bash
cd $REPO_ROOT && git pull
bash $REPO_ROOT/setup.sh $PROJECT_DIR
\`\`\`

## Available Hooks

$([ "$INSTALL_HOOKS" = true ] && cat << HOOKS
- **Session Start**: Branch context loader, Migration assistant
- **User Prompt**: Smart context injector, Test data generator
- **Before Tool Use**: Documentation fetcher, Dependency analyzer, API validator, Query analyzer
- **After Tool Use**: Similar code finder, Test runner, Type checker, Performance detector, Code narrator, Import organizer
- **On Stop**: Coverage gap finder
HOOKS
)

## Documentation

- Full documentation: $REPO_ROOT/docs/
- Hooks guide: $HOOKS_DIR/index.md
- Agents guide: $CLAUDE_TEMPLATE_DIR/agents/guide.md

## Troubleshooting

- **Hooks not running**: Check file permissions and dependencies
- **JSON errors**: Validate with \`jq . < .claude/settings.json\`
- **Missing dependencies**: 
  - Python: Install with \`uv\`
  - JavaScript: Run \`$JS_RUNNER install\` in \`.claude/\`
EOF

# Summary
echo ""
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo ""
echo -e "${BLUE}📋 Summary${NC}"
echo -e "${BLUE}===========${NC}"

[ "$INSTALL_HOOKS" = true ] && echo -e "${GREEN}  ✓ Hooks installed and configured${NC}"
[ "$INSTALL_AGENTS" = true ] && echo -e "${GREEN}  ✓ Agents installed${NC}"
[ "$INSTALL_CONFIGS" = true ] && echo -e "${GREEN}  ✓ Configurations installed${NC}"

echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "  1. Restart Claude Code to load the new configuration"
echo "  2. Run /hooks command to verify hook setup"
echo "  3. Check $PROJECT_DIR/.claude/README.md for usage instructions"

if [ "$PROJECT_TYPE" = "javascript" ]; then
    echo ""
    echo -e "${PURPLE}JavaScript/TypeScript specific:${NC}"
    echo "  • Use ${JS_RUNNER} for running Node packages"
    echo "  • Dependencies are in .claude/hooks-package.json"
fi

echo ""
echo -e "${BLUE}Happy coding with Grey Haven tools! 🚀${NC}"