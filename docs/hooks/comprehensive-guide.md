# Claude Code Hooks: Comprehensive Guide

Claude Code hooks are user-defined shell commands that execute automatically at specific points in Claude Code's lifecycle, providing deterministic control over the AI assistant's behavior. This comprehensive guide covers everything from basic concepts to advanced workflow patterns.

## Table of Contents

1. [Understanding Hooks](#understanding-hooks)
2. [Hook Events & Lifecycle](#hook-events--lifecycle)
3. [Configuration](#configuration)
4. [Basic Implementation](#basic-implementation)
5. [Advanced Patterns](#advanced-patterns)
6. [Workflow Components](#workflow-components)
7. [Security & Performance](#security--performance)
8. [Troubleshooting](#troubleshooting)
9. [Examples & Templates](#examples--templates)

## Understanding Hooks

Unlike relying on prompts that Claude might forget or interpret differently, hooks ensure certain actions always happen—from formatting code after edits to blocking dangerous operations before they execute. Hooks provide:

- **Deterministic Control**: Actions always execute at specific points
- **Security Enforcement**: Block dangerous operations before execution
- **Context Management**: Automatically inject relevant information
- **Quality Assurance**: Enforce standards without manual intervention
- **Workflow Automation**: Chain complex operations seamlessly

## Hook Events & Lifecycle

Claude Code provides eight distinct hook events that fire at critical moments:

### PreToolUse
**When**: After Claude creates tool parameters but before processing the tool call  
**Can Block**: Yes (exit code 2 or JSON with `decision: "block"`)  
**Matchers**: Supports tool-specific patterns (`Edit`, `Write`, `Bash`, `Edit|MultiEdit|Write`)  
**Use Cases**: Security validation, permission control, input sanitization

### PostToolUse
**When**: Immediately after a tool completes successfully  
**Can Block**: Yes (for feedback, not prevention)  
**Matchers**: Same as PreToolUse  
**Use Cases**: Auto-formatting, test running, operation logging

### UserPromptSubmit
**When**: When you submit a prompt, before Claude processes it  
**Output Handling**: stdout becomes part of Claude's context  
**Use Cases**: Context injection, prompt enhancement, security validation

### SessionStart
**When**: New session starts or existing one resumes  
**Output Handling**: stdout becomes part of Claude's context  
**Parameters**: Receives `source` (startup/resume/clear)  
**Use Cases**: Load development context, initialize environment, project setup

### Notification
**When**: Claude needs to notify about status/permissions  
**Can Block**: No  
**Use Cases**: Desktop alerts, mobile notifications, text-to-speech

### Stop & SubagentStop
**When**: Claude or subagents finish responding  
**Can Block**: Yes (forces continuation)  
**Use Cases**: Enforce test passage, automated follow-ups, cleanup

### PreCompact
**When**: Before context compaction for token limits  
**Can Block**: No  
**Use Cases**: Backup transcripts, preserve context, logging

## Configuration

### Configuration Hierarchy

1. `~/.claude/settings.json` - User-wide settings
2. `.claude/settings.json` - Project-specific (version controlled)
3. `.claude/settings.local.json` - Local overrides (not committed)

### Basic Configuration Structure

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|MultiEdit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "python3 .claude/hooks/validate_file_access.py",
            "timeout": 30
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/format_code.sh"
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/enhance_prompt.py"
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/load_context.sh"
          }
        ]
      }
    ]
  }
}
```

### Advanced Matcher Patterns

```json
{
  "matcher": "Edit|MultiEdit|Write",  // Multiple tools
  "matcher": "Bash",                  // Single tool
  "matcher": ".*",                    // All tools (regex)
  "matcher": "Edit.*"                 // Pattern matching
}
```

## Basic Implementation

### Hook Input/Output Protocol

Hooks receive JSON on stdin and can output to stdout/stderr:

**Input JSON Structure**:
```json
{
  "hook_event_name": "PreToolUse",
  "session_id": "unique-id",
  "transcript_path": "/path/to/transcript.json",
  "cwd": "/current/directory",
  "params": {
    "tool": "Edit",
    "file_path": "/path/to/file.py",
    "old_string": "...",
    "new_string": "..."
  }
}
```

**Output for Blocking**:
```json
{
  "decision": "block",
  "message": "Operation blocked: Security violation detected"
}
```

### Simple Hook Examples

**Python Hook Template**:
```python
#!/usr/bin/env python3
import json
import sys

def main():
    # Read input
    input_data = json.loads(sys.stdin.read())
    
    # Process based on event
    event = input_data.get('hook_event_name')
    params = input_data.get('params', {})
    
    # Your logic here
    if should_block(params):
        output = {
            "decision": "block",
            "message": "Operation not allowed"
        }
        print(json.dumps(output))
        sys.exit(2)  # Block operation
    
    # Allow operation
    sys.exit(0)

if __name__ == "__main__":
    main()
```

**Bash Hook Template**:
```bash
#!/bin/bash
INPUT=$(cat)
EVENT=$(echo "$INPUT" | jq -r '.hook_event_name')
TOOL=$(echo "$INPUT" | jq -r '.params.tool // empty')

if [[ "$TOOL" == "Bash" ]]; then
    COMMAND=$(echo "$INPUT" | jq -r '.params.command // empty')
    if [[ "$COMMAND" =~ rm.*-rf ]]; then
        echo '{"decision": "block", "message": "Dangerous rm -rf detected"}'
        exit 2
    fi
fi

exit 0
```

## Advanced Patterns

### Pattern 1: Intelligent Context Management

**Purpose**: Automatically load relevant context based on current work

**Implementation Chain**:
```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/branch-context-loader.sh"
          },
          {
            "type": "command",
            "command": ".claude/hooks/smart-context-injector.py"
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/prompt-enhancer.py"
          }
        ]
      }
    ]
  }
}
```

**Flow**:
1. Session starts → Load branch context (feature/bugfix/release)
2. Smart injector → Load relevant docs, specs, recent changes
3. Prompt submit → Add test coverage, dependencies, related files
4. Claude receives enriched context

### Pattern 2: Automated Quality Pipeline

**Purpose**: Ensure code quality without manual intervention

**Components**:
- Pre-edit validation
- Post-edit formatting
- Incremental testing
- Documentation updates

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/pre-edit-validator.py"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/format-and-test.sh"
          }
        ]
      }
    ]
  }
}
```

