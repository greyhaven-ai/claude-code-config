#!/bin/bash
# Incremental Type Checker Hook
# =============================
# Type: PostToolUse
# Description: Type checks only changed files and their dependents
#
# This hook runs type checking incrementally on changed files,
# providing fast feedback and auto-fixing simple type errors

set -euo pipefail

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
MAX_CHECK_TIME=10  # Maximum time for type checking in seconds

# Function to detect type checker
detect_type_checker() {
    local checker=""
    
    # TypeScript
    if [ -f "$PROJECT_DIR/tsconfig.json" ]; then
        if command -v tsc &> /dev/null; then
            checker="typescript"
        fi
    
    # Python - mypy, pyright, pyre
    elif [ -f "$PROJECT_DIR/mypy.ini" ] || [ -f "$PROJECT_DIR/setup.cfg" ] || [ -f "$PROJECT_DIR/pyproject.toml" ]; then
        if command -v mypy &> /dev/null; then
            checker="mypy"
        elif command -v pyright &> /dev/null; then
            checker="pyright"
        elif command -v pyre &> /dev/null; then
            checker="pyre"
        fi
    
    # Flow (JavaScript)
    elif [ -f "$PROJECT_DIR/.flowconfig" ]; then
        if command -v flow &> /dev/null; then
            checker="flow"
        fi
    
    # Go (built-in)
    elif [ -f "$PROJECT_DIR/go.mod" ]; then
        checker="go"
    
    # Rust (built-in)
    elif [ -f "$PROJECT_DIR/Cargo.toml" ]; then
        checker="cargo"
    
    # Java
    elif [ -f "$PROJECT_DIR/pom.xml" ] || [ -f "$PROJECT_DIR/build.gradle" ]; then
        checker="java"
    fi
    
    echo "$checker"
}

# Function to find dependent files (files that import the changed file)
find_dependent_files() {
    local changed_file="$1"
    local file_name=$(basename "$changed_file" | sed 's/\.[^.]*$//')
    local dependents=()
    
    # Use ripgrep to find files that import this one
    if command -v rg &> /dev/null; then
        # Search for various import patterns
        local patterns=(
            "from.*$file_name.*import"
            "import.*$file_name"
            "require.*$file_name"
            "from.*['\"].*$file_name['\"]"
        )
        
        for pattern in "${patterns[@]}"; do
            local found=$(rg -l "$pattern" "$PROJECT_DIR" 2>/dev/null | head -10)
            if [ -n "$found" ]; then
                dependents+=($found)
            fi
        done
    fi
    
    # Return unique dependents
    printf '%s\n' "${dependents[@]}" | sort -u
}

# Function to run type checking
run_type_check() {
    local checker="$1"
    shift
    local files=("$@")
    
    if [ ${#files[@]} -eq 0 ]; then
        return 0
    fi
    
    local exit_code=0
    
    case "$checker" in
        typescript)
            echo "📘 Running TypeScript type checking..."
            # Create a temporary tsconfig for incremental checking
            local temp_config=$(mktemp)
            cat > "$temp_config" << EOF
{
  "extends": "./tsconfig.json",
  "compilerOptions": {
    "noEmit": true,
    "incremental": true,
    "tsBuildInfoFile": ".tsbuildinfo-hook"
  },
  "files": [$(printf '"%s",' "${files[@]}" | sed 's/,$//')],
  "include": []
}
EOF
            timeout "$MAX_CHECK_TIME" npx tsc --project "$temp_config" || exit_code=$?
            rm -f "$temp_config"
            
            # Auto-fix suggestions if available
            if [ $exit_code -ne 0 ] && command -v ts-fix &> /dev/null; then
                echo "🔧 Attempting to auto-fix TypeScript errors..."
                npx ts-fix "${files[@]}" 2>/dev/null || true
            fi
            ;;
            
        mypy)
            echo "🐍 Running mypy type checking..."
            timeout "$MAX_CHECK_TIME" mypy "${files[@]}" --incremental --cache-dir .mypy_cache_hook || exit_code=$?
            
            # Check for simple fixes
            if [ $exit_code -ne 0 ]; then
                echo "💡 Common fixes:"
                echo "  • Add type hints to function parameters"
                echo "  • Import missing types from typing module"
                echo "  • Use Optional[] for nullable types"
            fi
            ;;
            
        pyright)
            echo "🐍 Running pyright type checking..."
            timeout "$MAX_CHECK_TIME" pyright "${files[@]}" || exit_code=$?
            ;;
            
        pyre)
            echo "🐍 Running pyre type checking..."
            timeout "$MAX_CHECK_TIME" pyre check "${files[@]}" || exit_code=$?
            ;;
            
        flow)
            echo "🌊 Running Flow type checking..."
            timeout "$MAX_CHECK_TIME" flow check "${files[@]}" || exit_code=$?
            
            # Auto-fix with flow-typed if available
            if [ $exit_code -ne 0 ] && command -v flow-typed &> /dev/null; then
                echo "🔧 Installing type definitions..."
                flow-typed install 2>/dev/null || true
            fi
            ;;
            
        go)
            echo "🐹 Running Go type checking..."
            for file in "${files[@]}"; do
                if [[ "$file" == *.go ]]; then
                    local dir=$(dirname "$file")
                    timeout "$MAX_CHECK_TIME" go build -o /dev/null "$dir" || exit_code=$?
                fi
            done
            ;;
            
        cargo)
            echo "🦀 Running Rust type checking..."
            timeout "$MAX_CHECK_TIME" cargo check --message-format short || exit_code=$?
            
            # Suggest fixes with clippy
            if [ $exit_code -ne 0 ] && command -v cargo-clippy &> /dev/null; then
                echo "🔧 Running clippy for suggestions..."
                cargo clippy --fix --allow-dirty --allow-staged 2>/dev/null || true
            fi
            ;;
            
        java)
            echo "☕ Running Java compilation check..."
            if [ -f "$PROJECT_DIR/pom.xml" ]; then
                timeout "$MAX_CHECK_TIME" mvn compile -q || exit_code=$?
            elif [ -f "$PROJECT_DIR/build.gradle" ]; then
                timeout "$MAX_CHECK_TIME" ./gradlew compileJava -q || exit_code=$?
            fi
            ;;
            
        *)
            echo "⚠️  Unknown type checker: $checker"
            return 1
            ;;
    esac
    
    return $exit_code
}

