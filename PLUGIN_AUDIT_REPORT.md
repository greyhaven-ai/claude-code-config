# Grey Haven Plugin Audit Report

**Generated:** 2026-01-08
**Claude Code Version Target:** v2.1.0
**Plugins Audited:** 16
**Overall Health Score:** 72/100

---

## Executive Summary

| Metric | Count | Status |
|--------|-------|--------|
| Total Plugins | 16 | ✅ |
| Total Agents | 48 | ✅ |
| Total Commands | 56 | ✅ |
| Total Skills | 43 | ✅ |
| Deprecations Found | 34 | ⚠️ |
| High Priority Issues | 10 | 🔴 |
| Medium Priority Issues | 44 | 🟡 |
| Low Priority Issues | 7 | 🟢 |

---

## Critical Issues (High Priority)

### 1. Agents Missing `tools:` Field (10 agents)

These agents have no tool restrictions, allowing unrestricted access to all tools:

| Agent | Plugin | Risk |
|-------|--------|------|
| `ci-cd-analyzer.md` | cloudflare-deployment-observability | HIGH |
| `deployment-monitor.md` | cloudflare-deployment-observability | HIGH |
| `performance-tracker.md` | cloudflare-deployment-observability | HIGH |
| `documentation-alignment-verifier.md` | core | MEDIUM |
| `git-diff-documentation-agent.md` | core | MEDIUM |
| `multi-agent-synthesis-orchestrator.md` | research | MEDIUM |
| `tech-docs-maintainer.md` | research | MEDIUM |
| `tech-docs-orchestrator.md` | research | MEDIUM |
| `web-docs-researcher.md` | research | MEDIUM |
| `bug-issue-creator.md` | testing | MEDIUM |

**Impact:** Without `tools:` restrictions, these agents can access all tools including potentially dangerous ones like `Bash` without constraints.

**Fix:** Add explicit `tools:` frontmatter with YAML list format:
```yaml
tools:
  - Read
  - Write
  - Grep
  - Glob
```

### 2. `core` Plugin Missing Agents Array in plugin.json

The `core` plugin has 9 agents but doesn't declare them in `plugin.json`:

- `code-quality-analyzer.md`
- `documentation-alignment-verifier.md`
- `git-diff-documentation-agent.md`
- `performance-optimizer.md`
- `project-scaffolder.md`
- `prompt-engineer.md`
- `tdd-orchestrator.md`
- `tdd-python.md`
- `tdd-typescript.md`

**Fix:** Add agents array to `grey-haven-plugins/core/.claude-plugin/plugin.json`:
```json
"agents": [
    "./agents/code-quality-analyzer.md",
    "./agents/documentation-alignment-verifier.md",
    "./agents/git-diff-documentation-agent.md",
    "./agents/performance-optimizer.md",
    "./agents/project-scaffolder.md",
    "./agents/prompt-engineer.md",
    "./agents/tdd-orchestrator.md",
    "./agents/tdd-python.md",
    "./agents/tdd-typescript.md"
]
```

### 3. `deployment` and `linear` Plugins Missing Agents Array

While these plugins may not have agents directories, the `plugin.json` should either:
- Declare an empty `"agents": []` array
- Or add agents if they exist but aren't declared

---

## Deprecated Patterns (Medium Priority)

### 1. Comma-Separated Tool Lists (34 agents)

**Status:** DEPRECATED - Use YAML lists instead

The following agents use comma-separated tool lists instead of YAML-style arrays:

| Plugin | Agent |
|--------|-------|
| agent-orchestration | context-manager.md |
| cc-trace | cc-trace.md |
| core | code-quality-analyzer.md |
| core | performance-optimizer.md |
| core | project-scaffolder.md |
| core | tdd-orchestrator.md |
| core | tdd-python.md |
| core | tdd-typescript.md |
| creative-writing | character-developer.md |
| creative-writing | content-strategist.md |
| creative-writing | dialogue-coach.md |
| creative-writing | editor-reviewer.md |
| creative-writing | outline-architect.md |
| creative-writing | research-gatherer.md |
| creative-writing | story-architect.md |
| creative-writing | world-builder.md |
| data-quality | data-validator.md |
| developer-experience | onboarding-coordinator.md |
| incident-response | incident-responder.md |
| incident-response | smart-debug.md |
| knowledge-base | kb-entry-creator.md |
| knowledge-base | kb-manifest-generator.md |
| knowledge-base | kb-ontology-mapper.md |
| knowledge-base | kb-search-analyzer.md |
| knowledge-base | kb-validator.md |
| knowledge-base | knowledge-curator.md |
| knowledge-base | memory-architect.md |
| knowledge-base | ontology-builder.md |
| observability | devops-troubleshooter.md |
| observability | memory-profiler.md |
| observability | observability-engineer.md |
| security | security-analyzer.md |
| testing | react-tanstack-tester.md |
| testing | test-generator.md |