### Pattern 3: Security-First Development

**Purpose**: Enforce security policies automatically

```python
# security-validator.py
def validate_operation(params):
    tool = params.get('tool')
    
    # Check file access
    if tool in ['Edit', 'Write', 'Read']:
        file_path = params.get('file_path')
        if not is_allowed_path(file_path):
            return block("Access denied to sensitive file")
    
    # Check for secrets
    if tool in ['Edit', 'Write']:
        content = params.get('new_string', '')
        if contains_secrets(content):
            return block("Detected potential secrets in code")
    
    # Check commands
    if tool == 'Bash':
        command = params.get('command')
        if is_dangerous_command(command):
            return block(f"Dangerous command blocked: {command}")
    
    return allow()
```

### Pattern 4: Test-Driven Enforcement

**Purpose**: Ensure tests exist before implementation

```bash
#!/bin/bash
# tdd-enforcer.sh

INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.params.tool')
FILE=$(echo "$INPUT" | jq -r '.params.file_path // empty')

if [[ "$TOOL" == "Edit" || "$TOOL" == "Write" ]]; then
    # Check if editing implementation file
    if [[ "$FILE" =~ \.(py|js|ts)$ ]] && [[ ! "$FILE" =~ test ]]; then
        # Look for corresponding test file
        TEST_FILE=$(find_test_file "$FILE")
        
        if [[ ! -f "$TEST_FILE" ]]; then
            echo '{"decision": "warn", "message": "No test file found. Consider TDD approach."}'
        fi
    fi
fi
```

## Workflow Components

### Component 1: Branch-Aware Context Loading

```bash
#!/bin/bash
# branch-context-loader.sh

BRANCH=$(git branch --show-current 2>/dev/null)

case "$BRANCH" in
    feature/*)
        echo "Loading feature development context..."
        echo "Related specs: $(find docs -name "*spec*.md")"
        echo "Recent features: $(git log --oneline -5 --grep="feat:")"
        ;;
    bugfix/*)
        echo "Loading bugfix context..."
        echo "Related issues: $(gh issue list --label bug)"
        echo "Recent fixes: $(git log --oneline -5 --grep="fix:")"
        ;;
    release/*)
        echo "Loading release context..."
        echo "Changelog: $(cat CHANGELOG.md | head -20)"
        echo "Version: $(cat package.json | jq -r .version)"
        ;;
esac
```

### Component 2: Smart Dependency Analysis

