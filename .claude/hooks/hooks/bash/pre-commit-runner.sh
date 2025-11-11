#!/bin/bash

# Pre-commit Runner Hook
# ======================
# Type: PreToolUse (Edit/Write/MultiEdit)
# Description: Runs pre-commit checks before code modifications
#
# This hook automatically runs pre-commit checks if available,
# helping catch issues before they're committed.

set -e

# Read hook data from stdin
HOOK_DATA=$(cat)

# Extract tool name and file paths
TOOL_NAME=$(echo "$HOOK_DATA" | jq -r '.tool_name // ""')
PROJECT_DIR=$(echo "$HOOK_DATA" | jq -r '.project_dir // "."')

# Only run for edit/write tools
if [[ ! "$TOOL_NAME" =~ ^(Edit|Write|MultiEdit)$ ]]; then
    exit 0
fi

# Change to project directory
cd "$PROJECT_DIR" 2>/dev/null || exit 0

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to run pre-commit
run_precommit() {
    local config_file="$1"
    
    if [ -f "$config_file" ]; then
        echo "🔍 Running pre-commit checks..."
        
        if command_exists pre-commit; then
            # Run pre-commit on all files (or specific files if provided)
            pre-commit run --all-files 2>&1 | head -20 || true
            return 0
        else
            echo "  ⚠️  pre-commit not installed. Install with: pip install pre-commit"
            return 1
        fi
    fi
    return 1
}

# Function to run git hooks
run_git_hooks() {
    if [ -d ".git/hooks" ]; then
        if [ -f ".git/hooks/pre-commit" ]; then
            echo "🔍 Running git pre-commit hook..."
            bash .git/hooks/pre-commit 2>&1 | head -20 || true
            return 0
        fi
    fi
    return 1
}

# Function to run husky
run_husky() {
    if [ -d ".husky" ]; then
        if [ -f ".husky/pre-commit" ]; then
            echo "🔍 Running husky pre-commit..."
            bash .husky/pre-commit 2>&1 | head -20 || true
            return 0
        fi
    fi
    return 1
}

# Function to run lint-staged
run_lint_staged() {
    if [ -f "package.json" ]; then
        if grep -q '"lint-staged"' package.json 2>/dev/null; then
            echo "🔍 Running lint-staged..."
            
            if command_exists npx; then
                npx lint-staged 2>&1 | head -20 || true
                return 0
            elif command_exists bunx; then
                bunx lint-staged 2>&1 | head -20 || true
                return 0
            fi
        fi
    fi
    return 1
}

echo "=" "=" | tr -d ' ' | head -c 60 && echo
echo "🎯 Pre-commit Check"
echo "=" "=" | tr -d ' ' | head -c 60 && echo

# Try different pre-commit systems
FOUND_SYSTEM=false

# Check for .pre-commit-config.yaml
if run_precommit ".pre-commit-config.yaml"; then
    FOUND_SYSTEM=true
fi

# Check for husky
if [ "$FOUND_SYSTEM" = false ]; then
    if run_husky; then
        FOUND_SYSTEM=true
    fi
fi

# Check for lint-staged
if [ "$FOUND_SYSTEM" = false ]; then
    if run_lint_staged; then
        FOUND_SYSTEM=true
    fi
fi

# Check for git hooks
if [ "$FOUND_SYSTEM" = false ]; then
    if run_git_hooks; then
        FOUND_SYSTEM=true
    fi
fi

if [ "$FOUND_SYSTEM" = false ]; then
    echo "ℹ️  No pre-commit system found"
    echo ""
    echo "💡 Consider setting up pre-commit:"
    echo "   Python: pip install pre-commit && pre-commit install"
    echo "   Node: npx husky install"
    echo "   Or: Create .git/hooks/pre-commit"
fi

echo "=" "=" | tr -d ' ' | head -c 60 && echo

# Always exit 0 to not block operations
exit 0