#!/bin/bash

# Code Linter Hook
# ================
# Type: PostToolUse (Edit/Write/MultiEdit)
# Description: Runs appropriate linters based on file type
#
# Supports:
# - Python: ruff (check + format)
# - JavaScript/TypeScript: eslint + prettier
# - Go: gofmt + golint
# - Rust: rustfmt + clippy

set -e

# Read hook data from stdin
HOOK_DATA=$(cat)

# Extract tool name and changed files
TOOL_NAME=$(echo "$HOOK_DATA" | jq -r '.tool_name // ""')
PROJECT_DIR=$(echo "$HOOK_DATA" | jq -r '.project_dir // "."')
CHANGED_FILES=$(echo "$HOOK_DATA" | jq -r '.changed_files[]? // empty' 2>/dev/null)

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

# Function to detect project type from config files
detect_linter_config() {
    local config_type=""
    
    # Python configs
    if [ -f "pyproject.toml" ] || [ -f "ruff.toml" ] || [ -f ".ruff.toml" ]; then
        config_type="python"
    # JavaScript/TypeScript configs
    elif [ -f "eslint.config.js" ] || [ -f ".eslintrc.js" ] || [ -f ".eslintrc.json" ]; then
        config_type="javascript"
    elif [ -f "package.json" ]; then
        if grep -q '"eslint"' package.json 2>/dev/null || grep -q '"prettier"' package.json 2>/dev/null; then
            config_type="javascript"
        fi
    # Go
    elif [ -f "go.mod" ]; then
        config_type="go"
    # Rust
    elif [ -f "Cargo.toml" ]; then
        config_type="rust"
    fi
    
    echo "$config_type"
}

# Function to run Python linters
run_python_linters() {
    local files="$1"
    local ran_linter=false
    
    echo "🐍 Python Linting"
    
    # Try ruff first (preferred)
    if command_exists ruff; then
        echo "  Running ruff..."
        
        # Check for ruff config
        local ruff_args=""
        if [ -f "pyproject.toml" ] && grep -q '\[tool.ruff\]' pyproject.toml 2>/dev/null; then
            echo "  Using pyproject.toml configuration"
        elif [ -f "ruff.toml" ] || [ -f ".ruff.toml" ]; then
            echo "  Using ruff.toml configuration"
        fi
        
        # Run ruff check with fixes
        if [ -n "$files" ]; then
            echo "$files" | grep -E '\.py$' | while read -r file; do
                [ -f "$file" ] && ruff check "$file" --fix --show-fixes 2>&1 | head -10 || true
                [ -f "$file" ] && ruff format "$file" 2>&1 | head -5 || true
            done
        else
            ruff check . --fix --show-fixes 2>&1 | head -20 || true
            ruff format . 2>&1 | head -10 || true
        fi
        ran_linter=true
        
    # Try black + flake8 as fallback
    elif command_exists black || command_exists flake8; then
        if command_exists black; then
            echo "  Running black..."
            black . 2>&1 | head -10 || true
            ran_linter=true
        fi
        
        if command_exists flake8; then
            echo "  Running flake8..."
            flake8 . 2>&1 | head -20 || true
            ran_linter=true
        fi
    fi
    
    # Try mypy for type checking
    if command_exists mypy; then
        if [ -f "pyproject.toml" ] && grep -q '\[tool.mypy\]' pyproject.toml 2>/dev/null; then
            echo "  Running mypy..."
            mypy . 2>&1 | head -20 || true
            ran_linter=true
        fi
    fi
    
    if [ "$ran_linter" = false ]; then
        echo "  ⚠️  No Python linters found"
        echo "  💡 Install: pip install ruff (or: uv pip install ruff)"
    fi
}