```python
# dependency-analyzer.py
import ast
import json
import sys

def analyze_file_edit(file_path, old_code, new_code):
    """Analyze impact of code changes"""
    
    # Parse AST
    old_tree = ast.parse(old_code)
    new_tree = ast.parse(new_code)
    
    # Find changed functions/classes
    changed_items = find_changes(old_tree, new_tree)
    
    # Find dependents
    dependents = find_dependents(file_path, changed_items)
    
    if dependents:
        print(f"⚠️  This change affects {len(dependents)} files:")
        for dep in dependents[:5]:
            print(f"  - {dep}")
        
        # Suggest running tests
        test_files = [f for f in dependents if 'test' in f]
        if test_files:
            print(f"\n📝 Suggested tests to run:")
            for test in test_files:
                print(f"  pytest {test}")
```

### Component 3: Incremental Test Runner

```bash
#!/bin/bash
# smart-test-runner.sh

INPUT=$(cat)
FILE=$(echo "$INPUT" | jq -r '.params.file_path // empty')

if [[ -n "$FILE" ]]; then
    # Find affected test files
    TESTS=$(find_affected_tests "$FILE")
    
    if [[ -n "$TESTS" ]]; then
        echo "Running affected tests..."
        
        # Run tests based on file type
        if [[ "$FILE" =~ \.py$ ]]; then
            pytest $TESTS --tb=short
        elif [[ "$FILE" =~ \.(js|ts)$ ]]; then
            npm test -- $TESTS
        fi
        
        # Check coverage
        COVERAGE=$(check_coverage "$FILE")
        if [[ $COVERAGE -lt 80 ]]; then
            echo "⚠️  Coverage below 80% for $FILE"
        fi
    fi
fi
```

### Component 4: Auto-Documentation

```python
# doc-generator.py
def generate_docs_for_changes(params):
    """Auto-generate documentation for code changes"""
    
    tool = params.get('tool')
    if tool not in ['Edit', 'Write']:
        return
    
    file_path = params.get('file_path')
    new_content = params.get('new_string', '')
    
    # Parse code
    if file_path.endswith('.py'):
        docs = extract_python_docs(new_content)
    elif file_path.endswith(('.js', '.ts')):
        docs = extract_js_docs(new_content)
    else:
        return
    
    # Update documentation
    if docs:
        doc_file = f"docs/{os.path.basename(file_path)}.md"
        update_documentation(doc_file, docs)
        print(f"📚 Updated documentation: {doc_file}")
```

## Security & Performance

### Security Best Practices

1. **Path Validation**:
```python
ALLOWED_PATHS = ['/project', '/tmp']
BLOCKED_PATHS = ['/etc', '/usr', '~/.ssh']

def is_safe_path(path):
    abs_path = os.path.abspath(path)
    return any(abs_path.startswith(p) for p in ALLOWED_PATHS) and \
           not any(abs_path.startswith(p) for p in BLOCKED_PATHS)
```

2. **Secret Detection**:
```python
import re

SECRET_PATTERNS = [
    r'api[_-]?key\s*=\s*["\'][\w\-]+["\']',
    r'password\s*=\s*["\'].*["\']',
    r'token\s*=\s*["\'][\w\-]+["\']',
    r'-----BEGIN (RSA |DSA |EC |PGP )?PRIVATE KEY'
]

def contains_secrets(content):
    for pattern in SECRET_PATTERNS:
        if re.search(pattern, content, re.IGNORECASE):
            return True
    return False
```

3. **Command Validation**:
```bash
DANGEROUS_COMMANDS=(
    "rm -rf /"
    "dd if=/dev/zero"
    ":(){ :|:& };:"  # Fork bomb
    "chmod -R 777"
    "curl | bash"
)

for cmd in "${DANGEROUS_COMMANDS[@]}"; do
    if [[ "$COMMAND" == *"$cmd"* ]]; then
        exit 2  # Block
    fi
done
```

### Performance Optimization

1. **Timeout Configuration**:
```json
{
  "hooks": [{
    "type": "command",
    "command": "./hook.sh",
    "timeout": 30  // 30 seconds max
  }]
}
```

2. **Caching Strategy**:
```python
import functools
import time

@functools.lru_cache(maxsize=128)
def expensive_analysis(file_path):
    # Cache results for repeated calls
    return analyze_dependencies(file_path)

# Time-based cache
CACHE = {}
CACHE_TTL = 300  # 5 minutes

def get_cached_or_compute(key, compute_func):
    if key in CACHE:
        value, timestamp = CACHE[key]
        if time.time() - timestamp < CACHE_TTL:
            return value
    
    value = compute_func()
    CACHE[key] = (value, time.time())
    return value
```

