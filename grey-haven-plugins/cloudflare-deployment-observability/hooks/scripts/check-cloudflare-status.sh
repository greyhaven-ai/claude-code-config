#!/bin/bash
# Check Cloudflare deployment status after bash commands
# Only runs if Cloudflare-related commands detected

set -e

# Check if this was a Cloudflare-related command
if [ -z "$CLAUDE_TOOL_INPUT" ]; then
    exit 0
fi

# Check if command involves Cloudflare deployments
if ! echo "$CLAUDE_TOOL_INPUT" | grep -q -E "wrangler|cloudflare|cf-|pages:deploy"; then
    # Not a Cloudflare command, skip checks
    exit 0
fi

echo "☁️  Cloudflare deployment detected, running health checks..."

warnings=()
errors=()

# Check if wrangler CLI is available
if command -v wrangler &> /dev/null; then
    # Check wrangler deployments
    if wrangler deployments list 2>&1 | grep -q "FAILED"; then
        errors+=("Recent Wrangler deployment failed")
    fi

    # Check wrangler whoami to verify authentication
    if ! wrangler whoami &> /dev/null; then
        warnings+=("Wrangler authentication may have expired")
    fi
else
    # Wrangler not installed, check if it should be
    if echo "$CLAUDE_TOOL_INPUT" | grep -q "wrangler"; then
        warnings+=("Wrangler CLI not installed but wrangler command was used")
    fi
fi

# Check for common Cloudflare environment variables
if echo "$CLAUDE_TOOL_INPUT" | grep -q -E "wrangler|cloudflare"; then
    if [ -z "$CLOUDFLARE_API_TOKEN" ] && [ -z "$CLOUDFLARE_ACCOUNT_ID" ]; then
        warnings+=("Cloudflare environment variables not set (CLOUDFLARE_API_TOKEN, CLOUDFLARE_ACCOUNT_ID)")
    fi
fi

# Check for Pages deployment commands
if echo "$CLAUDE_TOOL_INPUT" | grep -q "pages:deploy\|pages publish"; then
    # Verify build output exists
    if [ -d "dist" ] || [ -d "build" ] || [ -d "public" ]; then
        echo "✅ Build output directory found"
    else
        warnings+=("Pages deployment but no standard build directory (dist/build/public) found")
    fi
fi

# Check for Workers deployment
if echo "$CLAUDE_TOOL_INPUT" | grep -q "wrangler publish\|wrangler deploy"; then
    # Check if wrangler.toml exists
    if [ ! -f "wrangler.toml" ] && [ ! -f "wrangler.json" ]; then
        errors+=("Workers deployment but no wrangler.toml configuration found")
    fi
fi

# Report results
if [ ${#errors[@]} -gt 0 ]; then
    echo "❌ Cloudflare deployment errors:" >&2
    printf '   - %s\n' "${errors[@]}" >&2
    exit 2  # Blocking error
fi

if [ ${#warnings[@]} -gt 0 ]; then
    echo "⚠️  Cloudflare deployment warnings:"
    printf '   - %s\n' "${warnings[@]}"
    echo ""
    echo "💡 Verify these warnings don't affect your deployment."
fi

echo "✅ Cloudflare health checks passed"
exit 0
