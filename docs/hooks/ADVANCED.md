# Advanced Hook Workflows for Claude Code

This guide explains how to combine hooks to create powerful, automated development workflows that empower both developers and subagents.

## Quick Start

1. **Install the advanced hooks:**
   ```bash
   cd /path/to/your/project
   cp -r /path/to/grey-haven-claude-code-config/.claude/hooks .claude/
   ```

2. **Apply the advanced workflow configuration:**
   ```bash
   cp .claude/hooks/examples/advanced-workflow-settings.json .claude/settings.json
   ```

3. **Make hooks executable:**
   ```bash
   chmod +x .claude/hooks/**/*.{sh,py,js}
   ```

## Core Workflow Components

### 1. Intelligent Context Management

**Purpose:** Automatically load relevant context based on your current work.

**Hooks:**
- `branch-context-loader.sh` (SessionStart) - Loads context based on git branch
- `prompt-enhancer.py` (UserPromptSubmit) - Enhances prompts with relevant info
- `smart-context-injector.py` (SessionStart) - Injects project-specific context

**How it works:**
1. When session starts, branch context identifies your work type (feature/bugfix/release)
2. Smart context injector loads relevant docs, specs, and recent changes
3. When you submit prompts, enhancer adds test coverage, dependencies, and related files

**Example Flow:**
```
You: "Fix the login bug"
Hook adds: Current branch info, recent login-related commits, test coverage for auth files
Claude sees: Enhanced context helping it understand the specific issue
```

### 2. Automated Quality Assurance Pipeline

**Purpose:** Ensure code quality without manual intervention.

**Hooks:**
- `code-linter.sh` (PostToolUse) - Runs appropriate linters
- `auto-formatter.sh` (PostToolUse) - Formats code automatically
- `incremental-type-checker.sh` (PostToolUse) - Checks types
- `security-validator.py` (PreToolUse) - Prevents security issues
- `test-runner.sh` (PostToolUse/Stop) - Runs affected tests

**How it works:**
1. Before edits, security validator checks for dangerous patterns
2. After edits, linter → formatter → type checker run in sequence
3. Smart test runner identifies and runs only affected tests
4. On Stop, work completion assistant ensures everything passes

**Example Flow:**
```
Claude edits auth.py
→ Linter runs ruff
→ Formatter applies black
→ Type checker runs mypy
→ Test runner executes auth_test.py
→ You see: "✅ All checks passed"
```

### 3. Subagent Empowerment Framework

**Purpose:** Give subagents the context they need to work independently.

**Hooks:**
- `subagent-context-preparer.py` (PreToolUse:Task) - Prepares context for subagents
- `subagent-work-validator.py` (SubagentStop/PostToolUse:Task) - Validates work

**How it works:**
1. When launching a subagent, context preparer analyzes the task
2. Injects project structure, coding standards, similar implementations
3. When subagent finishes, validator checks syntax, tests, documentation
4. Blocks completion if critical issues found

**Example Flow:**
```
You: "Task: Implement user profile API endpoint"
Hook adds: Project structure, existing API patterns, test examples
Subagent: Creates endpoint following existing patterns
Validator: Checks syntax ✓, suggests adding tests, validates imports ✓
```

### 4. Smart Development Assistant

**Purpose:** Anticipate needs and automate routine tasks.

**Hooks:**
- `work-completion-assistant.py` (Stop) - Ensures work is complete
- `test-data-generator.py` (PostToolUse) - Generates test data
- `migration-assistant.py` (PostToolUse) - Helps with database migrations

**How it works:**
1. After code changes, test data generator creates fixtures
2. Migration assistant detects model changes and suggests migrations
3. Before stopping, completion assistant checks for TODOs, tests, commits

**Example Flow:**
```
Claude implements feature
→ Test data generator creates fixtures
→ Claude tries to stop
→ Completion assistant: "❌ 3 TODOs remaining, tests not run"
→ Claude addresses issues
→ "✅ Work complete!"
```

## Advanced Patterns

### Pattern 1: Progressive Enhancement

Start simple, add sophistication:

```json
{
  "PostToolUse": [{
    "matcher": "Edit",
    "hooks": [
      {"command": "quick-check.sh", "timeout": 5},
      {"command": "deep-analysis.py", "timeout": 30},
      {"command": "ai-review.py", "timeout": 60}
    ]
  }]
}
```

### Pattern 2: Context-Aware Decisions

Hooks that adapt to project state:

```python
# In a hook
if branch in ['main', 'master']:
    return {"permissionDecision": "ask"}  # Require approval
else:
    return {"permissionDecision": "allow"}  # Auto-approve
```

### Pattern 3: Collaborative Hooks

Multiple hooks building understanding:

```json
{
  "SessionStart": [{
    "hooks": [
      {"command": "gather-metrics.py"},
      {"command": "analyze-issues.py"},
      {"command": "load-preferences.py"}
    ]
  }]
}
```

