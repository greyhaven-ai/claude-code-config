#!/bin/bash

# Claude Code Hooks Setup Script
# This script helps install and configure Grey Haven hooks in any project

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
HOOKS_DIR="$SCRIPT_DIR"
PROJECT_DIR="${1:-$(pwd)}"

echo -e "${BLUE}🚀 Grey Haven Claude Code Hooks Setup${NC}"
echo -e "${BLUE}=====================================${NC}"
echo ""

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo -e "${YELLOW}📋 Checking prerequisites...${NC}"

MISSING_DEPS=()

if ! command_exists uv; then
    MISSING_DEPS+=("uv")
    echo -e "${RED}  ✗ uv not found${NC}"
else
    echo -e "${GREEN}  ✓ uv installed${NC}"
fi

if ! command_exists rg; then
    MISSING_DEPS+=("ripgrep")
    echo -e "${RED}  ✗ ripgrep not found${NC}"
else
    echo -e "${GREEN}  ✓ ripgrep installed${NC}"
fi

if ! command_exists git; then
    MISSING_DEPS+=("git")
    echo -e "${RED}  ✗ git not found${NC}"
else
    echo -e "${GREEN}  ✓ git installed${NC}"
fi

if ! command_exists jq; then
    echo -e "${YELLOW}  ⚠ jq not found (optional but recommended)${NC}"
fi

# If missing critical dependencies, provide installation instructions
if [ ${#MISSING_DEPS[@]} -gt 0 ]; then
    echo ""
    echo -e "${RED}Missing required dependencies!${NC}"
    echo ""
    echo "Please install the following:"
    
    for dep in "${MISSING_DEPS[@]}"; do
        case $dep in
            "uv")
                echo -e "${YELLOW}  Install uv:${NC}"
                echo "    curl -LsSf https://astral.sh/uv/install.sh | sh"
                ;;
            "ripgrep")
                echo -e "${YELLOW}  Install ripgrep:${NC}"
                echo "    macOS:  brew install ripgrep"
                echo "    Ubuntu: apt-get install ripgrep"
                ;;
            "git")
                echo -e "${YELLOW}  Install git:${NC}"
                echo "    macOS:  brew install git"
                echo "    Ubuntu: apt-get install git"
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

echo ""
echo -e "${YELLOW}📁 Setting up in: $PROJECT_DIR${NC}"

# Create .claude directory if it doesn't exist
mkdir -p "$PROJECT_DIR/.claude"

# Check if settings.json already exists
if [ -f "$PROJECT_DIR/.claude/settings.json" ]; then
    echo -e "${YELLOW}⚠  Found existing .claude/settings.json${NC}"
    read -p "Do you want to backup and replace it? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cp "$PROJECT_DIR/.claude/settings.json" "$PROJECT_DIR/.claude/settings.json.backup.$(date +%Y%m%d_%H%M%S)"
        echo -e "${GREEN}  ✓ Backup created${NC}"
    else
        echo -e "${YELLOW}  Keeping existing settings. You'll need to manually add hooks.${NC}"
        KEEP_EXISTING=true
    fi
fi

# Generate settings.json with all hooks configured
if [ -z "$KEEP_EXISTING" ]; then
    echo -e "${YELLOW}📝 Generating settings.json...${NC}"
    
    cat > "$PROJECT_DIR/.claude/settings.json" << EOF
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
        "command": "$HOOKS_DIR/bash/smart-test-runner.sh",
        "tools": ["Edit", "Write", "MultiEdit"]
      },
      {
        "command": "$HOOKS_DIR/bash/incremental-type-checker.sh",
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
        "command": "$HOOKS_DIR/python/smart-import-organizer.py",
        "tools": ["Edit", "Write", "MultiEdit"]
      }
    ],
    "stop": [
      "$HOOKS_DIR/python/coverage-gap-finder.py"
    ]
  }
}
EOF
    
    echo -e "${GREEN}  ✓ Settings generated${NC}"
fi

