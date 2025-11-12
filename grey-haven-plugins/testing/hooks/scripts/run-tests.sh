#!/bin/bash
# Auto-run tests after code changes
# Part of testing plugin quality enforcement

set -e

# Check if files were modified
if [ -z "$CLAUDE_FILE_PATHS" ]; then
    exit 0
fi

test_failures=()
tests_run=()

# Process each modified file
for file in $CLAUDE_FILE_PATHS; do
    if [ ! -f "$file" ]; then
        continue
    fi

    case "$file" in
        *.py)
            # Run Python tests with pytest
            if command -v pytest &> /dev/null; then
                # Check if this is a test file
                if [[ "$file" =~ test_.*\.py$ ]] || [[ "$file" =~ .*_test\.py$ ]]; then
                    echo "🧪 Running pytest for $file..."
                    if pytest "$file" -v --tb=short 2>&1; then
                        tests_run+=("$file (pytest)")
                    else
                        test_failures+=("$file: pytest tests failed")
                    fi
                else
                    # Try to find and run related test file
                    test_file=""
                    if [[ "$file" =~ ^(.*/)?([^/]+)\.py$ ]]; then
                        dir="${BASH_REMATCH[1]}"
                        name="${BASH_REMATCH[2]}"

                        # Try common test patterns
                        for pattern in "test_${name}.py" "${name}_test.py" "tests/test_${name}.py" "tests/${name}_test.py"; do
                            if [ -f "$pattern" ]; then
                                test_file="$pattern"
                                break
                            fi
                        done

                        if [ -n "$test_file" ]; then
                            echo "🧪 Running related tests: $test_file..."
                            if pytest "$test_file" -v --tb=short 2>&1; then
                                tests_run+=("$test_file (related to $file)")
                            else
                                test_failures+=("$test_file: related tests failed")
                            fi
                        fi
                    fi
                fi
            fi
            ;;

        *.js|*.jsx|*.ts|*.tsx)
            # Run JavaScript/TypeScript tests
            if command -v npm &> /dev/null && [ -f "package.json" ]; then
                # Check if this is a test file
                if [[ "$file" =~ \.test\.(js|jsx|ts|tsx)$ ]] || [[ "$file" =~ \.spec\.(js|jsx|ts|tsx)$ ]]; then
                    echo "🧪 Running tests for $file..."
                    if npm test -- --findRelatedTests "$file" --passWithNoTests 2>&1; then
                        tests_run+=("$file (npm test)")
                    else
                        test_failures+=("$file: npm tests failed")
                    fi
                else
                    # Try to find and run related tests
                    echo "🧪 Running related tests for $file..."
                    if npm test -- --findRelatedTests "$file" --passWithNoTests 2>&1; then
                        tests_run+=("$file related tests")
                    else
                        test_failures+=("$file: related tests failed")
                    fi
                fi
            fi
            ;;

        *.go)
            # Run Go tests
            if command -v go &> /dev/null; then
                if [[ "$file" =~ _test\.go$ ]]; then
                    dir=$(dirname "$file")
                    echo "🧪 Running go test in $dir..."
                    if (cd "$dir" && go test -v 2>&1); then
                        tests_run+=("$file (go test)")
                    else
                        test_failures+=("$file: go tests failed")
                    fi
                fi
            fi
            ;;
    esac
done

# Report results
if [ ${#tests_run[@]} -gt 0 ]; then
    echo ""
    echo "✅ Tests passed for ${#tests_run[@]} file(s):"
    printf '   - %s\n' "${tests_run[@]}"
fi

if [ ${#test_failures[@]} -gt 0 ]; then
    echo "" >&2
    echo "❌ TEST FAILURES DETECTED:" >&2
    printf '   - %s\n' "${test_failures[@]}" >&2
    echo "" >&2
    echo "Tests must pass before proceeding. Please fix the failing tests." >&2
    # Exit code 2 = blocking error (feedback sent to Claude)
    exit 2
fi

exit 0
