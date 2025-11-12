#!/bin/bash
# Sync Linear issue status based on git/development activity
# Provides reminders to update Linear issues

set -e

# Only run for git-related commands
if [ -z "$CLAUDE_TOOL_INPUT" ]; then
    exit 0
fi

# Check if this is a git commit or PR-related command
if ! echo "$CLAUDE_TOOL_INPUT" | grep -q -E "git commit|git push|gh pr"; then
    # Not a git command, skip Linear sync
    exit 0
fi

echo "📋 Checking Linear issue tracking..."

suggestions=()
warnings=()

# Extract Linear issue IDs from recent commit messages
# Linear issue format: ABC-123, PROJECT-456, etc.
if git rev-parse --git-dir > /dev/null 2>&1; then
    # Get the most recent commit message
    if commit_msg=$(git log -1 --pretty=%B 2>/dev/null); then
        # Look for Linear issue references (format: ABC-123)
        if issue_id=$(echo "$commit_msg" | grep -oE '[A-Z]+-[0-9]+' | head -1); then
            echo "✅ Found Linear issue reference: $issue_id"

            # Check if linear CLI is available
            if command -v linear &> /dev/null; then
                # Try to get issue status
                if issue_status=$(linear issue view "$issue_id" --format json 2>/dev/null | jq -r '.state.name' 2>/dev/null); then
                    echo "   Current status: $issue_status"

                    # Check if status should be updated based on git action
                    if echo "$CLAUDE_TOOL_INPUT" | grep -q "git push"; then
                        if [ "$issue_status" = "Todo" ] || [ "$issue_status" = "Backlog" ]; then
                            suggestions+=("Consider moving $issue_id to 'In Progress' since you're pushing code")
                        fi
                    fi

                    if echo "$CLAUDE_TOOL_INPUT" | grep -q "gh pr create"; then
                        if [ "$issue_status" != "In Review" ]; then
                            suggestions+=("Consider moving $issue_id to 'In Review' since you created a PR")
                        fi
                    fi
                else
                    warnings+=("Could not fetch status for $issue_id - verify issue exists")
                fi
            else
                suggestions+=("Linear CLI not installed - consider installing for automatic status updates (npm install -g @linear/cli)")
            fi
        else
            # No Linear issue reference found
            if echo "$CLAUDE_TOOL_INPUT" | grep -q "git commit"; then
                # Check if this is a feature/fix commit (not docs, chore, etc.)
                if echo "$commit_msg" | grep -q -E "^(feat|fix|feature):"; then
                    warnings+=("Feature/fix commit but no Linear issue reference found (format: ABC-123)")
                fi
            fi
        fi
    fi
fi

# Check for branch naming convention with Linear issues
if git rev-parse --git-dir > /dev/null 2>&1; then
    branch_name=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "")

    # Check if branch follows Linear convention (e.g., ABC-123-feature-name)
    if [[ "$branch_name" =~ ^[A-Z]+-[0-9]+ ]]; then
        branch_issue_id=$(echo "$branch_name" | grep -oE '^[A-Z]+-[0-9]+')
        echo "✅ Branch follows Linear naming: $branch_issue_id"

        # Check if this matches commit message issue ID
        if [ -n "$issue_id" ] && [ "$issue_id" != "$branch_issue_id" ]; then
            warnings+=("Branch issue ($branch_issue_id) differs from commit issue ($issue_id)")
        fi
    fi
fi

# Report results
if [ ${#warnings[@]} -gt 0 ]; then
    echo "⚠️  Linear tracking warnings:"
    printf '   - %s\n' "${warnings[@]}"
    echo ""
fi

if [ ${#suggestions[@]} -gt 0 ]; then
    echo "💡 Linear status suggestions:"
    printf '   - %s\n' "${suggestions[@]}"
    echo ""
fi

# Check for LINEAR_API_KEY if Linear CLI detected but not configured
if command -v linear &> /dev/null; then
    if [ -z "$LINEAR_API_KEY" ]; then
        echo "💡 Tip: Set LINEAR_API_KEY environment variable for automatic Linear updates"
    fi
fi

# Don't block - these are just suggestions
exit 0
