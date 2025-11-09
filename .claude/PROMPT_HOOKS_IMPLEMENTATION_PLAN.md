# Prompt-Based Hooks Implementation Plan

## Executive Summary

This document outlines opportunities to implement prompt-based hooks to enhance the Grey Haven plugins ecosystem (12 plugins, 31 agents, 20 skills). Prompt-based hooks provide deterministic context injection and validation at key points in the Claude Code lifecycle.

## What Are Prompt-Based Hooks?

Prompt-based hooks are automated commands that run at specific lifecycle events and can inject context or validate inputs. Unlike relying on Claude to remember context, hooks ensure consistent behavior.

### Key Hook Types for Context Enhancement

1. **UserPromptSubmit** - Runs when user submits prompt, before processing
   - Can inject `additionalContext` based on prompt analysis
   - Can validate/block prompts
   - Exit code 0 with stdout automatically adds context

2. **SessionStart** - Runs when session starts/resumes
   - Can load project context at session start
   - Matchers: `startup`, `resume`, `clear`

3. **PreToolUse** - Runs before tool execution
   - Can prepare context for specific tools
   - Especially useful for `Task` tool (subagents)

## Current Hook Implementation Status

### ✅ Existing Hooks

1. **prompt-enhancer.py** (UserPromptSubmit)
   - Intent detection (testing, debugging, feature, refactor, etc.)
   - File reference extraction
   - Test coverage context
   - Recent git changes
   - Dependency context
   - API/database context
   - Branch context

2. **subagent-context-preparer.py** (PreToolUse, Task matcher)
   - Prepares context for 8 specific subagents
   - Writes context files to `.claude/context/`
   - Supports: TDD, security, analysis, git, docs, refactor, research, issue creation

3. **security-validator.py** (PreToolUse)
   - Security validation for tool calls

4. **work-completion-assistant.py** (Stop/SubagentStop)
   - Work tracking and completion

## Recommended Implementations

### Phase 1: Agent-Specific Context Enhancement (High Priority)

#### 1. TDD Workflow Enhancement
**Target Agents**: `tdd-orchestrator`, `tdd-python`, `tdd-typescript`
**Hook Type**: UserPromptSubmit
**Implementation**: `.claude/hooks/tdd-context-enhancer.py`

**Purpose**: Automatically inject test framework, coverage, and TDD best practices when TDD work is detected

**Context to Add**:
- Active test framework (pytest, jest, mocha)
- Current test coverage percentage
- Failed tests from last run
- TDD cycle reminders (Red-Green-Refactor)
- Testing strategy skill reference

**Trigger Keywords**: "test", "tdd", "spec", "coverage", "unit test"

```python
def enhance_tdd_context(prompt: str) -> Optional[str]:
    """Add TDD-specific context"""
    if not detect_tdd_intent(prompt):
        return None

    context = []
    context.append("=== TDD Context ===")
    context.append(f"Test Framework: {detect_framework()}")
    context.append(f"Coverage: {get_coverage_summary()}")
    context.append(f"Failed Tests: {get_failed_tests()}")
    context.append("TDD Cycle: Red (write failing test) → Green (make it pass) → Refactor")

    # Reference testing-strategy skill
    if has_skill("testing-strategy"):
        context.append("📚 Skill: testing-strategy available in plugins/core/skills/")

    return "\n".join(context)
```

---

#### 2. Security Analysis Enhancement
**Target Agents**: `security-analyzer`
**Hook Type**: UserPromptSubmit
**Implementation**: `.claude/hooks/security-context-enhancer.py`

**Purpose**: Automatically inject security context, OWASP Top 10, and auth patterns

**Context to Add**:
- OWASP Top 10 checklist
- Authentication patterns from skills
- Security practices from skills
- Recent security-related commits
- Known vulnerabilities in dependencies

**Trigger Keywords**: "security", "auth", "vulnerability", "owasp", "xss", "sql injection"

**Skill Integration**:
- `security-practices` (security plugin)
- `authentication-patterns` (security plugin)

---

#### 3. Documentation Workflow Enhancement
**Target Agents**: `docs-architect`, `tech-docs-maintainer`, `tech-docs-orchestrator`
**Hook Type**: UserPromptSubmit + SessionStart
**Implementation**: `.claude/hooks/docs-context-enhancer.py`

**Purpose**: Inject documentation standards, ontological patterns, and API design guidelines

**Context to Add**:
- Documentation format (Markdown, RST)
- API design standards
- Ontological documentation patterns
- Recent documentation changes
- Undocumented code areas