## Common Workflows

### The "Perfect PR" Workflow

1. **SessionStart**: Load PR template and guidelines
2. **UserPromptSubmit**: Enhance with issue context
3. **PostToolUse**: Format, lint, test each change
4. **Stop**: Generate commit message, update changelog
5. **SessionEnd**: Create PR with full context

### The "Zero-Touch Testing" Workflow

1. **PostToolUse(Write/Edit)**: Detect new functions
2. **Auto-generate**: Test stubs with coverage-gap-finder
3. **Run tests**: With test-runner
4. **Stop**: Block if coverage drops

### The "Subagent Army" Workflow

1. **UserPromptSubmit**: Detect complex task
2. **Suggest**: Breaking into subtasks
3. **PreToolUse(Task)**: Enhance each with context
4. **SubagentStop**: Validate and integrate work
5. **Stop**: Ensure all subtasks complete

## Configuration Examples

### Minimal Setup (Start Here)

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [
        {"type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/bash/code-linter.sh"}
      ]
    }],
    "Stop": [{
      "hooks": [
        {"type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/python/work-completion-assistant.py"}
      ]
    }]
  }
}
```

### Recommended Setup

```json
{
  "hooks": {
    "SessionStart": [{
      "hooks": [
        {"type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/bash/branch-context-loader.sh"}
      ]
    }],
    "UserPromptSubmit": [{
      "hooks": [
        {"type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/python/prompt-enhancer.py"}
      ]
    }],
    "PostToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [
        {"type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/bash/code-linter.sh"},
        {"type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/bash/test-runner.sh"}
      ]
    }],
    "Stop": [{
      "hooks": [
        {"type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/python/work-completion-assistant.py"}
      ]
    }]
  }
}
```

### Full Advanced Setup

See `.claude/hooks/examples/advanced-workflow-settings.json`

## Performance Considerations

1. **Use timeouts**: Prevent hooks from blocking indefinitely
   ```json
   {"type": "command", "command": "slow-hook.py", "timeout": 30}
   ```

2. **Parallel execution**: Hooks run in parallel by default
   - Order them by priority if dependencies exist

3. **Exit early**: Hooks should exit 0 quickly if not applicable
   ```python
   if not relevant:
       sys.exit(0)  # Don't block
   ```

4. **Cache results**: For expensive operations
   ```python
   cache_file = Path('/tmp/hook-cache.json')
   if cache_file.exists() and cache_file.stat().st_mtime > time.time() - 300:
       # Use cache if less than 5 minutes old
   ```

## Troubleshooting

### Hooks not running
1. Check permissions: `chmod +x .claude/hooks/**/*.{sh,py,js}`
2. Verify paths: Use `$CLAUDE_PROJECT_DIR` for project-relative paths
3. Check settings: Run `/hooks` in Claude Code

### Hooks blocking work
1. Add timeout: `"timeout": 30`
2. Use exit 0 instead of exit 2 for non-critical issues
3. Check `claude --debug` for details

### Performance issues
1. Profile slow hooks: `time ./hook.sh`
2. Move expensive operations to Stop/SessionEnd
3. Use incremental checks (only check changed files)

## Best Practices

1. **Start simple**: Add one hook at a time
2. **Test locally**: Run hooks manually first
3. **Use appropriate events**: 
   - PreToolUse for validation
   - PostToolUse for formatting
   - Stop for final checks
4. **Provide feedback**: Use stderr for Claude, stdout for users
5. **Be non-blocking**: Only block (exit 2) for critical issues
6. **Document your hooks**: Add comments explaining purpose

## Security Notes

- Hooks run with your user permissions
- Always validate inputs from stdin
- Use absolute paths or `$CLAUDE_PROJECT_DIR`
- Never execute untrusted code
- Review hooks before adding to settings

## Contributing

To add a new hook:

1. Create script in appropriate directory:
   - `.claude/hooks/python/` for Python hooks
   - `.claude/hooks/bash/` for shell hooks
   - `.claude/hooks/javascript/` for JS hooks

2. Follow naming convention: `{purpose}-{action}.{ext}`
   Example: `code-formatter.sh`, `test-runner.py`

3. Add shebang and description:
   ```python
   #!/usr/bin/env -S uv run --quiet --script
   # /// script
   # dependencies = ["needed-package"]
   # ///
   """
   Hook Name
   =========
   Type: PostToolUse
   Description: What this hook does
   """
   ```

4. Test thoroughly before adding to settings

## Summary

By combining these hooks strategically, you can create an intelligent development environment that:

- **Anticipates needs** through context awareness
- **Maintains quality** with automated checks
- **Empowers subagents** with relevant information
- **Reduces friction** by automating routine tasks
- **Prevents issues** before they occur

Start with the minimal setup and progressively add hooks as you identify workflow improvements. The goal is to let Claude Code and its subagents handle the mundane while you focus on creative problem-solving.