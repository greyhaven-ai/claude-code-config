#!/bin/bash
# Performance analysis for code changes
# Part of observability plugin

set -e

# Check if files were modified
if [ -z "$CLAUDE_FILE_PATHS" ]; then
    exit 0
fi

warnings=()
errors=()

# Analyze each modified file for performance issues
for file in $CLAUDE_FILE_PATHS; do
    if [ ! -f "$file" ]; then
        continue
    fi

    case "$file" in
        *.py)
            # Check for nested loops (potential O(n²) complexity)
            nested_loops=$(grep -n "^\s*for\s" "$file" | wc -l)
            if [ "$nested_loops" -gt 5 ]; then
                warnings+=("$file: $nested_loops for-loops detected - review for nested iterations")
            fi

            # Check for queries in loops (N+1 pattern)
            if grep -q "for\s.*:" "$file" && grep -q -E "(query|select|filter|get\()" "$file"; then
                # Basic heuristic: if file has loops and query methods
                warnings+=("$file: Potential N+1 query pattern - verify queries aren't in loops")
            fi

            # Check for missing database indices hints
            if grep -q -E "filter\(|where\(" "$file" && ! grep -q "index" "$file"; then
                warnings+=("$file: Database queries present - verify indices exist for filters")
            fi

            # Check for proper async usage
            if grep -q -E "requests\.(get|post)" "$file" && ! grep -q "async" "$file"; then
                warnings+=("$file: Synchronous HTTP requests detected - consider async for better performance")
            fi

            # Run complexity analysis if radon is available
            if command -v radon &> /dev/null; then
                complex_functions=$(radon cc "$file" -s -n C 2>&1 | grep -v "^$" || true)
                if [ -n "$complex_functions" ]; then
                    warnings+=("$file: High complexity functions detected:\n$complex_functions")
                fi
            fi
            ;;

        *.js|*.jsx|*.ts|*.tsx)
            # Check for nested loops
            nested_loops=$(grep -n "^\s*for\s*(" "$file" | wc -l)
            if [ "$nested_loops" -gt 5 ]; then
                warnings+=("$file: $nested_loops for-loops detected - review for nested iterations")
            fi

            # Check for queries in loops
            if grep -q "\.map\|\.forEach\|for\s*(" "$file" && grep -q -E "query|find|filter" "$file"; then
                warnings+=("$file: Potential N+1 query pattern - verify queries aren't in iteration callbacks")
            fi

            # Check for missing React.memo/useMemo
            if grep -q "export.*function.*Component" "$file" && ! grep -q -E "React\.memo|useMemo|useCallback" "$file"; then
                warnings+=("$file: React component without memoization - consider React.memo for expensive components")
            fi

            # Check for synchronous API calls
            if grep -q "fetch(" "$file" && ! grep -q "await" "$file"; then
                warnings+=("$file: fetch() without await - ensure proper async handling")
            fi
            ;;

        *.sql)
            # Check for missing WHERE clauses (potential full table scans)
            if grep -q -i "SELECT.*FROM" "$file" && ! grep -q -i "WHERE" "$file"; then
                warnings+=("$file: SELECT without WHERE - potential full table scan")
            fi

            # Check for SELECT * queries
            if grep -q -i "SELECT \*" "$file"; then
                warnings+=("$file: SELECT * detected - specify columns for better performance")
            fi

            # Check for missing indices hints
            if ! grep -q -i "INDEX\|KEY" "$file"; then
                warnings+=("$file: No index definitions found - verify indices exist for queries")
            fi
            ;;
    esac

    # Check for common resource leak patterns across all file types
    if grep -q -E "open\(|connect\(|socket\(" "$file" && ! grep -q -E "close\(|with\s|finally" "$file"; then
        warnings+=("$file: Resource acquisition without explicit cleanup - verify proper resource management")
    fi

    # Check for large data loading
    if grep -q -E "\.all\(\)|load_all|fetchall|find\(\)" "$file" && ! grep -q -E "limit\(|paginate|chunk" "$file"; then
        warnings+=("$file: Loading all records without pagination - consider pagination for large datasets")
    fi
done

# Report results
if [ ${#warnings[@]} -gt 0 ]; then
    echo "⚠️  Performance warnings detected:" >&2
    printf '   %s\n' "${warnings[@]}" >&2
    echo "" >&2
    echo "💡 These are heuristic checks - review if applicable to your changes." >&2
    # Don't block - these are warnings only
fi

if [ ${#errors[@]} -gt 0 ]; then
    echo "❌ Performance errors detected:" >&2
    printf '   %s\n' "${errors[@]}" >&2
    exit 2  # Blocking error
fi

# If radon installed, show complexity summary
if command -v radon &> /dev/null; then
    for file in $CLAUDE_FILE_PATHS; do
        if [[ "$file" == *.py ]]; then
            echo "📊 Complexity analysis for $file:"
            radon cc "$file" -s 2>&1 || true
        fi
    done
fi

exit 0