**Trigger Keywords**: "document", "docs", "readme", "api", "ontology"

**Skill Integration**:
- `ontological-documentation` (developer-experience plugin) - Complex skill with templates
- `api-design-standards` (developer-experience plugin)

---

#### 4. Data Quality & Validation Enhancement
**Target Agents**: `data-validator`
**Hook Type**: UserPromptSubmit
**Implementation**: `.claude/hooks/data-quality-context-enhancer.py`

**Purpose**: Inject Pydantic v2 patterns, database conventions, and schema information

**Context to Add**:
- Database schema summary (PlanetScale PostgreSQL)
- Pydantic v2 validation patterns
- Recent migrations
- Data modeling best practices
- Database conventions

**Trigger Keywords**: "database", "schema", "migration", "pydantic", "validation", "data model"

**Skill Integration**:
- `data-modeling` (data-quality plugin)
- `database-conventions` (data-quality plugin)

---

#### 5. Observability & Performance Enhancement
**Target Agents**: `observability-engineer`, `memory-profiler`, `performance-optimizer`, `devops-troubleshooter`
**Hook Type**: UserPromptSubmit
**Implementation**: `.claude/hooks/observability-context-enhancer.py`

**Purpose**: Inject monitoring setup, SLO definitions, and performance baselines

**Context to Add**:
- Current monitoring stack (Datadog, Sentry, OpenTelemetry)
- Existing SLOs and SLIs
- Recent performance metrics
- Memory usage patterns
- Performance optimization guidelines

**Trigger Keywords**: "performance", "slow", "memory", "monitoring", "slo", "metric", "trace", "observability"

**Skill Integration**:
- `observability-monitoring` (observability plugin)
- `performance-optimization` (observability plugin)

---

#### 6. Linear Integration Enhancement
**Target Commands**: All Linear commands (7 commands)
**Hook Type**: UserPromptSubmit + PreToolUse
**Implementation**: `.claude/hooks/linear-context-enhancer.py`

**Purpose**: Automatically inject Linear issue context, workflow state, and commit format

**Context to Add**:
- Current Linear issue details (if issue ID detected)
- Linear workflow state
- Commit format requirements
- Related issues and PRs
- Team conventions

**Trigger Keywords**: Issue IDs (e.g., "DEV-123"), "linear", "issue", "ticket"

**Skill Integration**:
- `linear-workflow` (linear plugin)
- `commit-format` (linear plugin)

---

### Phase 2: Skill-Aware Context Injection (Medium Priority)

#### 7. Universal Skill Detector Hook
**Hook Type**: SessionStart + UserPromptSubmit
**Implementation**: `.claude/hooks/skill-context-injector.py`

**Purpose**: Automatically detect when a skill is relevant and inject its path as context

**How It Works**:
1. Scan all 20 skills at session start
2. Build skill index by keywords/domain
3. On UserPromptSubmit, detect relevant skills
4. Inject skill reference into context

**Example**:
```
User: "Implement TanStack Query for data fetching"
Hook injects: "📚 Relevant skill: tanstack-patterns at grey-haven-plugins/research/skills/"
```

**Skills to Index**:
- All 20 skills across all plugins
- Create keyword mappings for each skill
- Build reverse index for fast lookup

---

#### 8. Code Style & Standards Hook
**Hook Type**: PreToolUse (Edit, Write matchers)
**Implementation**: `.claude/hooks/code-style-validator.py`

**Purpose**: Inject code style requirements before file modifications

**Context to Add**:
- Linting configuration (.eslintrc, .prettierrc, ruff.toml)
- Code style skill reference
- Language-specific conventions
- Project structure guidelines

**Skills**:
- `code-style` (core and developer-experience)
- `project-structure` (developer-experience)

---

### Phase 3: Multi-Agent Orchestration (Advanced)

#### 9. Agent Orchestration Context Manager
**Target Agent**: `context-manager` (agent-orchestration plugin)
**Hook Type**: PreToolUse (Task matcher)
**Implementation**: `.claude/hooks/orchestration-context-manager.py`

**Purpose**: Enhanced context management for multi-agent workflows

**Features**:
- Detect agent chains (TDD → Code Review → Quality Pipeline)
- Pass context between agents
- Track workflow state
- Inject workflow composition patterns

**Commands**:
- `/context-save`
- `/context-restore`
- `/workflow-composer`

---

#### 10. Research Agent Enhancement
**Target Agents**: `web-docs-researcher`, `tech-docs-orchestrator`, `multi-agent-synthesis-orchestrator`
**Hook Type**: UserPromptSubmit + PreToolUse
**Implementation**: `.claude/hooks/research-context-enhancer.py`

