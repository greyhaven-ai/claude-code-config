#!/bin/bash
# Auto-format and lint code after edits
# Part of core plugin TDD enforcement

set -e

# Check if files were modified
if [ -z "$CLAUDE_FILE_PATHS" ]; then
    exit 0
fi

formatted_files=()
linted_files=()
errors=()

# Process each modified file
for file in $CLAUDE_FILE_PATHS; do
    if [ ! -f "$file" ]; then
        continue
    fi

    case "$file" in
        *.py)
            # Format Python with black
            if command -v black &> /dev/null; then
                if black "$file" 2>&1; then
                    formatted_files+=("$file (black)")
                fi
            fi

            # Lint Python with ruff
            if command -v ruff &> /dev/null; then
                if ruff check --fix "$file" 2>&1; then
                    linted_files+=("$file (ruff)")
                else
                    errors+=("$file: ruff found issues")
                fi
            fi
            ;;

        *.js|*.jsx|*.ts|*.tsx)
            # Format JavaScript/TypeScript with prettier
            if command -v prettier &> /dev/null; then
                if prettier --write "$file" 2>&1; then
                    formatted_files+=("$file (prettier)")
                fi
            fi

            # Lint with eslint
            if command -v eslint &> /dev/null; then
                if eslint --fix "$file" 2>&1; then
                    linted_files+=("$file (eslint)")
                else
                    errors+=("$file: eslint found issues")
                fi
            fi
            ;;

        *.go)
            # Format Go with gofmt
            if command -v gofmt &> /dev/null; then
                if gofmt -w "$file" 2>&1; then
                    formatted_files+=("$file (gofmt)")
                fi
            fi
            ;;

        *.rs)
            # Format Rust with rustfmt
            if command -v rustfmt &> /dev/null; then
                if rustfmt "$file" 2>&1; then
                    formatted_files+=("$file (rustfmt)")
                fi
            fi
            ;;
    esac
done

# Report results
if [ ${#formatted_files[@]} -gt 0 ]; then
    echo "✅ Formatted ${#formatted_files[@]} file(s):"
    printf '   - %s\n' "${formatted_files[@]}"
fi

if [ ${#linted_files[@]} -gt 0 ]; then
    echo "✅ Linted ${#linted_files[@]} file(s):"
    printf '   - %s\n' "${linted_files[@]}"
fi

if [ ${#errors[@]} -gt 0 ]; then
    echo "⚠️  Linting errors found:" >&2
    printf '   - %s\n' "${errors[@]}" >&2
    # Don't block - just warn
    exit 0
fi

exit 0