# Function to extract type errors and format them
format_type_errors() {
    local output="$1"
    
    # Extract and format common error patterns
    echo "$output" | grep -E "(error|Error|ERROR)" | head -5 | while IFS= read -r line; do
        # Clean up the error message
        echo "  • $line" | sed 's/^[[:space:]]*//' | cut -c1-100
    done
}

# Main execution
main() {
    # Check if we have changed files
    if [ -z "${CLAUDE_FILE_PATHS:-}" ]; then
        exit 0
    fi
    
    # Detect type checker
    local checker=$(detect_type_checker)
    
    if [ -z "$checker" ]; then
        # No type checker found, exit silently
        exit 0
    fi
    
    echo "="
    echo "🔍 Incremental Type Checker"
    echo "="
    echo "Type checker: $checker"
    echo ""
    
    # Collect files to check (changed files + dependents)
    local files_to_check=()
    
    for file in $CLAUDE_FILE_PATHS; do
        if [ -f "$file" ]; then
            files_to_check+=("$file")
            
            # Find dependent files
            local dependents=$(find_dependent_files "$file")
            if [ -n "$dependents" ]; then
                files_to_check+=($dependents)
            fi
        fi
    done
    
    # Remove duplicates
    files_to_check=($(printf '%s\n' "${files_to_check[@]}" | sort -u))
    
    echo "Checking ${#files_to_check[@]} file(s)..."
    
    # Run type checking and capture output
    local temp_output=$(mktemp)
    
    if run_type_check "$checker" "${files_to_check[@]}" 2>&1 | tee "$temp_output"; then
        echo ""
        echo "✅ Type checking passed!"
    else
        echo ""
        echo "❌ Type errors found!"
        
        # Format and display errors
        local errors=$(format_type_errors "$(cat "$temp_output")")
        if [ -n "$errors" ]; then
            echo ""
            echo "Key errors:"
            echo "$errors"
        fi
        
        # Provide suggestions based on checker
        echo ""
        echo "💡 Quick fixes:"
        
        case "$checker" in
            typescript)
                echo "  • Run: npx tsc --noEmit --listFiles to see all checked files"
                echo "  • Add // @ts-ignore above problematic lines (temporary)"
                echo "  • Check tsconfig.json strictness settings"
                ;;
            mypy|pyright|pyre)
                echo "  • Add type: ignore comment for false positives"
                echo "  • Use typing.cast() for type assertions"
                echo "  • Install type stubs: pip install types-*"
                ;;
            flow)
                echo "  • Add // \$FlowFixMe comment for complex issues"
                echo "  • Run: flow suggest to get automatic fixes"
                ;;
            go)
                echo "  • Run: go fmt ./... to format code"
                echo "  • Check for missing imports"
                ;;
            cargo)
                echo "  • Run: cargo fix to apply suggestions"
                echo "  • Use #[allow(...)] for false positives"
                ;;
        esac
        
        # Clean up
        rm -f "$temp_output"
        
        # Don't block with exit code 2, just warn
        echo ""
        echo "⚠️  Please fix type errors to maintain code quality"
    fi
    
    rm -f "$temp_output"
    echo "="
    
    exit 0
}

# Run main function
main