**Current (deprecated):**
```yaml
tools: Read, Write, Bash, Grep
```

**Recommended (v2.1.0+):**
```yaml
tools:
  - Read
  - Write
  - Bash
  - Grep
```

### 2. Lowercase Tool Names (1 agent)

**Agent:** `core/agents/prompt-engineer.md`
**Issue:** `tools: read, write` should use proper casing: `Read, Write`

---

## Commands Missing `allowed-tools` (Low Priority)

20+ commands are missing the `allowed-tools` frontmatter. While not strictly required, it's a best practice for:
- Security: Restricting tool access
- Performance: Reducing token overhead from unnecessary tool descriptions

**Commands missing `allowed-tools`:**

| Plugin | Command |
|--------|---------|
| agent-orchestration | context-restore.md, context-save.md, workflow-composer.md |
| cc-trace | cc-trace-connect.md, cc-trace-setup.md, cc-trace-start.md |
| cloudflare-deployment-observability | deployment-status.md, logs-analyze.md, metrics-dashboard.md |
| data-quality | data-validation-workflow.md, validation-workflow-checklist.md |
| developer-experience | api-documentation-checklist.md, async-standup.md, doc-coverage.md, doc-generate-api.md |
| incident-response | smart-fix.md |
| observability | monitor-setup.md, monitoring-setup-checklist.md, slo-implement.md, slo-implementation-checklist.md |

---

## Feature Adoption Opportunities

### 1. Agent-Scoped Hooks (v2.1.0+)

Only **9 of 48 agents** (19%) have hooks configured. Consider adding hooks for:

| Use Case | Hook Type | Example |
|----------|-----------|---------|
| Quality gates | `Stop` | Validate code before completion |
| Security checks | `PreToolUse` | Validate dangerous operations |
| Logging/metrics | `PostToolUse` | Track agent actions |

**Agents with hooks (already implemented):**
- `tdd-python.md` ✅
- `tdd-typescript.md` ✅
- `tdd-orchestrator.md` ✅
- `deployment-monitor.md` ✅
- `data-validator.md` ✅
- `incident-responder.md` ✅
- `believability-auditor.md` ✅

**Priority agents to add hooks:**
- `security-analyzer.md` - Security validation on Stop
- `code-quality-analyzer.md` - Quality gate on Stop
- `test-generator.md` - Test validation on Stop

### 2. `disallowedTools` Field (v2.1.0+)

Only **11 of 48 agents** (23%) use `disallowedTools`. Consider adding to restrict dangerous tools:

```yaml
disallowedTools:
  - Bash(rm *)
  - Bash(sudo *)
  - Task(security-analyzer)  # Prevent recursion
```

### 3. `context: fork` for Commands (v2.1.0+)

New feature allowing commands to run in forked sub-agent context. Consider for:
- Long-running analysis commands
- Commands that spawn multiple agents
- Commands requiring isolated context

```yaml
---
name: my-command
context: fork
allowed-tools:
  - Read
  - Write
---
```

### 4. Skills Already Well-Configured

**Good news:** All 43 skills have both:
- ✅ `skills:` for auto-loading (v2.0.43+)
- ✅ `allowed-tools:` for tool restrictions (v2.0.74+)

---

## Plugin-by-Plugin Analysis

### core (Score: 65/100)

| Aspect | Status | Notes |
|--------|--------|-------|
| plugin.json | ⚠️ | Missing agents array |
| Agents | ⚠️ | 9 agents, 8 use comma-separated tools |
| Skills | ✅ | 12 well-configured skills |
| Commands | ✅ | All have allowed-tools |
| Hooks | ⚠️ | Only 3/9 agents have hooks |

