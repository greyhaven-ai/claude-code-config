# Hook Activation Guide: How Settings Files Work with Claude Code

## Overview

When you place one of these settings files in your project (`.claude/settings.json` or `.claude/settings.local.json`), Claude Code automatically reads it and activates the hooks during your session. Here's exactly what each configuration does and when hooks trigger:

## How Hooks Activate During Claude Interaction

### 1. **settings.minimal.json** - Lightweight Quality Control

**What it does:**
- Automatically runs linter after every code edit
- Checks if work is complete before Claude stops

**Activation flow:**
```
You: "Fix the login bug in auth.py"
Claude: *edits auth.py*
→ PostToolUse triggers → code-linter.sh runs
  → Linter finds issues → Reports to Claude
  → Claude fixes issues automatically

Claude: "I've fixed the bug"
→ Stop event triggers → work-completion-assistant.py runs
  → Checks for TODOs, uncommitted changes
  → Blocks if issues found: "3 TODOs remaining"
  → Claude addresses them before stopping
```

### 2. **settings.recommended.json** - Intelligent Development Assistant

**What it does:**
- Loads context when session starts
- Enhances your prompts with relevant info
- Formats and tests code automatically
- Empowers subagents with context
- Validates work completion

**Activation flow:**
```
SESSION START:
→ SessionStart triggers → branch-context-loader.sh
  → Detects you're on "feature/user-auth" branch
  → Loads related specs, docs, recent commits
  → Shows: "Feature branch detected: user-auth"

You: "Implement the password reset"
→ UserPromptSubmit triggers → prompt-enhancer.py
  → Detects "password reset" keywords
  → Adds: Recent auth changes, test coverage, API docs
  → Claude sees enriched context

Claude: "I'll use a subagent to handle the email service"
→ PreToolUse(Task) triggers → subagent-context-preparer.py
  → Injects project structure, coding standards
  → Subagent gets full context to work independently

Claude: *edits password_reset.py*
→ PostToolUse triggers multiple hooks in parallel:
  → code-linter.sh: Runs ruff, fixes issues
  → auto-formatter.sh: Applies black formatting
  → smart-test-runner.sh: Runs test_password_reset.py

Subagent: "Email service integrated"
→ SubagentStop triggers → subagent-work-validator.py
  → Checks syntax, tests, documentation
  → Validates work quality

Claude: "Feature complete"
→ Stop triggers → work-completion-assistant.py
  → Ensures all tests pass, no TODOs
  → Confirms work is actually done
```

### 3. **settings.complete.json** - Full Automation Suite

**What it does:**
- Everything from recommended PLUS:
- Security validation before edits
- Import organization
- Test data generation
- Performance monitoring
- Migration assistance
- Dependency analysis
- Code similarity detection
- Documentation fetching
- Session documentation

**Activation flow:**
```
You: "Add user profile API endpoint"

Claude: "I'll read the existing API structure"
→ PreToolUse(Read) → auto-documentation-fetcher.py
  → Fetches related API docs automatically

Claude: *starts editing api/users.py*
→ PreToolUse(Edit) → security-validator.py
  → Checks for SQL injection, XSS risks
  → Blocks dangerous patterns

Claude: *completes edit*
→ PostToolUse triggers cascade:
  1. code-linter.sh → Lints with ruff/eslint
  2. auto-formatter.sh → Formats code
  3. incremental-type-checker.sh → Checks types
  4. smart-import-organizer.py → Organizes imports
  5. test-data-generator.py → Creates test fixtures
  6. similar-code-finder.py → Finds duplicate patterns
  7. smart-test-runner.sh → Runs affected tests
  8. coverage-gap-finder.py → Identifies untested code
  9. performance-regression-detector.py → Checks performance

Claude: *creates migration file*
→ PostToolUse(Write) → migration-assistant.py
  → Generates database migration
  → Validates schema changes

Claude: "API endpoint complete"
→ Stop triggers:
  → work-completion-assistant.py → Final validation
  → pre-commit-runner.sh → Runs pre-commit hooks
  → dependency-impact-analyzer.py → Checks breaking changes

SESSION END:
→ SessionEnd → session-documenter.py
  → Creates session summary
  → Documents changes made
```

