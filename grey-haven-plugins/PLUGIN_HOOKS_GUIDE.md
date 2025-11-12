# Plugin Hooks Implementation Guide

This guide provides templates and recommendations for adding intelligent prompt-based hooks to Grey Haven plugins.

## Overview

Plugins can provide hooks that automatically merge with user hooks when enabled. Plugin hooks use:
- `${CLAUDE_PLUGIN_ROOT}` to reference plugin files
- Both `command` (bash scripts) and `prompt` (LLM-based) hook types
- Standard hook events: PreToolUse, PostToolUse, Stop, SubagentStop, UserPromptSubmit, SessionStart, Notification

## Plugin Hook Structure

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json
├── hooks/
│   ├── hooks.json          # Hook configurations
│   └── scripts/            # Optional bash scripts
│       ├── format.sh
│       └── validate.sh
├── agents/
├── commands/
└── skills/
```

## Template: hooks/hooks.json

```json
{
  "description": "Brief description of what these hooks do",
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit|MultiEdit",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Your validation prompt here. Context: $ARGUMENTS",
            "timeout": 30
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/scripts/format.sh",
            "timeout": 30
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Evaluate if work is complete: $ARGUMENTS",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

## Hook Recommendations by Plugin

### 🔴 HIGH PRIORITY (Quality & Safety Critical)

#### 1. core - TDD & Quality Enforcement

**Priority**: Critical
**Hook Events**: Stop, SubagentStop, PostToolUse
**Purpose**: Enforce TDD discipline and quality standards

```json
{
  "description": "TDD enforcement and code quality validation",
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "You are a TDD discipline enforcer reviewing: $ARGUMENTS\n\nEvaluate if:\n1. Tests were written BEFORE implementation (true TDD)\n2. All tests are passing (no failures or skips)\n3. Code coverage meets project thresholds (≥80%)\n4. No obvious code quality issues (complexity, duplication)\n5. Documentation is updated for API changes\n\nBe strict. If ANY criterion fails, block with specific feedback.\n\nReturn: {\"decision\": \"approve\" or \"block\", \"reason\": \"detailed explanation with line numbers if blocking\"}",
            "timeout": 30
          }
        ]
      }
    ],
    "SubagentStop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Review subagent TDD compliance: $ARGUMENTS\n\nVerify:\n- Subagent wrote tests first\n- All tests pass\n- Code is clean and maintainable\n- No technical debt introduced\n\nReturn: {\"decision\": \"approve\" or \"block\", \"reason\": \"specific feedback\"}",
            "timeout": 30
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit|MultiEdit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/scripts/format-and-lint.sh",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

**Bash script**: `hooks/scripts/format-and-lint.sh`
```bash
#!/bin/bash
# Auto-format code after edits
for file in $CLAUDE_FILE_PATHS; do
    case "$file" in
        *.py) black "$file" && ruff check --fix "$file" ;;
        *.js|*.jsx|*.ts|*.tsx) prettier --write "$file" && eslint --fix "$file" ;;
    esac