# Function to run JavaScript/TypeScript linters
run_javascript_linters() {
    local files="$1"
    local ran_linter=false
    
    echo "📦 JavaScript/TypeScript Linting"
    
    # Detect package manager
    local PKG_RUNNER=""
    if command_exists bun; then
        PKG_RUNNER="bunx"
    elif command_exists npm; then
        PKG_RUNNER="npx"
    fi
    
    if [ -z "$PKG_RUNNER" ]; then
        echo "  ⚠️  No package manager found (npm or bun)"
        return
    fi
    
    # Run ESLint
    if [ -f "eslint.config.js" ] || [ -f ".eslintrc.js" ] || [ -f ".eslintrc.json" ]; then
        echo "  Running ESLint..."
        
        if [ -n "$files" ]; then
            echo "$files" | grep -E '\.(js|jsx|ts|tsx)$' | while read -r file; do
                [ -f "$file" ] && $PKG_RUNNER eslint "$file" --fix 2>&1 | head -10 || true
            done
        else
            $PKG_RUNNER eslint . --fix --ext .js,.jsx,.ts,.tsx 2>&1 | head -20 || true
        fi
        ran_linter=true
    fi
    
    # Run Prettier
    if [ -f ".prettierrc" ] || [ -f ".prettierrc.json" ] || [ -f "prettier.config.js" ]; then
        echo "  Running Prettier..."
        
        if [ -n "$files" ]; then
            echo "$files" | grep -E '\.(js|jsx|ts|tsx|json|css|scss)$' | while read -r file; do
                [ -f "$file" ] && $PKG_RUNNER prettier --write "$file" 2>&1 | head -5 || true
            done
        else
            $PKG_RUNNER prettier --write "**/*.{js,jsx,ts,tsx,json,css,scss}" 2>&1 | head -10 || true
        fi
        ran_linter=true
    fi
    
    # Run TypeScript compiler for type checking
    if [ -f "tsconfig.json" ]; then
        echo "  Running TypeScript type check..."
        $PKG_RUNNER tsc --noEmit 2>&1 | head -20 || true
        ran_linter=true
    fi
    
    if [ "$ran_linter" = false ]; then
        echo "  ⚠️  No JavaScript/TypeScript linters configured"
        echo "  💡 Install: npm install -D eslint prettier"
    fi
}

# Function to run Go linters
run_go_linters() {
    local files="$1"
    local ran_linter=false
    
    echo "🐹 Go Linting"
    
    if command_exists gofmt; then
        echo "  Running gofmt..."
        gofmt -w . 2>&1 | head -10 || true
        ran_linter=true
    fi
    
    if command_exists golangci-lint; then
        echo "  Running golangci-lint..."
        golangci-lint run 2>&1 | head -20 || true
        ran_linter=true
    elif command_exists golint; then
        echo "  Running golint..."
        golint ./... 2>&1 | head -20 || true
        ran_linter=true
    fi
    
    if [ "$ran_linter" = false ]; then
        echo "  ⚠️  No Go linters found"
        echo "  💡 Install: go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest"
    fi
}

# Function to run Rust linters
run_rust_linters() {
    local files="$1"
    local ran_linter=false
    
    echo "🦀 Rust Linting"
    
    if command_exists rustfmt; then
        echo "  Running rustfmt..."
        cargo fmt 2>&1 | head -10 || true
        ran_linter=true
    fi
    
    if command_exists cargo; then
        echo "  Running clippy..."
        cargo clippy --all-targets --all-features 2>&1 | head -20 || true
        ran_linter=true
    fi
    
    if [ "$ran_linter" = false ]; then
        echo "  ⚠️  No Rust linters found"
        echo "  💡 Install: rustup component add rustfmt clippy"
    fi
}

echo "=" "=" | tr -d ' ' | head -c 60 && echo
echo "🧹 Code Linter"
echo "=" "=" | tr -d ' ' | head -c 60 && echo

# Detect project type and run appropriate linters
PROJECT_TYPE=$(detect_linter_config)

if [ -z "$PROJECT_TYPE" ]; then
    # Try to detect from changed files
    if echo "$CHANGED_FILES" | grep -q '\.py$'; then
        PROJECT_TYPE="python"
    elif echo "$CHANGED_FILES" | grep -qE '\.(js|jsx|ts|tsx)$'; then
        PROJECT_TYPE="javascript"
    elif echo "$CHANGED_FILES" | grep -q '\.go$'; then
        PROJECT_TYPE="go"
    elif echo "$CHANGED_FILES" | grep -q '\.rs$'; then
        PROJECT_TYPE="rust"
    fi
fi

# Run appropriate linters
case "$PROJECT_TYPE" in
    python)
        run_python_linters "$CHANGED_FILES"
        ;;
    javascript)
        run_javascript_linters "$CHANGED_FILES"
        ;;
    go)
        run_go_linters "$CHANGED_FILES"
        ;;
    rust)
        run_rust_linters "$CHANGED_FILES"
        ;;
    *)
        echo "ℹ️  No linter configuration detected"
        echo ""
        echo "💡 Quick setup:"
        echo "   Python: echo '[tool.ruff]' >> pyproject.toml"
        echo "   JS/TS: npm init @eslint/config"
        echo "   Go: go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest"
        echo "   Rust: rustup component add rustfmt clippy"
        ;;
esac

echo ""
echo "📚 Linting Best Practices:"
echo "   • Configure linters in project config files"
echo "   • Use pre-commit hooks to catch issues early"
echo "   • Run linters in CI/CD pipelines"
echo "   • Keep linter rules consistent across team"

echo "=" "=" | tr -d ' ' | head -c 60 && echo

# Always exit 0 to not block operations
exit 0