**Action Items:**
1. Add agents array to plugin.json
2. Convert tools to YAML lists
3. Add hooks to code-quality-analyzer, performance-optimizer

### creative-writing (Score: 75/100)

| Aspect | Status | Notes |
|--------|--------|-------|
| plugin.json | ✅ | Complete |
| Agents | ⚠️ | 9 agents, all use comma-separated tools |
| Skills | ✅ | 1 skill, well-configured |
| Hooks | ✅ | believability-auditor has hooks |

**Action Items:**
1. Convert all 9 agents to YAML tool lists

### knowledge-base (Score: 70/100)

| Aspect | Status | Notes |
|--------|--------|-------|
| plugin.json | ✅ | Complete |
| Agents | ⚠️ | 8 agents, all use comma-separated tools |
| Skills | ✅ | 1 skill, well-configured |
| disallowedTools | ✅ | All agents have empty disallowedTools |

**Action Items:**
1. Convert all 8 agents to YAML tool lists
2. Consider adding actual disallowed tools restrictions

### cloudflare-deployment-observability (Score: 55/100)

| Aspect | Status | Notes |
|--------|--------|-------|
| plugin.json | ✅ | Complete |
| Agents | 🔴 | 3 agents missing tools field entirely |
| Commands | ⚠️ | 3 commands missing allowed-tools |
| Hooks | ✅ | deployment-monitor has hooks |

**Action Items:**
1. Add tools field to all 3 agents (CRITICAL)
2. Add allowed-tools to commands

### testing (Score: 70/100)

| Aspect | Status | Notes |
|--------|--------|-------|
| plugin.json | ✅ | Complete |
| Agents | ⚠️ | 2/3 use comma-separated, 1 missing tools |
| Skills | ✅ | 3 well-configured skills |

**Action Items:**
1. Add tools to bug-issue-creator.md
2. Convert to YAML tool lists

### research (Score: 60/100)

| Aspect | Status | Notes |
|--------|--------|-------|
| plugin.json | ✅ | Complete |
| Agents | 🔴 | 4 agents all missing tools field |
| Skills | ✅ | 1 well-configured skill |

**Action Items:**
1. Add tools field to all 4 agents (CRITICAL)

---

## Recommended Priority Actions

### Immediate (This Week)

1. **Add tools field to 10 agents missing it** - Security risk
   ```bash
   # Run this to find them
   for f in grey-haven-plugins/*/agents/*.md; do
     grep -q "^tools:" "$f" || echo "$f"
   done
   ```

2. **Add agents array to core plugin.json** - Plugin discovery

3. **Fix lowercase tools in prompt-engineer.md**

### Short-Term (This Month)

4. **Convert 34 agents from comma-separated to YAML tool lists**
   - While not broken, this is the modern standard

5. **Add allowed-tools to 20+ commands**
   - Security best practice

### Long-Term (Next Quarter)

6. **Add hooks to security-critical agents**
   - security-analyzer
   - code-quality-analyzer
   - tdd-* agents

7. **Review disallowedTools configuration**
   - Currently 11 agents have it but most are empty
   - Consider blocking dangerous patterns

---

## Changelog Compatibility Matrix

| Feature | Introduced | Plugins Using | Plugins Should Use |
|---------|------------|---------------|-------------------|
| YAML tool lists | v2.0.0 | 14 agents | 48 agents |
| `skills:` auto-load | v2.0.43 | 43 skills | 43 skills ✅ |
| `allowed-tools:` skills | v2.0.74 | 43 skills | 43 skills ✅ |
| Agent hooks | v2.1.0 | 9 agents | 15+ agents |
| `disallowedTools` | v2.1.0 | 11 agents | 20+ agents |
| `context: fork` | v2.1.0 | 0 commands | Consider for complex commands |

---

## Conclusion

The Grey Haven plugin ecosystem is **generally well-structured** with good skill configuration. The main areas for improvement are:

1. **Critical:** 10 agents missing tool restrictions
2. **Deprecation:** 34 agents using comma-separated tool lists
3. **Enhancement:** Low hook and disallowedTools adoption

Addressing the critical issues first will improve security posture. Converting to YAML tool lists is a modernization that should be done but isn't urgent.

---

*Report generated by plugin-auditor skill*