### 4. **settings.python-focused.json** - Python Development Optimized

**Specific Python behaviors:**
```
Claude: *edits models.py*
→ Triggers Python-specific chain:
  → Ruff linting with pyproject.toml config
  → Import sorting with isort rules
  → Type checking with mypy
  → Test data generation for Django/SQLAlchemy
  → Migration detection and generation
  → Pytest test discovery and execution
  → Coverage.py integration
```

### 5. **settings.javascript-focused.json** - JavaScript/TypeScript Optimized

**Specific JS/TS behaviors:**
```
Claude: *edits components/Button.tsx*
→ Triggers JS-specific chain:
  → ESLint with project config
  → Prettier formatting
  → TypeScript compilation check
  → Import organization (ES6 modules)
  → Jest/Vitest test execution
  → Coverage with c8/nyc
```

## Installation & Activation

### Method 1: Copy Pre-configured Settings
```bash
# For a Python project
cp .claude/templates/settings.python-focused.json .claude/settings.local.json

# For a JavaScript project
cp .claude/templates/settings.javascript-focused.json .claude/settings.local.json

# For general use
cp .claude/templates/settings.recommended.json .claude/settings.local.json
```

### Method 2: Use the Install Script
```bash
./install-hooks.sh
# Select option 2 (Recommended) or 3 (Advanced)
```

### Method 3: Direct Placement
Simply place any settings file at `.claude/settings.json` or `.claude/settings.local.json`

## How Claude Code Processes Hooks

1. **On Startup**: Claude Code reads all settings files in precedence order
2. **During Session**: Monitors for matching events
3. **Event Occurs**: Checks if event has hooks configured
4. **Matcher Check**: For Pre/PostToolUse, checks if tool matches pattern
5. **Execution**: Runs all matching hooks in parallel
6. **Response Handling**:
   - Exit 0: Success, continue normally
   - Exit 2: Blocking error, Claude responds to feedback
   - Other: Non-blocking error, shown to user

## Real-World Examples

### Example 1: Automatic Code Quality
```
You: "Create a user authentication system"
Claude: *creates auth.py with login function*
→ Linter runs → finds missing type hints
→ Claude adds type hints automatically
→ Formatter runs → fixes indentation
→ Test runner creates test_auth.py
→ Coverage finder suggests edge cases
→ Claude adds edge case handling
Result: Production-ready code without manual intervention
```

### Example 2: Smart Context Loading
```
You: "Fix the bug reported in issue #123"
→ Prompt enhancer fetches issue details
→ Adds recent commits touching affected files
→ Includes test failures from CI
Claude: "I can see issue #123 is about the race condition in..."
Result: Claude has full context without manual explanation
```

### Example 3: Subagent Empowerment
```
You: "Refactor the payment processing module"
Claude: "I'll use a subagent for this complex task"
→ Context preparer injects:
  - Current payment flow architecture
  - Testing patterns used in codebase
  - Performance benchmarks
  - Security requirements
Subagent: Works independently with full knowledge
Result: Consistent refactoring matching project standards
```

## Benefits of Pre-configured Settings

1. **Zero Setup**: Copy one file, everything works
2. **Consistency**: Same workflow across all projects
3. **No Manual Steps**: No need to navigate /hooks menu
4. **Team Sharing**: Commit settings.json for team-wide standards
5. **Customizable**: Easy to modify for project needs
6. **Progressive**: Start minimal, add complexity as needed

## Troubleshooting

If hooks aren't activating:

1. **Check file location**: Must be in `.claude/` directory
2. **Verify JSON syntax**: Use `jq . .claude/settings.json` to validate
3. **Check hook permissions**: `chmod +x .claude/hooks/**/*.{sh,py,js}`
4. **Debug mode**: Run `claude --debug` to see hook execution
5. **Verify paths**: Ensure `$CLAUDE_PROJECT_DIR` is used for project paths

## Summary

These settings files transform Claude Code from a helpful assistant into an intelligent development environment that:

- **Knows** your project structure and standards
- **Prevents** errors before they happen
- **Fixes** issues automatically
- **Tests** changes immediately
- **Validates** work completeness
- **Documents** everything done

Just place the appropriate settings file in your project, and Claude Code handles the rest automatically!