# Make all hooks executable
echo -e "${YELLOW}🔧 Setting permissions...${NC}"
chmod +x "$HOOKS_DIR"/python/*.py 2>/dev/null || true
chmod +x "$HOOKS_DIR"/bash/*.sh 2>/dev/null || true
echo -e "${GREEN}  ✓ Hooks made executable${NC}"

# Test a simple hook to verify setup
echo -e "${YELLOW}🧪 Testing hook execution...${NC}"
if echo '{"prompt": "test"}' | "$HOOKS_DIR/python/smart-context-injector.py" > /dev/null 2>&1; then
    echo -e "${GREEN}  ✓ Hooks are working${NC}"
else
    echo -e "${YELLOW}  ⚠ Hook test failed (dependencies may need to be installed on first run)${NC}"
fi

# Provide configuration options
echo ""
echo -e "${BLUE}📋 Configuration Options${NC}"
echo -e "${BLUE}========================${NC}"
echo ""
echo "You can customize which hooks are active by editing:"
echo "  $PROJECT_DIR/.claude/settings.json"
echo ""
echo "To disable a hook, comment it out or remove it from the settings."
echo ""

# Show enabled hooks summary
echo -e "${BLUE}✨ Enabled Hooks${NC}"
echo -e "${BLUE}=================${NC}"
echo ""
echo -e "${GREEN}Session Start:${NC}"
echo "  • Branch Context Loader - Loads context based on git branch"
echo "  • Migration Assistant - Detects outdated patterns"
echo ""
echo -e "${GREEN}User Prompt:${NC}"
echo "  • Smart Context Injector - Loads relevant code context"
echo "  • Test Data Generator - Generates test data when needed"
echo ""
echo -e "${GREEN}Before Tool Use:${NC}"
echo "  • Auto Documentation Fetcher - Gets library docs"
echo "  • Dependency Impact Analyzer - Shows impact of changes"
echo "  • API Contract Validator - Validates API changes"
echo "  • Database Query Analyzer - Analyzes SQL performance"
echo ""
echo -e "${GREEN}After Tool Use:${NC}"
echo "  • Similar Code Finder - Finds similar patterns"
echo "  • Smart Test Runner - Runs affected tests"
echo "  • Incremental Type Checker - Type checks changes"
echo "  • Performance Regression Detector - Detects perf issues"
echo "  • Code Narrator - Generates explanations"
echo "  • Smart Import Organizer - Organizes imports"
echo ""
echo -e "${GREEN}On Stop:${NC}"
echo "  • Coverage Gap Finder - Shows test coverage gaps"
echo ""

# Create a local README for the project
cat > "$PROJECT_DIR/.claude/HOOKS_README.md" << EOF
# Claude Code Hooks - Project Configuration

This project has been configured with Grey Haven Claude Code hooks.

## Active Hooks

See \`.claude/settings.json\` for the complete configuration.

## Managing Hooks

### Disable a Hook
Edit \`.claude/settings.json\` and remove or comment out the hook entry.

### Test a Hook
\`\`\`bash
echo '{"prompt": "test"}' | $HOOKS_DIR/python/smart-context-injector.py
\`\`\`

### Update Hooks
\`\`\`bash
cd $HOOKS_DIR && git pull
\`\`\`

## Troubleshooting

- **Hook not running**: Check file permissions and that dependencies are installed
- **JSON errors**: Validate your settings.json with \`jq . < .claude/settings.json\`
- **Missing dependencies**: Install with \`uv\` for Python hooks

## Documentation

Full documentation: $HOOKS_DIR/index.md
EOF

echo -e "${GREEN}✅ Setup Complete!${NC}"
echo ""
echo "Next steps:"
echo "  1. Restart Claude Code to load the new hooks"
echo "  2. Try editing some code to see the hooks in action"
echo "  3. Check $PROJECT_DIR/.claude/HOOKS_README.md for more info"
echo ""
echo -e "${BLUE}Happy coding with Grey Haven hooks! 🚀${NC}"