3. **Parallel Processing**:
```bash
# Run multiple checks in parallel
{
    check_syntax "$FILE" &
    check_formatting "$FILE" &
    check_security "$FILE" &
    wait
} 2>/dev/null
```

## Troubleshooting

### Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| Hook not executing | Permission issue | `chmod +x hook_script.sh` |
| Hook timing out | Long operation | Increase timeout or optimize code |
| JSON parse errors | Malformed output | Validate with `jq` before outputting |
| Context not injecting | Wrong exit code | Ensure exit 0 for success |
| Blocking not working | Wrong format | Return JSON with `decision: "block"` |
| Path not found | Relative paths | Use absolute paths or `$CLAUDE_PROJECT_DIR` |

### Debugging Hooks

**Enable verbose logging**:
```bash
#!/bin/bash
set -x  # Enable debug output
exec 2>/tmp/hook_debug.log  # Redirect stderr to log

INPUT=$(cat)
echo "Received: $INPUT" >&2
# ... rest of hook
```

**Test hooks manually**:
```bash
# Test with mock input
echo '{"hook_event_name": "PreToolUse", "params": {"tool": "Edit", "file_path": "test.py"}}' | ./hook.sh
echo "Exit code: $?"
```

**Monitor hook execution**:
```bash
# Watch hook logs
tail -f /tmp/hook_debug.log

# Check Claude Code logs
tail -f ~/.claude/logs/session.log
```

## Examples & Templates

### Complete Security Pipeline

```json
{
  "hooks": {
    "SessionStart": [{
      "hooks": [{
        "type": "command",
        "command": ".claude/hooks/security/load-policies.sh"
      }]
    }],
    "PreToolUse": [{
      "matcher": ".*",
      "hooks": [{
        "type": "command",
        "command": ".claude/hooks/security/validate-operation.py"
      }]
    }],
    "PostToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{
        "type": "command",
        "command": ".claude/hooks/security/scan-changes.sh"
      }]
    }]
  }
}
```

### TDD Workflow

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{
        "type": "command",
        "command": ".claude/hooks/tdd/ensure-tests-exist.py"
      }]
    }],
    "PostToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{
        "type": "command",
        "command": ".claude/hooks/tdd/run-affected-tests.sh"
      }]
    }],
    "Stop": [{
      "hooks": [{
        "type": "command",
        "command": ".claude/hooks/tdd/verify-all-tests-pass.sh"
      }]
    }]
  }
}
```

### Performance Monitoring

```python
#!/usr/bin/env python3
# performance-monitor.py
import json
import sys
import time
import psutil

def monitor_performance():
    input_data = json.loads(sys.stdin.read())
    
    # Track metrics
    metrics = {
        'timestamp': time.time(),
        'event': input_data['hook_event_name'],
        'memory': psutil.Process().memory_info().rss / 1024 / 1024,  # MB
        'cpu': psutil.cpu_percent(interval=0.1)
    }
    
    # Log to file
    with open('.claude/metrics.jsonl', 'a') as f:
        f.write(json.dumps(metrics) + '\n')
    
    # Alert if high usage
    if metrics['memory'] > 1000:  # 1GB
        print("⚠️  High memory usage detected")
    
    if metrics['cpu'] > 80:
        print("⚠️  High CPU usage detected")

if __name__ == "__main__":
    monitor_performance()
```

## Best Practices

1. **Keep hooks fast** - Under 500ms for responsive experience
2. **Handle errors gracefully** - Don't crash on unexpected input
3. **Log for debugging** - But don't spam stdout unless needed
4. **Use caching** - For expensive operations
5. **Document side effects** - Make it clear what hooks do
6. **Version control settings** - But use `.local.json` for personal preferences
7. **Test hooks thoroughly** - They run in production constantly
8. **Use appropriate languages** - Python for complex logic, Bash for simple operations
9. **Respect user intent** - Block dangerous operations but don't be overly restrictive
10. **Provide helpful messages** - When blocking, explain why and suggest alternatives

## Conclusion

Claude Code hooks transform the development experience from reactive assistance to proactive automation. By combining hooks strategically, you create an intelligent development environment that:

- Maintains code quality automatically
- Enforces security policies consistently
- Provides rich context for better AI assistance
- Reduces manual repetitive tasks
- Enables complex workflows with simple triggers

Start with basic hooks for formatting and validation, then gradually build more sophisticated workflows as your needs evolve. The hook system's flexibility means you can adapt it to any development methodology or team requirements.