done
```

---

#### 2. security - Security Validation

**Priority**: Critical
**Hook Events**: PreToolUse, Stop
**Purpose**: Prevent security vulnerabilities before code is written

```json
{
  "description": "Security validation for all code changes",
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit|MultiEdit",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "SECURITY REVIEW: $ARGUMENTS\n\nScan for vulnerabilities:\n1. SQL Injection (parameterized queries?)\n2. XSS (proper escaping?)\n3. Hardcoded secrets (passwords, API keys, tokens)\n4. Path traversal (input sanitization?)\n5. Authentication bypass (proper checks?)\n6. Insecure dependencies (known CVEs?)\n7. CSRF protection (tokens present?)\n8. Insecure deserialization\n9. Command injection\n10. Insufficient logging/monitoring\n\nBLOCK if ANY security issue found. Be thorough.\n\nReturn: {\"decision\": \"approve\" or \"block\", \"reason\": \"detailed security findings with CWE numbers\"}",
            "timeout": 30
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Final security audit: $ARGUMENTS\n\nConfirm:\n- No security vulnerabilities introduced\n- Security tests added for changes\n- Secure by default principles followed\n- No exposure of sensitive data\n\nReturn: {\"decision\": \"approve\" or \"block\", \"reason\": \"security summary\"}",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

---

#### 3. testing - Test Quality Enforcement

**Priority**: Critical
**Hook Events**: SubagentStop, PostToolUse
**Purpose**: Ensure comprehensive, high-quality tests

```json
{
  "description": "Test quality and coverage enforcement",
  "hooks": {
    "SubagentStop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Evaluate test quality: $ARGUMENTS\n\nCheck:\n1. All edge cases covered (happy path, errors, boundaries)\n2. Test names are descriptive (test_should_xxx_when_yyy)\n3. Assertions are meaningful (not just assert True)\n4. No flaky tests (no random/timing dependencies)\n5. Tests are fast (<1s each for unit tests)\n6. No skipped/ignored tests without good reason\n7. Mocks are appropriate (not over-mocked)\n8. Integration tests for API contracts\n\nBe strict on test quality.\n\nReturn: {\"decision\": \"approve\" or \"block\", \"reason\": \"test quality feedback\"}",
            "timeout": 30
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/scripts/run-tests.sh",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

**Bash script**: `hooks/scripts/run-tests.sh`
```bash
#!/bin/bash
# Run tests after code changes
for file in $CLAUDE_FILE_PATHS; do
    if [[ "$file" =~ \\.py$ ]]; then
        pytest "$file" -v || exit 2
    elif [[ "$file" =~ \\.(ts|tsx|js|jsx)$ ]]; then
        npm test -- --findRelatedTests "$file" || exit 2
    fi
done
```

---

#### 4. incident-response - Fix Quality Validation

**Priority**: Critical
**Hook Events**: Stop, PreToolUse
**Purpose**: Ensure incident fixes are proper, not quick hacks

```json
{
  "description": "Incident fix quality validation",
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Validate incident fix quality: $ARGUMENTS\n\nVerify:\n1. ROOT CAUSE addressed (not just symptoms)\n2. No quick hacks or workarounds\n3. Tests prevent regression\n4. Monitoring/alerts added to detect recurrence\n5. Runbook created or updated\n6. Postmortem action items completed\n7. Documentation updated\n8. Code is production-ready (not temporary fix)\n\nBlock if fix is inadequate or risky.\n\nReturn: {\"decision\": \"approve\" or \"block\", \"reason\": \"fix quality assessment with recommendations\"}",
            "timeout": 30
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Validate incident fix approach: $ARGUMENTS\n\nCheck:\n- Fix is surgical and targeted\n- No unrelated changes\n- Rollback plan exists\n- Low risk of new issues\n\nReturn: {\"decision\": \"approve\" or \"block\", \"reason\": \"risk assessment\"}",
            "timeout": 20
          }
        ]
      }
    ]
  }
}
```

---

#### 5. data-quality - Data Validation

**Priority**: Critical
**Hook Events**: PreToolUse, Stop
**Purpose**: Prevent data corruption and validation errors

```json
{
  "description": "Data validation and schema enforcement",
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Data validation review: $ARGUMENTS\n\nValidate:\n1. Pydantic models have proper validators\n2. All fields have type hints\n3. Database constraints match model validators\n4. Migrations handle existing data\n5. No data loss in transformations\n6. Proper null/optional handling\n7. Foreign key relationships valid\n8. Index optimization for queries\n\nReturn: {\"decision\": \"approve\" or \"block\", \"reason\": \"data validation findings\"}",
            "timeout": 30
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Final data quality check: $ARGUMENTS\n\nConfirm:\n- All data changes are reversible\n- Validation is comprehensive\n- No data corruption risks\n- Tests cover data edge cases\n\nReturn: {\"decision\": \"approve\" or \"block\", \"reason\": \"data quality summary\"}",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

---

### 🟡 MEDIUM PRIORITY (Operations & Workflow)

#### 6. observability - Performance Monitoring

**Priority**: High
**Hook Events**: Stop, PostToolUse
**Purpose**: Detect performance regressions early

```json
{
  "description": "Performance regression detection",
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Performance analysis: $ARGUMENTS\n\nCheck for:\n1. N+1 query problems\n2. Inefficient algorithms (O(n²) or worse)\n3. Missing database indices\n4. Synchronous calls that should be async\n5. Memory leaks (unclosed connections/files)\n6. Excessive API calls\n7. Large payload sizes\n8. Missing caching opportunities\n\nWarn if performance concerns exist.\n\nReturn: {\"decision\": \"approve\" or \"block\", \"reason\": \"performance analysis\"}",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

---

#### 7. deployment - Deployment Validation

**Priority**: High
**Hook Events**: PreToolUse, Stop
**Purpose**: Prevent bad deployments

```json
{
  "description": "Deployment safety checks",
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Deployment safety check: $ARGUMENTS\n\nValidate:\n- Deployment command is safe\n- Environment is correct (not accidentally prod)\n- Rollback plan exists\n- Breaking changes handled\n- Database migrations tested\n\nReturn: {\"decision\": \"approve\" or \"block\", \"reason\": \"deployment risk assessment\"}",
            "timeout": 20
          }
        ]
      }
    ]
  }
}
```

---

#### 8. cloudflare-deployment-observability - CI/CD Monitoring

**Priority**: Medium
**Hook Events**: UserPromptSubmit, Stop
**Purpose**: Monitor deployment health

```json
{
  "description": "CI/CD pipeline monitoring",
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/scripts/check-pipeline-status.sh",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

---

### 🟢 LOW PRIORITY (Support & Utilities)

#### 9. developer-experience - Documentation Validation

**Priority**: Medium
**Hook Events**: Stop
**Purpose**: Ensure documentation stays current

```json
{
  "description": "Documentation currency checks",
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Documentation validation: $ARGUMENTS\n\nCheck if documentation needs updates for:\n- API changes\n- New features\n- Configuration changes\n- Breaking changes\n\nReturn: {\"decision\": \"approve\" or \"block\", \"reason\": \"documentation status\"}",
            "timeout": 20
          }
        ]
      }
    ]
  }
}
```

---

## Implementation Priority

### Phase 1: Critical Quality & Security (Week 1)
1. ✅ **security** - Security validation (highest risk)
2. ✅ **core** - TDD enforcement (core workflow)
3. ✅ **testing** - Test quality (quality foundation)

### Phase 2: Operations & Incidents (Week 2)
4. ✅ **incident-response** - Fix quality validation
5. ✅ **data-quality** - Data validation
6. ✅ **observability** - Performance monitoring

### Phase 3: Deployment & Workflow (Week 3)
7. ✅ **deployment** - Deployment safety
8. ✅ **cloudflare-deployment-observability** - CI/CD monitoring

### Phase 4: Support & Enhancement (Week 4)
9. ✅ **developer-experience** - Documentation
10. ✅ **browser-automation** - Safe browsing
11. ✅ **linear** - Work tracking

## Best Practices

### Prompt Design
1. **Be specific**: Clearly state what to evaluate
2. **List criteria**: Enumerate all checks
3. **Be strict**: Block on ANY failure for critical hooks
4. **Provide context**: Include line numbers, examples in feedback
5. **Use structured output**: Always return JSON with decision + reason

### Hook Performance
1. **Set appropriate timeouts**: 20-30s for prompts, 60s max for bash
2. **Run in parallel**: Multiple hooks can run simultaneously
3. **Fail fast**: Block early in PreToolUse rather than late in Stop
4. **Cache results**: Don't re-validate unchanged code

### Testing Hooks
1. **Test with real scenarios**: Use actual code changes
2. **Verify blocking works**: Confirm hooks actually prevent bad changes
3. **Check feedback quality**: Ensure Claude gets actionable feedback
4. **Monitor performance**: Track hook execution times

### Maintenance
1. **Update prompts regularly**: Refine based on false positives/negatives
2. **Version control**: Track hook changes in git
3. **Document decisions**: Explain why hooks block/approve
4. **Monitor effectiveness**: Track how often hooks catch issues

## Environment Variables

Available in all plugin hooks:
- `${CLAUDE_PLUGIN_ROOT}` - Absolute path to plugin directory
- `${CLAUDE_PROJECT_DIR}` - Project root directory
- `$CLAUDE_FILE_PATHS` - Files being edited (PostToolUse)
- `$CLAUDE_TOOL_NAME` - Tool being used
- `$ARGUMENTS` - Hook input JSON (in prompts)

## Troubleshooting

### Hook not executing
- Check `hooks/hooks.json` exists in plugin directory
- Verify JSON syntax with `jq`
- Confirm plugin is enabled in `.claude/settings.json`
- Check Claude Code logs for errors

### Prompt hook returning wrong decision
- Refine prompt to be more specific
- Add more evaluation criteria
- Include examples in prompt
- Increase timeout if LLM is timing out

### Bash hook failing
- Make scripts executable: `chmod +x hooks/scripts/*.sh`
- Use absolute paths with `${CLAUDE_PLUGIN_ROOT}`
- Test scripts manually
- Check stderr output for errors

## Example: Complete Plugin with Hooks

See `grey-haven-plugins/core/` for a complete example implementing all recommended hooks.

## Resources

- [Claude Code Hooks Documentation](https://docs.claude.com/en/docs/claude-code/hooks)
- [Plugin Components Reference](https://docs.claude.com/en/docs/claude-code/plugins)
- Grey Haven Plugin Library: `/grey-haven-plugins/hooks/` (reference implementations)