**Purpose**: Inject research history, API documentation patterns, and learning goals

**Context to Add**:
- Previous research topics (from `.claude/context/research-history.json`)
- Relevant MCP tools (Firecrawl, Context7)
- API research patterns
- Technology stack detected in project

**MCP Integration**:
- Detect when to use `mcp__firecrawl__*` tools
- Inject Firecrawl usage patterns

---

### Phase 4: Specialized Workflow Hooks (Low Priority)

#### 11. Incident Response Context
**Target Agents**: `incident-responder`, `smart-debug`
**Hook Type**: UserPromptSubmit
**Implementation**: `.claude/hooks/incident-context-enhancer.py`

**Trigger Keywords**: "incident", "outage", "error", "production issue", "debug"

**Context**:
- Recent error logs
- Monitoring alerts
- Runbook references
- SLO violations

---

#### 12. Deployment Context
**Target Commands**: Cloudflare deployment commands
**Hook Type**: PreToolUse (Bash matcher for wrangler commands)
**Implementation**: `.claude/hooks/deployment-context-enhancer.py`

**Context**:
- Cloudflare Worker/Pages configuration
- Environment variables
- Deployment history
- Rollback procedures

---

## Implementation Priority Matrix

| Hook | Priority | Complexity | Impact | Agents Affected |
|------|----------|------------|--------|----------------|
| TDD Context Enhancer | HIGH | Medium | High | 3 agents |
| Security Context Enhancer | HIGH | Low | High | 2 agents |
| Skill Detector | HIGH | Medium | Very High | All agents |
| Docs Context Enhancer | MEDIUM | Medium | High | 3 agents |
| Data Quality Enhancer | MEDIUM | Low | Medium | 1 agent |
| Observability Enhancer | MEDIUM | Medium | High | 4 agents |
| Linear Context Enhancer | MEDIUM | Low | Medium | 7 commands |
| Code Style Validator | MEDIUM | Low | Medium | All edits |
| Research Enhancer | LOW | High | Medium | 4 agents |
| Orchestration Manager | LOW | High | High | 1 agent |
| Incident Context | LOW | Medium | Medium | 2 agents |
| Deployment Context | LOW | Low | Low | 1 plugin |

## Technical Architecture

### Hook Structure

```
.claude/hooks/
├── prompt-enhancer.py                    # ✅ Existing - General intent
├── subagent-context-preparer.py          # ✅ Existing - Subagent prep
├── security-validator.py                 # ✅ Existing - Security
├── work-completion-assistant.py          # ✅ Existing - Completion
│
├── tdd-context-enhancer.py              # 🆕 Phase 1
├── security-context-enhancer.py         # 🆕 Phase 1
├── docs-context-enhancer.py             # 🆕 Phase 1
├── data-quality-context-enhancer.py     # 🆕 Phase 1
├── observability-context-enhancer.py    # 🆕 Phase 1
├── linear-context-enhancer.py           # 🆕 Phase 1
│
├── skill-context-injector.py            # 🆕 Phase 2
├── code-style-validator.py              # 🆕 Phase 2
│
├── research-context-enhancer.py         # 🆕 Phase 3
├── orchestration-context-manager.py     # 🆕 Phase 3
│
├── incident-context-enhancer.py         # 🆕 Phase 4
└── deployment-context-enhancer.py       # 🆕 Phase 4
```

