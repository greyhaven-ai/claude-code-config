# Context Manager Examples

Real-world examples of multi-agent workflow context management and state persistence.

## Quick Navigation

| Example | Workflow Type | Agents Involved | Context Size | Complexity |
|---------|---------------|-----------------|--------------|------------|
| [Feature Development Handoff](feature-development-handoff.md) | Sequential | 4 agents | Medium | Moderate |
| [Incident Response Workflow](incident-response-workflow.md) | Parallel + Sequential | 6 agents | Large | High |
| [Code Review Pipeline](code-review-pipeline.md) | Conditional | 3 agents | Small | Low |
| [Multi-Session Refactoring](multi-session-refactoring.md) | Resumable | 5 agents | Large | Very High |

## Context Management Patterns

### Pattern 1: Sequential Handoff
**Use Case:** Linear workflow where each agent completes before next begins

**Example**: Design → Implement → Test → Deploy
```
Agent A (Designer) → Context Save → Agent B (Developer)
                                   → Context Save → Agent C (Tester)
                                                  → Context Save → Agent D (DevOps)
```

**Context Contains:**
- Decisions made by previous agents
- Modified files
- Pending actions for next agent
- Constraints and requirements

### Pattern 2: Parallel Execution
**Use Case:** Multiple agents work concurrently on independent tasks

**Example**: Frontend + Backend + Database development in parallel
```
Context Fork → Agent A (Frontend)  → Context Merge
            → Agent B (Backend)    →
            → Agent C (Database)   →
```

**Challenges:**
- Conflict resolution when merging
- Dependency coordination
- Partial failure handling

### Pattern 3: Conditional Routing
**Use Case:** Next agent determined by previous agent's outcome

**Example**: Code review → (Pass: Deploy) | (Fail: Fix) → Re-review
```
Agent A (Reviewer) → Decision Point → (if pass) Agent B (Deploy)
                                   → (if fail) Agent C (Fix) → back to Agent A
```

**Context Needs:**
- Decision criteria
- Route history
- Loop detection

### Pattern 4: Long-Running Resumable
**Use Case:** Workflow spans multiple sessions/days

**Example**: Large codebase refactoring over 3 days
```
Day 1: Agent A → Save checkpoint
Day 2: Restore → Agent A continues → Save checkpoint
Day 3: Restore → Agent B (testing) → Complete
```

**Critical Features:**
- Robust serialization
- Version compatibility
- Progress tracking
- Partial completion handling

## Context Size Benchmarks

| Workflow Type | Avg Context Size | Serialization Time | Restore Time |
|---------------|------------------|-------------------|--------------|
| Simple (1-2 agents) | 5-10 KB | < 10ms | < 10ms |
| Moderate (3-5 agents) | 20-50 KB | 20-50ms | 20-50ms |
| Complex (6+ agents) | 100-200 KB | 100-200ms | 100-200ms |
| Large (multi-session) | 500KB-2MB | 500ms-1s | 500ms-1s |

**Optimization Target:** < 100KB for 80% of workflows

## State Management Strategies

### Minimal State
**Principle:** Only save essential context

**Includes:**
- File paths (not file contents)
- Decision summaries (not full reasoning)
- Pending actions (not completed tasks)

**Benefits:**
- Faster serialization
- Lower storage
- Easier debugging

### Comprehensive State
**Principle:** Save everything for full resumption

**Includes:**
- Complete conversation history
- All file modifications
- Full reasoning chains
- Error logs

**Benefits:**
- Perfect restoration
- Complete audit trail
- Advanced debugging

### Hybrid Approach
**Principle:** Essential + compression

**Strategy:**
- Essential context in JSON
- Full history compressed separately
- Load essential first, decompress on demand

## Common Pitfalls

### Pitfall 1: Context Bloat
**Symptom:** Context grows unbounded
**Solution:** Pruning strategy - remove completed tasks, compress history

### Pitfall 2: Version Incompatibility
**Symptom:** Can't restore old contexts after updates
**Solution:** Context versioning with migration scripts

### Pitfall 3: Missing Dependencies
**Symptom:** Context refers to external state that changed
**Solution:** Capture or validate external dependencies

### Pitfall 4: Concurrent Modification
**Symptom:** Two agents modify same context simultaneously
**Solution:** Locking or optimistic concurrency

### Pitfall 5: Sensitive Data in Context
**Symptom:** API keys, passwords in saved context
**Solution:** Redaction and encryption

## Success Metrics

**Context Quality Indicators:**
- Restoration success rate: Target > 99%
- Context size vs workflow complexity: Linear relationship
- Time to restore: Target < 1 second
- Agent resume success: Target > 95%

**Workflow Efficiency:**
- Reduced re-work: 70% reduction
- Faster handoffs: < 30 seconds
- Session continuity: Seamless multi-day workflows

## Quick Reference: Context Schema

**Minimal Required Fields:**
```json
{
  "version": "1.0",
  "workflow_id": "unique-id",
  "timestamp": "ISO-8601",
  "current_agent": "agent-name",
  "next_agent": "agent-name",
  "phase": "current-phase",
  "files_modified": ["paths"],
  "decisions": ["summaries"],
  "pending_actions": ["tasks"]
}
```

**Extended Optional Fields:**
```json
{
  "conversation_history": [...],
  "error_log": [...],
  "checkpoints": [...],
  "metadata": {...}
}
```

## Navigation Tips

- **New to context management?** Start with [Code Review Pipeline](code-review-pipeline.md)
- **Complex workflows?** See [Feature Development Handoff](feature-development-handoff.md)
- **Multi-session work?** Check [Multi-Session Refactoring](multi-session-refactoring.md)
- **Parallel agents?** Review [Incident Response Workflow](incident-response-workflow.md)

---

**Total Examples**: 4 comprehensive workflow scenarios
**Patterns Covered**: Sequential, Parallel, Conditional, Resumable
**Context Sizes**: 5KB to 2MB
**Success Rate**: 99%+ restoration across all patterns
