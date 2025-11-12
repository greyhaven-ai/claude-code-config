#!/bin/bash
# Check if documentation is in sync with code changes
# Warns when code changes may require documentation updates

set -e

# Check if files were modified
if [ -z "$CLAUDE_FILE_PATHS" ]; then
    exit 0
fi

warnings=()
suggestions=()

# Track if documentation was updated
docs_updated=false
code_updated=false

# Analyze each modified file
for file in $CLAUDE_FILE_PATHS; do
    if [ ! -f "$file" ]; then
        continue
    fi

    # Check if documentation file
    case "$file" in
        README.md|CHANGELOG.md|*.md)
            docs_updated=true
            ;;
        docs/*|documentation/*|guides/*)
            docs_updated=true
            ;;
        *openapi.yaml|*openapi.json|*swagger.yaml|*swagger.json)
            docs_updated=true
            ;;
        *)
            # Check if it's a code file
            case "$file" in
                *.py|*.js|*.ts|*.jsx|*.tsx|*.go|*.rs|*.java|*.rb|*.php)
                    code_updated=true
                    ;;
            esac
            ;;
    esac
done

# If code was updated but docs weren't, suggest updates
if [ "$code_updated" = true ] && [ "$docs_updated" = false ]; then
    # Check what type of changes were made
    for file in $CLAUDE_FILE_PATHS; do
        case "$file" in
            */api/*|*/routes/*|*/endpoints/*|*/controllers/*)
                suggestions+=("API changes detected in $file - consider updating API documentation")
                ;;
            */models/*|*/schema/*|*/database/*)
                suggestions+=("Data model changes in $file - verify schema documentation is current")
                ;;
            */config/*|*.config.js|*.config.ts|*rc.json)
                suggestions+=("Configuration changes in $file - update configuration documentation")
                ;;
            */cli/*|*/commands/*)
                suggestions+=("CLI changes in $file - update command documentation and help text")
                ;;
        esac
    done
fi

# Check for missing CHANGELOG entry
if [ "$code_updated" = true ]; then
    if [ -f "CHANGELOG.md" ]; then
        # Check if CHANGELOG was modified recently (within this session)
        found_in_files=false
        for file in $CLAUDE_FILE_PATHS; do
            if [ "$file" = "CHANGELOG.md" ]; then
                found_in_files=true
                break
            fi
        done

        if [ "$found_in_files" = false ]; then
            warnings+=("Code changes made but CHANGELOG.md not updated")
        fi
    fi
fi

# Check for package.json changes without README update
if echo "$CLAUDE_FILE_PATHS" | grep -q "package.json"; then
    if ! echo "$CLAUDE_FILE_PATHS" | grep -q "README.md"; then
        suggestions+=("package.json modified - verify README.md reflects any new dependencies or scripts")
    fi
fi

# Check for new environment variables
for file in $CLAUDE_FILE_PATHS; do
    if [ -f "$file" ]; then
        # Look for new environment variable usage
        if grep -q "process\.env\.\|os\.getenv\|ENV\[" "$file" 2>/dev/null; then
            if [ ! -f ".env.example" ] || ! echo "$CLAUDE_FILE_PATHS" | grep -q ".env.example"; then
                suggestions+=("Environment variables used in $file - ensure .env.example is updated")
            fi
        fi
    fi
done

# Check for breaking changes in API files
for file in $CLAUDE_FILE_PATHS; do
    if [ -f "$file" ]; then
        # Simple heuristic: look for removed functions/endpoints
        if git diff HEAD "$file" 2>/dev/null | grep -q "^-.*def \|^-.*function \|^-.*export "; then
            warnings+=("Functions/exports removed in $file - document breaking changes and migration path")
        fi
    fi
done

# Report results
if [ ${#warnings[@]} -gt 0 ]; then
    echo "⚠️  Documentation warnings:" >&2
    printf '   - %s\n' "${warnings[@]}" >&2
    echo "" >&2
fi

if [ ${#suggestions[@]} -gt 0 ]; then
    echo "💡 Documentation suggestions:"
    printf '   - %s\n' "${suggestions[@]}"
    echo ""
fi

# Check for common documentation files
if [ "$code_updated" = true ]; then
    echo "📚 Verify these documentation files are current:"
    [ -f "README.md" ] && echo "   - README.md"
    [ -f "CHANGELOG.md" ] && echo "   - CHANGELOG.md"
    [ -d "docs" ] && echo "   - docs/ directory"
    [ -f ".env.example" ] && echo "   - .env.example"
    [ -f "API.md" ] && echo "   - API.md"
fi

# Don't block - these are just reminders
exit 0
