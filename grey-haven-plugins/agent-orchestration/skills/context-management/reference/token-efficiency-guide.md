# Token Efficiency Guide

Understanding and optimizing token usage in multi-agent workflows.

## Token Multiplier Effect

Different architectures have dramatically different token costs:

| Architecture | Token Multiplier | Example (10K input) |
|--------------|------------------|---------------------|
| Single agent | 1x | 10K tokens |
| Agent + tools | 4x | 40K tokens |
| Multi-agent | 15x | 150K tokens |
| Multi-agent + tools | 60x | 600K tokens |

### Why Multi-Agent is Expensive

Each agent in a multi-agent system:
1. Receives full context (or summary)
2. Processes independently
3. Returns results to coordinator
4. Coordinator processes aggregated results

```
Coordinator (10K) ──┬──▶ Agent A (5K) = 5K
                    ├──▶ Agent B (5K) = 5K
                    └──▶ Agent C (5K) = 5K

Total: 10K + (3 × 5K) + aggregation = ~25K minimum
```

## Attention Budget

### What is Attention Budget?

LLMs have limited "attention" - the ability to reason about all tokens in context simultaneously. As context grows:
- Attention per token decreases
- Earlier context becomes less influential
- "Lost in the middle" effect occurs

### Attention Budget Guidelines

| Context Size | Attention Quality | Use Case |
|--------------|-------------------|----------|
| <4K tokens | Excellent | Critical reasoning |
| 4K-16K tokens | Good | Standard tasks |
| 16K-32K tokens | Moderate | Reference lookups |
| 32K+ tokens | Low | Background context only |

### Managing Attention Budget

**Do**:
- Put critical information at start and end
- Use clear section headers
- Summarize verbose content
- Remove irrelevant context

**Don't**:
- Dump entire files when only sections needed
- Include full history for simple tasks
- Pass raw logs without filtering

## Context Optimization Strategies

### 1. Progressive Disclosure

Reveal information only when needed:

```
Phase 1: High-level task description
↓
Phase 2: Add relevant file contents
↓
Phase 3: Add specific code sections
↓
Phase 4: Add error details if needed
```

### 2. Observation Masking

Hide irrelevant tool outputs from context:

```typescript
// Instead of:
"Tool output: [50KB of JSON response]"

// Use:
"Tool output: Successfully retrieved 1,247 records.
 Key fields: id, name, status"
```

### 3. Context Compaction

When context grows too large:

```
Before compaction:
- Full conversation history (30K tokens)
- All file contents (20K tokens)
- All tool outputs (15K tokens)
Total: 65K tokens

After compaction:
- Conversation summary (2K tokens)
- Relevant file excerpts (5K tokens)
- Key tool results only (1K tokens)
Total: 8K tokens
```

### 4. Selective Context Loading

Load context based on task type:

| Task Type | Load | Skip |
|-----------|------|------|
| Code review | Changed files, related tests | Unrelated modules |
| Bug fix | Error logs, failing test, related code | Feature docs |
| New feature | Requirements, similar code patterns | Historical discussions |

## Multi-Agent Context Patterns

### Pattern 1: Context Isolation

Each agent gets only what it needs:

```
Coordinator
├── Frontend Agent
│   └── Context: React components, CSS, types
├── Backend Agent
│   └── Context: API routes, database queries
└── Test Agent
    └── Context: Test files, coverage data
```

**Benefit**: Smaller context per agent = better reasoning

### Pattern 2: Summary Handoff

Don't pass raw context between agents:

```
Agent A completes work
↓
Coordinator creates summary:
- Files modified: 3
- Key changes: Added validation, updated types
- Outstanding issues: None
↓
Agent B receives summary (not full context)
```

### Pattern 3: Reference, Don't Copy

```
# Bad: Copy entire file content
context = {
    "file_content": read_entire_file("app.py")  # 10K tokens
}

# Good: Reference with excerpt
context = {
    "file_path": "app.py",
    "relevant_lines": "42-58",
    "excerpt": "function validate_input..."  # 200 tokens
}
```

## The "Telephone Game" Problem

When passing context through multiple agents, information degrades:

```
Original: "Fix the bug in user authentication"
↓ Agent A
"Address the issue with login"
↓ Agent B
"Look at the login problem"
↓ Agent C
"There's something wrong with login"  # Lost specificity
```

### Solution: Forward Original Message

```typescript
interface AgentContext {
    originalTask: string    // Always include
    previousSummary: string // Condensed handoff
    currentPhase: string    // Where we are now
}
```

## Token Cost Estimation

### Quick Estimation

```
Tokens ≈ Words × 1.3
Tokens ≈ Characters / 4
```

### Per-Model Costs

| Model | Input ($/1M) | Output ($/1M) |
|-------|--------------|---------------|
| Haiku 3.5 | $0.80 | $4.00 |
| Sonnet 4 | $3.00 | $15.00 |
| Opus 4.5 | $15.00 | $75.00 |

### Multi-Agent Cost Example

```
3-agent workflow, each agent:
- Input: 5K tokens
- Output: 2K tokens
- Coordination overhead: 3K tokens

Total tokens: (3 × 5K) + (3 × 2K) + 3K = 24K tokens

Cost (Sonnet):
  Input: 15K × $3.00/1M = $0.045
  Output: 6K × $15.00/1M = $0.090
  Coordination: 3K × $3.00/1M = $0.009
  Total: ~$0.14 per workflow
```

## Optimization Checklist

- [ ] Know your context size (measure, don't guess)
- [ ] Apply token multiplier awareness when designing
- [ ] Use progressive disclosure, not upfront dump
- [ ] Summarize before handoffs
- [ ] Reference files, don't copy
- [ ] Forward original task in multi-agent flows
- [ ] Track and log token usage
- [ ] Set cost budgets per workflow type

---

*Understanding token economics prevents both cost overruns and quality degradation*