### Settings Configuration

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {"type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/prompt-enhancer.py"},
          {"type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/tdd-context-enhancer.py"},
          {"type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/security-context-enhancer.py"},
          {"type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/docs-context-enhancer.py"},
          {"type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/skill-context-injector.py"}
        ]
      }
    ],
    "SessionStart": [
      {
        "hooks": [
          {"type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/skill-context-injector.py"}
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Task",
        "hooks": [
          {"type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/subagent-context-preparer.py"},
          {"type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/orchestration-context-manager.py"}
        ]
      },
      {
        "matcher": "Edit|Write|MultiEdit",
        "hooks": [
          {"type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/code-style-validator.py"}
        ]
      }
    ]
  }
}
```

## Hook Coordination Strategy

### Avoiding Context Overload

With multiple hooks injecting context, we need strategies to prevent overwhelming Claude:

1. **Priority-Based Selection**
   - Only inject high-priority context
   - Limit to 3-5 context sections per prompt
   - Use confidence scoring

2. **Context Budget**
   - Each hook limited to ~200 tokens
   - Total context injection < 1000 tokens
   - Truncate low-priority items

3. **Deduplication**
   - Track what context is already in conversation
   - Don't re-inject if recently mentioned
   - Use session state tracking

4. **Conditional Injection**
   - Only inject if confidence > 70%
   - Require multiple keyword matches
   - Skip if context already present

### Hook Execution Order

All hooks in same event run in parallel, but we can use exit timing:
1. Fast checks first (keyword matching)
2. File system checks second
3. Git operations last (slower)

### Example Coordination

```python
class ContextCoordinator:
    MAX_TOTAL_TOKENS = 1000
    MAX_SECTIONS = 5

    def __init__(self):
        self.sections = []
        self.token_count = 0

    def add_section(self, priority: int, content: str, tokens: int):
        if self.token_count + tokens > self.MAX_TOTAL_TOKENS:
            return False
        if len(self.sections) >= self.MAX_SECTIONS:
            return False

        self.sections.append((priority, content))
        self.token_count += tokens
        return True

    def get_context(self) -> str:
        # Sort by priority, return top sections
        sorted_sections = sorted(self.sections, key=lambda x: x[0], reverse=True)
        return "\n\n".join([content for _, content in sorted_sections[:self.MAX_SECTIONS]])
```

## Testing Strategy

### Unit Testing Hooks

Each hook should have:
1. Intent detection tests
2. Context generation tests
3. Edge case handling
4. Performance tests (< 100ms execution)

### Integration Testing

1. Test hook combinations
2. Verify context quality with real agents
3. Measure context injection effectiveness
4. Monitor token usage

### Example Test

```python
def test_tdd_context_enhancer():
    # Test intent detection
    assert detect_tdd_intent("write unit tests for user service")
    assert not detect_tdd_intent("fix typo in readme")

    # Test context generation
    context = enhance_tdd_context("add tests for login")
    assert "Test Framework:" in context
    assert "Coverage:" in context
    assert "TDD Cycle:" in context
```

## Metrics & Success Criteria

### Hook Effectiveness Metrics

1. **Context Relevance**
   - % of injected context used by Claude
   - User satisfaction with context quality
   - Reduction in "missing context" errors

2. **Performance**
   - Hook execution time (target < 100ms)
   - Token usage per hook
   - Total context overhead

3. **Agent Effectiveness**
   - Task completion rate improvement
   - Reduction in back-and-forth clarifications
   - Code quality metrics

### Success Criteria (Phase 1)

- [ ] 6 new hooks implemented
- [ ] < 100ms average execution time per hook
- [ ] < 1000 tokens total context injection
- [ ] > 80% context relevance score
- [ ] No duplicate context injection
- [ ] All hooks have unit tests

## Implementation Roadmap

### Week 1-2: Phase 1 High Priority Hooks
1. Implement TDD Context Enhancer
2. Implement Security Context Enhancer
3. Implement Docs Context Enhancer
4. Write unit tests
5. Deploy and monitor

### Week 3-4: Phase 1 Continuation + Phase 2
1. Implement Data Quality Enhancer
2. Implement Observability Enhancer
3. Implement Linear Context Enhancer
4. Start Skill Detector (Phase 2)
5. Comprehensive testing

### Week 5-6: Phase 2 Completion
1. Complete Skill Detector
2. Implement Code Style Validator
3. Refine coordination strategy
4. Performance optimization

### Week 7-8: Phase 3 Advanced Features
1. Research Context Enhancer
2. Orchestration Context Manager
3. Multi-agent workflow testing

### Week 9-10: Phase 4 & Polish
1. Incident Context Enhancer
2. Deployment Context Enhancer
3. Documentation
4. Performance tuning
5. User feedback incorporation

## Next Steps

1. **Review this plan** with the team
2. **Prioritize** which hooks to implement first based on your workflow
3. **Start with Phase 1** - implement highest-impact hooks
4. **Measure effectiveness** - track metrics from day 1
5. **Iterate** - refine based on real-world usage

## Questions to Consider

1. Which agents do you use most frequently?
2. What context do you find yourself repeatedly providing?
3. Which skills are most valuable to your workflow?
4. Are there domain-specific contexts we should add?
5. What's your tolerance for context injection verbosity?

## References

- [Claude Code Hooks Documentation](https://docs.anthropic.com/en/docs/claude-code/hooks)
- [Hooks Guide](https://docs.anthropic.com/en/docs/claude-code/hooks-guide)
- Grey Haven Plugins: `/home/user/claude-code-config/grey-haven-plugins/`
- Existing Hooks: `/home/user/claude-code-config/.claude/hooks/`
