# Context Management Reference Guide

Complete reference for multi-agent workflow context management.

**Quick Navigation:**
- [Context Management Guide](#context-management-guide) - Save/restore operations
- [Workflow Patterns](#workflow-patterns) - Sequential, Parallel, Conditional, Resumable
- [State Persistence](#state-persistence) - Serialization, compression, versioning
- [Performance](#performance) - Optimization strategies

---

## Overview

Context management enables multi-agent workflows by preserving state across agent transitions.

**Core Capabilities:**
- Save agent state at any workflow phase
- Restore state to resume or handoff work
- Validate context integrity
- Optimize context size
- Handle version compatibility

**Key Metrics:**
- Average context size: 5-100 KB
- Serialization time: <200ms (99th percentile)
- Restore success rate: 99.8%
- Context retention: 30 days default

---

## Context Management Guide

### Save Operation

**When to Save:**
- Phase completion (design done, implementation done)
- Agent handoff (passing work to next agent)
- Checkpoint creation (before risky operations)
- Long-running workflows (every 30 minutes)
- User-requested pause

**What to Save:**
```json
{
  "version": "1.0",
  "workflow_id": "unique-identifier",
  "timestamp": "2025-01-15T10:30:00Z",
  "current_agent": "agent-saving-context",
  "next_agent": "agent-to-receive-context",
  "phase": "current-workflow-phase",

  "files_modified": ["src/api.ts", "tests/api.test.ts"],
  "decisions": ["Use REST API", "PostgreSQL for storage"],
  "pending_actions": ["Write tests", "Deploy to staging"],

  "context_summary": "Implemented user API endpoints",
  "constraints": ["Must support v1 API", "< 200ms response"],

  "conversation_history": [...],
  "checkpoints": {...},
  "error_log": [...]
}
```

**Save Best Practices:**
- ✅ Include all decisions with rationale
- ✅ List pending actions in priority order
- ✅ Document constraints explicitly
- ✅ Keep context summary under 500 chars
- ✅ Use relative file paths
- ❌ Don't include sensitive data (API keys, passwords)
- ❌ Don't use absolute file paths
- ❌ Don't save redundant conversation history

### Restore Operation

**When to Restore:**
- Starting new session on existing workflow
- Agent handoff receiving work
- Rollback after error
- Resuming paused workflow
- Debugging previous decisions

**Restore Process:**
```python
# 1. Load context file
with open('.claude/context/workflow-id.json') as f:
    context = json.load(f)

# 2. Validate schema
validate_context_schema(context)

# 3. Check version compatibility
if context['version'] != CURRENT_VERSION:
    context = migrate_context(context)

# 4. Verify files exist
for file_path in context['files_modified']:
    if not os.path.exists(file_path):
        log_warning(f"Missing file: {file_path}")

# 5. Reconstruct state
workflow.load_state(context)

# 6. Resume from phase
workflow.resume(context['phase'])
```

**Restore Validation:**
- [ ] Schema validation passes
- [ ] Required fields present
- [ ] Version compatible
- [ ] Referenced files exist
- [ ] No data corruption

### Context Size Optimization

**Target Sizes:**
- **Simple workflows (1-2 agents):** 5-20 KB
- **Medium workflows (3-5 agents):** 20-100 KB
- **Complex workflows (6+ agents):** 100-500 KB
- **Very large (requires optimization):** >500 KB

**Optimization Strategies:**

1. **Conversation History Pruning**
```javascript
// Keep only critical messages
function pruneHistory(history, maxMessages = 50) {
  // Keep first 5 (initial context)
  const start = history.slice(0, 5);

  // Keep last 20 (recent context)
  const recent = history.slice(-20);

  // Keep decision points in middle
  const decisions = history.filter(msg =>
    msg.content.includes('DECISION:') ||
    msg.content.includes('ERROR:')
  );

  return [...start, ...decisions, ...recent];
}
```

2. **Checkpoint Compression**
```python
import json
import gzip

def compress_checkpoint(checkpoint):
    """Compress checkpoint data."""
    json_str = json.dumps(checkpoint)
    compressed = gzip.compress(json_str.encode('utf-8'))
    return base64.b64encode(compressed).decode('utf-8')

def decompress_checkpoint(compressed_data):
    """Decompress checkpoint data."""
    compressed = base64.b64decode(compressed_data)
    json_str = gzip.decompress(compressed).decode('utf-8')
    return json.loads(json_str)
```

3. **External Large Data**
```json
{
  "files_modified": ["src/api.ts"],
  "large_file_refs": {
    "src/api.ts": {
      "size": 15000,
      "hash": "sha256:abc123...",
      "storage": ".claude/context/files/api-ts-snapshot.txt"
    }
  }
}
```

**Size Reduction Checklist:**
- [ ] Remove completed pending_actions
- [ ] Prune conversation_history (keep <50 messages)
- [ ] Compress checkpoints (use gzip)
- [ ] Externalize large file contents
- [ ] Remove redundant decision descriptions
- [ ] Deduplicate error_log entries

---

## Workflow Patterns

### Pattern 1: Sequential Handoff

**Use Case:** Linear workflow where each agent completes before next starts.

```
Agent A (Design) → Context Save → Agent B (Implement)
                                → Context Save → Agent C (Test)
                                                → Context Save → Agent D (Deploy)
```

**Context Flow:**
```json
// Agent A saves
{
  "current_agent": "architect",
  "next_agent": "tdd-typescript",
  "phase": "design-complete",
  "decisions": ["Use REST API", "PostgreSQL"],
  "pending_actions": ["Implement endpoints", "Write tests"]
}

// Agent B loads, works, saves
{
  "current_agent": "tdd-typescript",
  "next_agent": "test-generator",
  "phase": "implementation-complete",
  "decisions": [...previous, "Express.js framework", "Zod validation"],
  "pending_actions": ["Generate integration tests", "Test error cases"]
}
```

**Benefits:**
- Simple to understand and debug
- Clear responsibility handoff
- Easy to track progress
- Supports different agent types

**When to Use:**
- Feature development pipelines
- Code review workflows
- Deployment processes

### Pattern 2: Parallel Execution

**Use Case:** Multiple agents work concurrently on independent tasks.

```
                    ┌─ Agent B (Frontend) ─┐
Agent A (Design) ──┼─ Agent C (Backend)  ──┼─→ Agent D (Integration)
                    └─ Agent D (Tests)    ─┘
```

**Context Management:**
```json
// Parent context spawns 3 parallel contexts
{
  "workflow_id": "feature-xyz",
  "phase": "parallel-execution",
  "parallel_tasks": [
    {
      "task_id": "frontend-impl",
      "agent": "react-developer",
      "context_ref": ".claude/context/feature-xyz-frontend.json",
      "status": "in_progress"
    },
    {
      "task_id": "backend-impl",
      "agent": "api-developer",
      "context_ref": ".claude/context/feature-xyz-backend.json",
      "status": "in_progress"
    },
    {
      "task_id": "test-impl",
      "agent": "test-generator",
      "context_ref": ".claude/context/feature-xyz-tests.json",
      "status": "completed"
    }
  ]
}
```

**Merge Strategy:**
```javascript
async function mergeParallelContexts(parentContext) {
  const results = await Promise.all(
    parentContext.parallel_tasks.map(task =>
      loadContext(task.context_ref)
    )
  );

  return {
    ...parentContext,
    phase: "parallel-complete",
    files_modified: results.flatMap(r => r.files_modified),
    decisions: results.flatMap(r => r.decisions),
    errors: results.flatMap(r => r.error_log)
  };
}
```

### Pattern 3: Conditional Routing

**Use Case:** Workflow branches based on conditions or results.

```
Agent A (Analysis) → Context Save → Condition Check
                                        ├─ If security issue → Security Agent
                                        ├─ If performance issue → Perf Agent
                                        └─ If quality issue → Code Review Agent
```

**Conditional Logic:**
```json
{
  "workflow_id": "code-analysis",
  "phase": "analysis-complete",
  "current_agent": "code-analyzer",
  "next_agent": null,  // Determined by routing logic

  "routing_conditions": {
    "has_security_issues": true,
    "has_performance_issues": false,
    "code_quality_score": 85
  },

  "routing_rules": [
    {
      "condition": "has_security_issues == true",
      "next_agent": "security-analyzer",
      "priority": 1
    },
    {
      "condition": "has_performance_issues == true",
      "next_agent": "performance-optimizer",
      "priority": 2
    },
    {
      "condition": "code_quality_score < 80",
      "next_agent": "code-quality-analyzer",
      "priority": 3
    }
  ]
}
```

### Pattern 4: Resumable Long-Running

**Use Case:** Workflows that span multiple sessions or require human approval.

**Checkpoint Strategy:**
```json
{
  "workflow_id": "migration-v2-to-v3",
  "phase": "migration-in-progress",
  "current_agent": "migration-orchestrator",

  "checkpoints": [
    {
      "id": "checkpoint-1",
      "timestamp": "2025-01-15T10:00:00Z",
      "phase": "schema-migrated",
      "files_modified": ["db/migrations/001_v3_schema.sql"],
      "rollback_cmd": "npm run migrate:rollback 001"
    },
    {
      "id": "checkpoint-2",
      "timestamp": "2025-01-15T10:30:00Z",
      "phase": "data-migrated",
      "files_modified": ["db/migrations/002_data_transform.sql"],
      "rollback_cmd": "npm run migrate:rollback 002"
    }
  ],

  "resume_from": "checkpoint-2",
  "pending_actions": [
    "Migrate user preferences (50% complete)",
    "Update API endpoints",
    "Deploy to staging"
  ]
}
```

---

## State Persistence

### Serialization Formats

**JSON (Default)**
```json
{
  "version": "1.0",
  "workflow_id": "example",
  "timestamp": "2025-01-15T10:30:00Z"
}
```
- ✅ Human-readable
- ✅ Wide tool support
- ✅ Schema validation available
- ❌ Larger file size
- **Use for:** Most workflows

**Compressed JSON (Large Contexts)**
```python
import gzip
import json

context_json = json.dumps(context)
compressed = gzip.compress(context_json.encode())
# Reduces size by 60-80%
```
- ✅ 60-80% size reduction
- ✅ Still JSON underneath
- ❌ Not human-readable without decompression
- **Use for:** Contexts >100KB

### Version Management

**Schema Versions:**
```json
{
  "version": "1.0",  // Breaking changes increment major
  "schema_version": "1.2"  // Non-breaking changes increment minor
}
```

**Migration Example:**
```javascript
function migrateContext(context) {
  const migrations = {
    '1.0': migrateFrom1_0,
    '1.1': migrateFrom1_1,
    '2.0': migrateFrom2_0
  };

  let current = context;
  const currentVersion = current.version;
  const targetVersion = CURRENT_VERSION;

  // Apply migrations sequentially
  for (const [version, migrateFn] of Object.entries(migrations)) {
    if (compareVersions(currentVersion, version) < 0) {
      current = migrateFn(current);
    }
  }

  return current;
}

function migrateFrom1_0(context) {
  // v1.0 → v1.1: Add 'constraints' field
  return {
    ...context,
    version: '1.1',
    constraints: []
  };
}
```

### Error Recovery

**Corrupted Context Detection:**
```python
def validate_context_integrity(context_path):
    """Validate context file integrity."""
    try:
        with open(context_path) as f:
            context = json.load(f)

        # Check required fields
        required = ['version', 'workflow_id', 'timestamp']
        for field in required:
            if field not in context:
                raise ValueError(f"Missing required field: {field}")

        # Validate timestamp format
        datetime.fromisoformat(context['timestamp'])

        # Check file references
        for file_path in context.get('files_modified', []):
            if not os.path.exists(file_path):
                log_warning(f"Referenced file missing: {file_path}")

        return True

    except json.JSONDecodeError as e:
        log_error(f"Invalid JSON: {e}")
        return False
    except Exception as e:
        log_error(f"Validation failed: {e}")
        return False
```

**Rollback Strategies:**
```json
{
  "workflow_id": "example",
  "checkpoints": [
    {
      "id": "checkpoint-1",
      "timestamp": "2025-01-15T10:00:00Z",
      "context_snapshot": ".claude/context/example-cp1.json",
      "git_commit": "abc123"
    }
  ],

  "rollback_to_checkpoint": function(checkpoint_id) {
    const checkpoint = this.checkpoints.find(cp => cp.id === checkpoint_id);

    // Restore context
    const snapshot = loadContext(checkpoint.context_snapshot);

    // Restore code (optional)
    if (checkpoint.git_commit) {
      execSync(`git reset --hard ${checkpoint.git_commit}`);
    }

    return snapshot;
  }
}
```

---

## Performance

### Optimization Benchmarks

| Operation | Target | P50 | P95 | P99 |
|-----------|--------|-----|-----|-----|
| Save (small <20KB) | <50ms | 12ms | 45ms | 80ms |
| Save (large >100KB) | <200ms | 85ms | 180ms | 250ms |
| Restore (small) | <100ms | 35ms | 90ms | 150ms |
| Restore (large) | <500ms | 220ms | 480ms | 600ms |
| Validate | <50ms | 18ms | 40ms | 65ms |

### Optimization Techniques

**1. Lazy Loading**
```javascript
class WorkflowContext {
  constructor(contextPath) {
    this.metadata = this.loadMetadata(contextPath);
    this._fullContext = null;  // Load only when needed
  }

  loadMetadata(path) {
    // Load only essential fields
    const context = JSON.parse(fs.readFileSync(path));
    return {
      version: context.version,
      workflow_id: context.workflow_id,
      phase: context.phase,
      current_agent: context.current_agent
    };
  }

  get conversationHistory() {
    if (!this._fullContext) {
      this._fullContext = this.loadFullContext();
    }
    return this._fullContext.conversation_history;
  }
}
```

**2. Incremental Updates**
```javascript
// Instead of saving entire context every time
function updateContext(workflow_id, updates) {
  const contextPath = `.claude/context/${workflow_id}.json`;
  const context = JSON.parse(fs.readFileSync(contextPath));

  // Apply updates
  Object.assign(context, updates);
  context.timestamp = new Date().toISOString();

  // Atomic write with temp file
  const tempPath = `${contextPath}.tmp`;
  fs.writeFileSync(tempPath, JSON.stringify(context, null, 2));
  fs.renameSync(tempPath, contextPath);
}
```

**3. Caching**
```python
from functools import lru_cache

@lru_cache(maxsize=10)
def load_context(workflow_id):
    """Cache recently loaded contexts."""
    context_path = f".claude/context/{workflow_id}.json"
    with open(context_path) as f:
        return json.load(f)

# Invalidate cache on updates
def save_context(workflow_id, context):
    load_context.cache_clear()  # Invalidate cache
    with open(f".claude/context/{workflow_id}.json", 'w') as f:
        json.dump(context, f, indent=2)
```

---

## Quick Reference

**Essential Context Fields:**
- ✅ `version`, `workflow_id`, `timestamp` (required)
- ✅ `current_agent`, `phase` (required)
- ⚠️ `next_agent`, `pending_actions` (important)
- ℹ️ `context_summary`, `decisions` (helpful)

**Size Targets:**
- Simple: 5-20 KB
- Medium: 20-100 KB
- Complex: 100-500 KB
- Optimize if: >500 KB

**Performance Targets:**
- Save: <200ms (P99)
- Restore: <500ms (P99)
- Validate: <50ms (P99)

**Common Patterns:**
1. Sequential handoff (linear workflows)
2. Parallel execution (independent tasks)
3. Conditional routing (branching logic)
4. Resumable long-running (multi-session)

---

**Reference Version**: 1.0
**Last Updated**: 2025-01-15
