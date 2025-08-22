#!/bin/bash
# Smart Test Runner Hook
# ======================
# Type: PostToolUse (Edit)
# Description: Intelligently runs only affected tests based on dependency graph
#
# This hook detects which tests need to run based on file changes and
# runs them in order from unit -> integration -> e2e

set -euo pipefail

# Configuration
MAX_TEST_TIME=30  # Maximum time for test execution in seconds
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"

# Function to detect test framework
detect_test_framework() {
    local framework=""
    
    # Python - pytest, unittest
    if [ -f "$PROJECT_DIR/pytest.ini" ] || [ -f "$PROJECT_DIR/setup.cfg" ] || [ -f "$PROJECT_DIR/pyproject.toml" ]; then
        if command -v pytest &> /dev/null; then
            framework="pytest"
        elif [ -f "$PROJECT_DIR/manage.py" ]; then
            framework="django"
        else
            framework="unittest"
        fi
    
    # JavaScript/TypeScript - jest, mocha, vitest
    elif [ -f "$PROJECT_DIR/package.json" ]; then
        if grep -q '"jest"' "$PROJECT_DIR/package.json" 2>/dev/null; then
            framework="jest"
        elif grep -q '"vitest"' "$PROJECT_DIR/package.json" 2>/dev/null; then
            framework="vitest"
        elif grep -q '"mocha"' "$PROJECT_DIR/package.json" 2>/dev/null; then
            framework="mocha"
        elif grep -q '"test"' "$PROJECT_DIR/package.json" 2>/dev/null; then
            framework="npm"
        fi
    
    # Go
    elif [ -f "$PROJECT_DIR/go.mod" ]; then
        framework="go"
    
    # Rust
    elif [ -f "$PROJECT_DIR/Cargo.toml" ]; then
        framework="cargo"
    
    # Java - Maven, Gradle
    elif [ -f "$PROJECT_DIR/pom.xml" ]; then
        framework="maven"
    elif [ -f "$PROJECT_DIR/build.gradle" ] || [ -f "$PROJECT_DIR/build.gradle.kts" ]; then
        framework="gradle"
    fi
    
    echo "$framework"
}

# Function to find related test files
find_test_files() {
    local changed_file="$1"
    local base_name=$(basename "$changed_file" | sed 's/\.[^.]*$//')
    local dir_name=$(dirname "$changed_file")
    local test_files=()
    
    # Common test file patterns
    local patterns=(
        "test_${base_name}.py"
        "${base_name}_test.py"
        "${base_name}.test.js"
        "${base_name}.test.ts"
        "${base_name}.spec.js"
        "${base_name}.spec.ts"
        "${base_name}_test.go"
        "Test${base_name}.java"
        "${base_name}Test.java"
    )
    
    # Search for test files
    for pattern in "${patterns[@]}"; do
        # Look in common test directories
        for test_dir in "test" "tests" "spec" "__tests__" "test_${base_name}" "${dir_name}/test" "${dir_name}/__tests__"; do
            if [ -d "$PROJECT_DIR/$test_dir" ]; then
                local found=$(find "$PROJECT_DIR/$test_dir" -name "$pattern" 2>/dev/null | head -5)
                if [ -n "$found" ]; then
                    test_files+=($found)
                fi
            fi
        done
        
        # Also look in the same directory
        local same_dir_test="$dir_name/$pattern"
        if [ -f "$PROJECT_DIR/$same_dir_test" ]; then
            test_files+=("$PROJECT_DIR/$same_dir_test")
        fi
    done
    
    # Return unique test files
    printf '%s\n' "${test_files[@]}" | sort -u
}

# Function to categorize tests
categorize_tests() {
    local test_files=("$@")
    local unit_tests=()
    local integration_tests=()
    local e2e_tests=()
    
    for test_file in "${test_files[@]}"; do
        if [[ "$test_file" =~ (unit|Unit) ]]; then
            unit_tests+=("$test_file")
        elif [[ "$test_file" =~ (integration|Integration|int_test) ]]; then
            integration_tests+=("$test_file")
        elif [[ "$test_file" =~ (e2e|E2E|end_to_end|EndToEnd) ]]; then
            e2e_tests+=("$test_file")
        else
            # Default to unit tests
            unit_tests+=("$test_file")
        fi
    done
    
    echo "UNIT:${unit_tests[*]}"
    echo "INTEGRATION:${integration_tests[*]}"
    echo "E2E:${e2e_tests[*]}"
}

