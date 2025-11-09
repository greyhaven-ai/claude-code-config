#!/bin/bash
# Branch Context Loader Hook
# ==========================
# Type: SessionStart
# Description: Detects current git branch and loads appropriate context
#
# This hook runs when a Claude Code session starts and automatically
# loads relevant context based on the branch naming pattern.

set -euo pipefail

# Function to load context based on branch pattern
load_branch_context() {
    local branch=$1
    local project_dir="${CLAUDE_PROJECT_DIR:-$(pwd)}"
    
    echo "=" 
    echo "🌿 Branch Context Loader"
    echo "="
    echo "Current branch: $branch"
    echo ""
    
    # Feature branches - load specs and related docs
    if [[ "$branch" =~ ^feature/(.+)$ ]]; then
        local feature_name="${BASH_REMATCH[1]}"
        echo "📋 Feature Branch Detected: $feature_name"
        echo ""
        
        # Look for related specification files
        if [ -d "$project_dir/specs" ]; then
            echo "📄 Related Specifications:"
            find "$project_dir/specs" -type f -name "*${feature_name}*" 2>/dev/null | head -5 | while read -r file; do
                echo "  • ${file#$project_dir/}"
            done
        fi
        
        # Look for related documentation
        if [ -d "$project_dir/docs" ]; then
            echo "📚 Related Documentation:"
            find "$project_dir/docs" -type f -name "*${feature_name}*" 2>/dev/null | head -5 | while read -r file; do
                echo "  • ${file#$project_dir/}"
            done
        fi
        
        # Check for related Linear tickets
        echo ""
        echo "💡 Tips for feature development:"
        echo "  • Check acceptance criteria in ticket"
        echo "  • Write tests first (TDD approach)"
        echo "  • Update documentation as you go"
        
    # Bugfix branches - load error logs and test files
    elif [[ "$branch" =~ ^(bugfix|fix|hotfix)/(.+)$ ]]; then
        local bug_name="${BASH_REMATCH[2]}"
        echo "🐛 Bugfix Branch Detected: $bug_name"
        echo ""
        
        # Show recent test failures
        if [ -d "$project_dir/.pytest_cache" ] || [ -d "$project_dir/test-results" ]; then
            echo "🧪 Recent Test Information:"
            # Check for pytest cache
            if [ -f "$project_dir/.pytest_cache/v/cache/lastfailed" ]; then
                echo "  • Failed tests found in pytest cache"
            fi
            # Check for test results
            if [ -d "$project_dir/test-results" ]; then
                local failed_count=$(find "$project_dir/test-results" -name "*.xml" -exec grep -l 'failure\|error' {} \; 2>/dev/null | wc -l)
                if [ "$failed_count" -gt 0 ]; then
                    echo "  • $failed_count test result files with failures"
                fi
            fi
        fi
        
        # Look for error logs
        if [ -d "$project_dir/logs" ]; then
            echo "📝 Recent Error Logs:"
            find "$project_dir/logs" -type f -name "*.log" -exec grep -l -i "error\|exception" {} \; 2>/dev/null | head -3 | while read -r file; do
                echo "  • ${file#$project_dir/}"
            done
        fi
        
        echo ""
        echo "💡 Debugging tips:"
        echo "  • Check recent commits that touched affected files"
        echo "  • Look for similar past issues"
        echo "  • Run tests in isolation first"
        
    # Release branches - load changelog and version files
    elif [[ "$branch" =~ ^release/(.+)$ ]]; then
        local release_version="${BASH_REMATCH[1]}"
        echo "🚀 Release Branch Detected: $release_version"
        echo ""
        
        # Show version files
        for version_file in "package.json" "pyproject.toml" "Cargo.toml" "go.mod" "pom.xml"; do
            if [ -f "$project_dir/$version_file" ]; then
                echo "📦 Version file: $version_file"
                grep -E "version|Version" "$project_dir/$version_file" | head -1 || true
            fi
        done
        
        # Show changelog
        if [ -f "$project_dir/CHANGELOG.md" ]; then
            echo ""
            echo "📋 Recent Changelog Entries:"
            head -20 "$project_dir/CHANGELOG.md" | grep -E "^#{1,3} |^- " | head -5 || true
        fi
        
        echo ""
        echo "💡 Release checklist:"
        echo "  • Update version numbers"
        echo "  • Update CHANGELOG.md"
        echo "  • Run full test suite"
        echo "  • Check dependency versions"
        
    # Refactor branches
    elif [[ "$branch" =~ ^refactor/(.+)$ ]]; then
        local refactor_target="${BASH_REMATCH[1]}"
        echo "♻️ Refactor Branch Detected: $refactor_target"
        echo ""
        
        echo "💡 Refactoring guidelines:"
        echo "  • Maintain backward compatibility"
        echo "  • Keep tests passing at each step"
        echo "  • Update affected documentation"
        echo "  • Consider performance implications"
        
    # Main/master branch
    elif [[ "$branch" == "main" ]] || [[ "$branch" == "master" ]]; then
        echo "🏠 Main Branch"
        echo ""
        
        # Show recent releases
        local recent_tags=$(git tag --sort=-creatordate | head -3 2>/dev/null)
        if [ -n "$recent_tags" ]; then
            echo "🏷️ Recent releases:"
            echo "$recent_tags" | while read -r tag; do
                echo "  • $tag"
            done
        fi
        
        # Show branch protection status
        echo ""
        echo "⚠️ Main branch guidelines:"
        echo "  • Direct commits may be restricted"
        echo "  • Changes should go through PR process"
        echo "  • Ensure CI/CD passes before merging"
    fi
    
    # Universal context - always show
    echo ""
    echo "📊 Repository Statistics:"
    
    # Count files by type
    echo "  File counts:"
    for ext in py js ts jsx tsx go rs java cpp c; do
        count=$(find "$project_dir" -name "*.${ext}" -type f 2>/dev/null | wc -l)
        if [ "$count" -gt 0 ]; then
            echo "    • .${ext}: $count files"
        fi
    done
    
    # Recent commit activity
    echo ""
    echo "📈 Recent Activity (last 5 commits):"
    git log --oneline -5 2>/dev/null | while read -r line; do
        echo "  $line"
    done
    
    # Check for uncommitted changes
    echo ""
    local changes=$(git status --porcelain 2>/dev/null | wc -l)
    if [ "$changes" -gt 0 ]; then
        echo "⚠️ You have $changes uncommitted changes"
        git status --short 2>/dev/null | head -5
    else
        echo "✅ Working directory is clean"
    fi
    
    echo "="
}

# Main execution
main() {
    # Get current branch
    local branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "no-branch")
    
    if [ "$branch" == "no-branch" ]; then
        echo "⚠️ Not in a git repository or no branch detected"
        exit 0
    fi
    
    # Load context based on branch
    load_branch_context "$branch"
}

# Run main function
main