# Function to run tests based on framework
run_tests() {
    local framework="$1"
    shift
    local test_files=("$@")
    
    if [ ${#test_files[@]} -eq 0 ]; then
        return 0
    fi
    
    echo "🧪 Running ${#test_files[@]} test file(s) with $framework"
    
    case "$framework" in
        pytest)
            timeout "$MAX_TEST_TIME" pytest "${test_files[@]}" -v --tb=short || return $?
            ;;
        unittest)
            for test in "${test_files[@]}"; do
                timeout "$MAX_TEST_TIME" python -m unittest "$test" || return $?
            done
            ;;
        django)
            timeout "$MAX_TEST_TIME" python manage.py test "${test_files[@]}" || return $?
            ;;
        jest)
            timeout "$MAX_TEST_TIME" npx jest "${test_files[@]}" --bail || return $?
            ;;
        vitest)
            timeout "$MAX_TEST_TIME" npx vitest run "${test_files[@]}" --bail || return $?
            ;;
        mocha)
            timeout "$MAX_TEST_TIME" npx mocha "${test_files[@]}" --bail || return $?
            ;;
        npm)
            timeout "$MAX_TEST_TIME" npm test -- "${test_files[@]}" || return $?
            ;;
        go)
            for test in "${test_files[@]}"; do
                local test_dir=$(dirname "$test")
                timeout "$MAX_TEST_TIME" go test "$test_dir" -v || return $?
            done
            ;;
        cargo)
            timeout "$MAX_TEST_TIME" cargo test --lib || return $?
            ;;
        maven)
            timeout "$MAX_TEST_TIME" mvn test || return $?
            ;;
        gradle)
            timeout "$MAX_TEST_TIME" ./gradlew test || return $?
            ;;
        *)
            echo "⚠️  Unknown test framework: $framework"
            return 1
            ;;
    esac
}

# Main execution
main() {
    # Check if we have changed files
    if [ -z "${CLAUDE_FILE_PATHS:-}" ]; then
        echo "ℹ️  No files changed, skipping test run"
        exit 0
    fi
    
    # Detect test framework
    local framework=$(detect_test_framework)
    
    if [ -z "$framework" ]; then
        echo "ℹ️  No test framework detected"
        exit 0
    fi
    
    echo "=" 
    echo "🧪 Smart Test Runner"
    echo "="
    echo "Framework: $framework"
    echo ""
    
    # Collect all test files for changed files
    local all_test_files=()
    
    for file in $CLAUDE_FILE_PATHS; do
        if [ -f "$file" ]; then
            echo "📝 Changed file: $(basename "$file")"
            local test_files=$(find_test_files "$file")
            if [ -n "$test_files" ]; then
                all_test_files+=($test_files)
            fi
        fi
    done
    
    # Remove duplicates
    all_test_files=($(printf '%s\n' "${all_test_files[@]}" | sort -u))
    
    if [ ${#all_test_files[@]} -eq 0 ]; then
        echo "ℹ️  No related test files found"
        
        # Check if we should run all tests for critical files
        for file in $CLAUDE_FILE_PATHS; do
            if [[ "$file" =~ (config|setup|requirements|package\.json|go\.mod|Cargo\.toml|pom\.xml) ]]; then
                echo "⚠️  Critical file changed, consider running full test suite"
                break
            fi
        done
        
        exit 0
    fi
    
    echo ""
    echo "Found ${#all_test_files[@]} test file(s) to run"
    
    # Categorize tests
    local categories=$(categorize_tests "${all_test_files[@]}")
    
    # Extract categorized tests
    local unit_tests=$(echo "$categories" | grep "^UNIT:" | cut -d: -f2)
    local integration_tests=$(echo "$categories" | grep "^INTEGRATION:" | cut -d: -f2)
    local e2e_tests=$(echo "$categories" | grep "^E2E:" | cut -d: -f2)
    
    # Run tests in order: unit -> integration -> e2e
    local failed=false
    
    if [ -n "$unit_tests" ]; then
        echo ""
        echo "1️⃣  Running unit tests..."
        if ! run_tests "$framework" $unit_tests; then
            echo "❌ Unit tests failed"
            failed=true
        else
            echo "✅ Unit tests passed"
        fi
    fi
    
    if [ "$failed" = false ] && [ -n "$integration_tests" ]; then
        echo ""
        echo "2️⃣  Running integration tests..."
        if ! run_tests "$framework" $integration_tests; then
            echo "❌ Integration tests failed"
            failed=true
        else
            echo "✅ Integration tests passed"
        fi
    fi
    
    if [ "$failed" = false ] && [ -n "$e2e_tests" ]; then
        echo ""
        echo "3️⃣  Running E2E tests..."
        if ! run_tests "$framework" $e2e_tests; then
            echo "❌ E2E tests failed"
            failed=true
        else
            echo "✅ E2E tests passed"
        fi
    fi
    
    echo ""
    echo "="
    
    if [ "$failed" = true ]; then
        echo "🔴 Tests failed - please fix before continuing"
        # Return exit code 2 to provide feedback to Claude
        exit 2
    else
        echo "🟢 All tests passed!"
        exit 0
    fi
}

# Run main function
main