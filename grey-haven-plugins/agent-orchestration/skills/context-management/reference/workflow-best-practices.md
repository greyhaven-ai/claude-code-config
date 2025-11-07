# Workflow Best Practices

Production-ready patterns and practices for multi-agent workflows.

**Quick Navigation:**
- [Context Design](#context-design)
- [Handoff Patterns](#handoff-patterns)
- [Error Handling](#error-handling)
- [Performance](#performance)
- [Security](#security)
- [Testing](#testing)

---

## Context Design

### Principle 1: Minimal Context Size

**Why:** Smaller contexts = faster operations, lower memory, easier debugging.

**Practice:**
```javascript
// ❌ BAD: Include everything
const context = {
  workflow_id: 'feature-123',
  // ... required fields ...

  all_git_commits: gitLog(),  // Huge!
  full_codebase: readAllFiles(),  // Unnecessary!
  raw_logs: getSystemLogs()  // Too much!
};

// ✅ GOOD: Only essential information
const context = {
  workflow_id: 'feature-123',
  version: '1.0',
  timestamp: new Date().toISOString(),
  current_agent: 'backend-architect',
  phase: 'design-complete',

  // Only modified files
  files_modified: ['src/api/users.ts', 'tests/api.test.ts'],

  // Only key decisions
  decisions: [
    'Use PostgreSQL for user data',
    'Implement JWT authentication',
    'Rate limit: 100 req/min per user'
  ],

  // Only next actions
  pending_actions: [
    'Implement user endpoints',
    'Add authentication middleware',
    'Write integration tests'
  ]
};
```

**Guidelines:**
- Target <100KB for 80% of workflows
- Include only information next agent needs
- Reference external data instead of embedding
- Prune completed actions regularly

---

### Principle 2: Explicit Over Implicit

**Why:** Clear intent prevents misunderstandings and errors.

**Practice:**
```javascript
// ❌ BAD: Implicit assumptions
const context = {
  files_modified: ['api.ts'],
  next_agent: 'test-generator'
  // Unclear: What should test-generator do?
  // Unclear: Are there constraints?
};

// ✅ GOOD: Explicit requirements
const context = {
  files_modified: ['src/api/users.ts'],
  next_agent: 'test-generator',

  pending_actions: [
    {
      action: 'generate_integration_tests',
      target: 'src/api/users.ts',
      requirements: [
        'Test all CRUD operations',
        'Test authentication',
        'Test error cases (401, 403, 404, 500)',
        'Test rate limiting'
      ],
      constraints: [
        'Use Vitest framework',
        'Coverage must be >90%',
        'Tests must be idempotent'
      ]
    }
  ],

  context_summary: 'User API implemented with JWT auth. Need comprehensive tests before deployment.'
};
```

**Checklist:**
- [ ] Next agent explicitly stated
- [ ] Actions clearly described
- [ ] Requirements enumerated
- [ ] Constraints documented
- [ ] Success criteria defined

---

### Principle 3: Versioned Evolution

**Why:** Workflows evolve. Version tracking enables migration and compatibility.

**Practice:**
```json
{
  "version": "2.1",
  "schema_version": "2.1.0",

  "version_history": [
    {
      "version": "1.0",
      "timestamp": "2025-01-10T10:00:00Z",
      "changes": "Initial context structure"
    },
    {
      "version": "2.0",
      "timestamp": "2025-01-12T14:30:00Z",
      "changes": "Added metadata and constraints fields"
    },
    {
      "version": "2.1",
      "timestamp": "2025-01-15T09:00:00Z",
      "changes": "Added parallel task support"
    }
  ],

  "migration_path": {
    "1.0_to_2.0": "Add metadata and constraints with defaults",
    "2.0_to_2.1": "Add parallel_tasks array if missing"
  }
}
```

**Guidelines:**
- Increment major version for breaking changes
- Increment minor version for new fields
- Document migration path
- Maintain backward compatibility for 2 versions

---

## Handoff Patterns

### Pattern 1: Clean Handoff

**When:** Sequential workflow where each agent completes fully before handoff.

**Implementation:**
```javascript
class WorkflowOrchestrator {
  async executeCleanHandoff(agents) {
    let context = this.initializeContext();

    for (const agent of agents) {
      console.log(`Starting agent: ${agent.name}`);

      // Load previous context
      const agentContext = {
        ...context,
        current_agent: agent.name,
        next_agent: agents[agents.indexOf(agent) + 1]?.name || null
      };

      // Execute agent
      const result = await agent.execute(agentContext);

      // Validate completion
      if (result.status !== 'completed') {
        throw new Error(`Agent ${agent.name} did not complete successfully`);
      }

      // Update context with results
      context = {
        ...context,
        phase: result.phase,
        files_modified: [
          ...context.files_modified,
          ...result.files_modified
        ],
        decisions: [
          ...context.decisions,
          ...result.decisions
        ],
        pending_actions: result.pending_actions
      };

      // Save checkpoint
      await this.saveContext(context);

      console.log(`✅ Completed agent: ${agent.name}`);
    }

    return context;
  }
}
```

**Best Practices:**
- Save context after each agent
- Validate agent completion
- Accumulate decisions and files
- Clear completed actions

---

### Pattern 2: Conditional Handoff

**When:** Next agent depends on results or conditions.

**Implementation:**
```javascript
class ConditionalRouter {
  async routeBasedOnResults(context, analysisResults) {
    // Define routing rules
    const rules = [
      {
        condition: () => analysisResults.security_score < 70,
        next_agent: 'security-analyzer',
        priority: 1,
        reason: 'Security vulnerabilities detected'
      },
      {
        condition: () => analysisResults.performance_score < 80,
        next_agent: 'performance-optimizer',
        priority: 2,
        reason: 'Performance issues detected'
      },
      {
        condition: () => analysisResults.test_coverage < 85,
        next_agent: 'test-generator',
        priority: 3,
        reason: 'Insufficient test coverage'
      }
    ];

    // Find highest priority match
    const match = rules
      .filter(rule => rule.condition())
      .sort((a, b) => a.priority - b.priority)[0];

    if (match) {
      // Update context for routing
      return {
        ...context,
        next_agent: match.next_agent,
        routing_reason: match.reason,
        routing_data: analysisResults
      };
    }

    // No issues - proceed to deployment
    return {
      ...context,
      next_agent: 'deployment-agent',
      routing_reason: 'All checks passed'
    };
  }
}
```

---

### Pattern 3: Parallel Handoff with Merge

**When:** Multiple agents can work concurrently, then merge results.

**Implementation:**
```javascript
class ParallelOrchestrator {
  async executeParallel(parentContext, tasks) {
    // Spawn parallel contexts
    const parallelContexts = tasks.map(task => ({
      ...parentContext,
      workflow_id: `${parentContext.workflow_id}-${task.id}`,
      current_agent: task.agent,
      task_id: task.id,
      task_scope: task.scope
    }));

    // Execute all tasks in parallel
    const results = await Promise.allSettled(
      parallelContexts.map((ctx, i) =>
        this.executeTask(tasks[i], ctx)
      )
    );

    // Check for failures
    const failures = results.filter(r => r.status === 'rejected');
    if (failures.length > 0) {
      throw new Error(
        `${failures.length} parallel tasks failed:\n` +
        failures.map(f => f.reason).join('\n')
      );
    }

    // Merge successful results
    return this.mergeResults(
      parentContext,
      results.map(r => r.value)
    );
  }

  mergeResults(parent, childContexts) {
    return {
      ...parent,
      phase: 'parallel-complete',

      // Union of all modified files
      files_modified: [
        ...new Set(
          childContexts.flatMap(ctx => ctx.files_modified)
        )
      ],

      // Concatenate all decisions
      decisions: childContexts.flatMap(ctx => ctx.decisions),

      // Merge pending actions
      pending_actions: childContexts.flatMap(ctx =>
        ctx.pending_actions
      ),

      // Collect errors from all tasks
      error_log: childContexts.flatMap(ctx =>
        ctx.error_log || []
      ),

      // Track parallel execution
      parallel_execution: {
        tasks: childContexts.map(ctx => ({
          task_id: ctx.task_id,
          agent: ctx.current_agent,
          duration_ms: ctx.execution_time,
          status: 'completed'
        }))
      }
    };
  }
}
```

---

## Error Handling

### Pattern 1: Graceful Degradation

**Practice:**
```javascript
async function executeWithGracefulDegradation(agent, context) {
  try {
    // Attempt full execution
    return await agent.execute(context);

  } catch (error) {
    console.error(`Agent ${agent.name} failed:`, error);

    // Try to save partial progress
    const partialContext = {
      ...context,
      phase: `${context.phase}-failed`,
      error_log: [
        ...(context.error_log || []),
        {
          timestamp: new Date().toISOString(),
          agent: agent.name,
          error: error.message,
          stack: error.stack,
          context_at_failure: {
            phase: context.phase,
            files_modified: context.files_modified
          }
        }
      ]
    };

    // Save failure context
    await saveContext(partialContext);

    // Determine if recoverable
    if (error.code === 'RECOVERABLE') {
      // Suggest recovery action
      partialContext.pending_actions.unshift({
        action: 'recover_from_error',
        error_id: partialContext.error_log.length - 1,
        recovery_strategy: error.recoveryStrategy
      });

      return partialContext;
    }

    // Unrecoverable - rethrow
    throw error;
  }
}
```

---

### Pattern 2: Checkpoint-Based Rollback

**Practice:**
```javascript
class CheckpointManager {
  async createCheckpoint(context, label) {
    const checkpoint = {
      id: `checkpoint-${Date.now()}`,
      label: label,
      timestamp: new Date().toISOString(),
      context_snapshot: JSON.parse(JSON.stringify(context)),
      git_commit: execSync('git rev-parse HEAD').toString().trim()
    };

    // Save checkpoint
    const checkpointPath = `.claude/context/checkpoints/${context.workflow_id}/${checkpoint.id}.json`;
    await fs.promises.mkdir(path.dirname(checkpointPath), { recursive: true });
    await fs.promises.writeFile(
      checkpointPath,
      JSON.stringify(checkpoint, null, 2)
    );

    // Add to context
    context.checkpoints = context.checkpoints || [];
    context.checkpoints.push({
      id: checkpoint.id,
      label: label,
      timestamp: checkpoint.timestamp
    });

    return checkpoint.id;
  }

  async rollbackToCheckpoint(context, checkpointId) {
    // Load checkpoint
    const checkpointPath = `.claude/context/checkpoints/${context.workflow_id}/${checkpointId}.json`;
    const checkpoint = JSON.parse(
      await fs.promises.readFile(checkpointPath, 'utf-8')
    );

    // Restore code state
    if (checkpoint.git_commit) {
      execSync(`git reset --hard ${checkpoint.git_commit}`);
      console.log(`✅ Rolled back code to ${checkpoint.git_commit}`);
    }

    // Restore context state
    const restoredContext = checkpoint.context_snapshot;

    // Add rollback metadata
    restoredContext.rollback_history = restoredContext.rollback_history || [];
    restoredContext.rollback_history.push({
      timestamp: new Date().toISOString(),
      from_phase: context.phase,
      to_checkpoint: checkpointId,
      reason: 'manual_rollback'
    });

    return restoredContext;
  }
}

// Usage
const checkpointMgr = new CheckpointManager();

// Before risky operation
const checkpointId = await checkpointMgr.createCheckpoint(
  context,
  'before-database-migration'
);

try {
  await performDatabaseMigration();
} catch (error) {
  // Rollback on failure
  context = await checkpointMgr.rollbackToCheckpoint(context, checkpointId);
}
```

---

## Performance

### Optimization 1: Lazy Context Loading

**Practice:**
```typescript
interface ContextMetadata {
  version: string;
  workflow_id: string;
  phase: string;
  timestamp: string;
  current_agent: string;
}

class LazyWorkflowContext {
  private _metadata: ContextMetadata | null = null;
  private _fullContext: any = null;

  constructor(private contextPath: string) {}

  // Fast metadata access (doesn't load full context)
  async getMetadata(): Promise<ContextMetadata> {
    if (!this._metadata) {
      const json = await fs.promises.readFile(this.contextPath, 'utf-8');
      const context = JSON.parse(json);

      this._metadata = {
        version: context.version,
        workflow_id: context.workflow_id,
        phase: context.phase,
        timestamp: context.timestamp,
        current_agent: context.current_agent
      };
    }

    return this._metadata;
  }

  // Load full context only when needed
  async getFullContext() {
    if (!this._fullContext) {
      const json = await fs.promises.readFile(this.contextPath, 'utf-8');
      this._fullContext = JSON.parse(json);
    }

    return this._fullContext;
  }

  // Access specific fields without full load
  async getField<T>(fieldName: string): Promise<T> {
    const metadata = await this.getMetadata();
    if (fieldName in metadata) {
      return (metadata as any)[fieldName];
    }

    // Need full context for this field
    const full = await this.getFullContext();
    return full[fieldName];
  }
}

// Usage - very fast for metadata-only operations
const ctx = new LazyWorkflowContext('.claude/context/workflow-123.json');
const phase = await ctx.getMetadata();  // Fast - only loads 5 fields
console.log(phase.phase);  // 'implementation-complete'

// Only load full context when actually needed
if (needFullHistory) {
  const full = await ctx.getFullContext();  // Slower
  processHistory(full.conversation_history);
}
```

---

### Optimization 2: Incremental Updates

**Practice:**
```javascript
class IncrementalContextManager {
  async updateContextField(workflowId, fieldName, value) {
    const contextPath = `.claude/context/${workflowId}.json`;

    // Read current context
    const json = await fs.promises.readFile(contextPath, 'utf-8');
    const context = JSON.parse(json);

    // Update only changed field
    context[fieldName] = value;
    context.timestamp = new Date().toISOString();

    // Atomic write
    const tempPath = `${contextPath}.tmp`;
    await fs.promises.writeFile(tempPath, JSON.stringify(context, null, 2));
    await fs.promises.rename(tempPath, contextPath);
  }

  async appendToArrayField(workflowId, fieldName, item) {
    const contextPath = `.claude/context/${workflowId}.json`;
    const json = await fs.promises.readFile(contextPath, 'utf-8');
    const context = JSON.parse(json);

    // Append to array
    if (!Array.isArray(context[fieldName])) {
      context[fieldName] = [];
    }
    context[fieldName].push(item);
    context.timestamp = new Date().toISOString();

    // Save
    const tempPath = `${contextPath}.tmp`;
    await fs.promises.writeFile(tempPath, JSON.stringify(context, null, 2));
    await fs.promises.rename(tempPath, contextPath);
  }
}

// Usage - faster than loading/saving entire context
const mgr = new IncrementalContextManager();

await mgr.updateContextField('workflow-123', 'phase', 'testing-complete');

await mgr.appendToArrayField('workflow-123', 'decisions',
  'Use Playwright for E2E tests'
);
```

---

## Security

### Practice 1: No Secrets in Context

**Rule:** Never save API keys, passwords, tokens, or sensitive data in context.

**Implementation:**
```javascript
// ❌ BAD: Secrets in context
const context = {
  workflow_id: 'deploy-prod',
  database_url: 'postgresql://user:password@host:5432/db',  // LEAKED!
  api_key: 'sk_live_abc123...',  // LEAKED!
  aws_secret: 'wJalrXUtnFEMI/K7MDENG...'  // LEAKED!
};

// ✅ GOOD: Reference secrets by ID
const context = {
  workflow_id: 'deploy-prod',
  secrets: {
    database_url: { ref: 'env:DATABASE_URL' },
    api_key: { ref: 'doppler:STRIPE_API_KEY' },
    aws_secret: { ref: 'vault:aws/secret_key' }
  }
};

// Agent resolves secrets at runtime
function resolveSecrets(context) {
  return Object.entries(context.secrets || {}).reduce((acc, [key, value]) => {
    const [provider, secretId] = value.ref.split(':');

    switch (provider) {
      case 'env':
        acc[key] = process.env[secretId];
        break;
      case 'doppler':
        acc[key] = fetchFromDoppler(secretId);
        break;
      case 'vault':
        acc[key] = fetchFromVault(secretId);
        break;
    }

    return acc;
  }, {});
}
```

---

### Practice 2: Context Access Control

**Implementation:**
```javascript
class SecureContextManager {
  constructor(workflowId, userId) {
    this.workflowId = workflowId;
    this.userId = userId;
  }

  async saveContext(context) {
    // Check write permission
    if (!await this.canWrite(this.userId, this.workflowId)) {
      throw new Error('Permission denied: cannot save context');
    }

    // Sanitize before saving
    const sanitized = this.sanitizeContext(context);

    // Save with restricted permissions
    const contextPath = this.getContextPath();
    await fs.promises.writeFile(
      contextPath,
      JSON.stringify(sanitized, null, 2),
      { mode: 0o600 }  // Owner read/write only
    );

    // Log access
    await this.logAccess('write', contextPath);
  }

  async loadContext() {
    // Check read permission
    if (!await this.canRead(this.userId, this.workflowId)) {
      throw new Error('Permission denied: cannot read context');
    }

    const contextPath = this.getContextPath();
    const json = await fs.promises.readFile(contextPath, 'utf-8');

    // Log access
    await this.logAccess('read', contextPath);

    return JSON.parse(json);
  }

  sanitizeContext(context) {
    // Remove sensitive fields
    const { password, token, secret, ...safe } = context;

    // Redact sensitive patterns
    const sanitized = JSON.stringify(safe);
    const redacted = sanitized
      .replace(/sk_live_[a-zA-Z0-9]+/g, 'sk_live_REDACTED')
      .replace(/password":\s*"[^"]+"/g, 'password": "REDACTED"');

    return JSON.parse(redacted);
  }
}
```

---

## Testing

### Practice 1: Context Validation Tests

**Implementation:**
```typescript
import { describe, test, expect } from 'vitest';

describe('Context Validation', () => {
  test('should have all required fields', () => {
    const context = createTestContext();

    expect(context).toHaveProperty('version');
    expect(context).toHaveProperty('workflow_id');
    expect(context).toHaveProperty('timestamp');
    expect(context).toHaveProperty('current_agent');
    expect(context).toHaveProperty('phase');
  });

  test('should have valid timestamp format', () => {
    const context = createTestContext();

    // Should be ISO 8601
    expect(() => {
      new Date(context.timestamp);
    }).not.toThrow();

    // Should be recent (within 1 hour)
    const timestamp = new Date(context.timestamp);
    const now = new Date();
    const diffMs = now.getTime() - timestamp.getTime();
    expect(diffMs).toBeLessThan(3600000);  // 1 hour
  });

  test('should not contain secrets', () => {
    const context = createTestContext();
    const json = JSON.stringify(context);

    // Check for common secret patterns
    expect(json).not.toMatch(/sk_live_[a-zA-Z0-9]+/);  // Stripe
    expect(json).not.toMatch(/password/i);
    expect(json).not.toMatch(/api[_-]?key/i);
  });

  test('should be under size limit', () => {
    const context = createTestContext();
    const size = JSON.stringify(context).length;

    expect(size).toBeLessThan(500 * 1024);  // 500KB
  });
});
```

---

### Practice 2: Workflow Integration Tests

**Implementation:**
```typescript
describe('Workflow Integration', () => {
  test('should complete sequential workflow', async () => {
    const workflow = new WorkflowOrchestrator();

    const agents = [
      new DesignAgent(),
      new ImplementAgent(),
      new TestAgent(),
      new DeployAgent()
    ];

    const result = await workflow.executeSequential(agents);

    expect(result.phase).toBe('deployed');
    expect(result.files_modified.length).toBeGreaterThan(0);
    expect(result.decisions.length).toBeGreaterThan(0);
  });

  test('should handle agent failure gracefully', async () => {
    const workflow = new WorkflowOrchestrator();

    const agents = [
      new DesignAgent(),
      new FailingAgent(),  // Will throw error
      new TestAgent()
    ];

    await expect(
      workflow.executeSequential(agents)
    ).rejects.toThrow();

    // Context should be saved up to failure point
    const context = await loadContext(workflow.workflowId);
    expect(context.phase).toBe('design-complete');
    expect(context.error_log).toHaveLength(1);
  });
});
```

---

## Quick Reference

**Context Design:**
- ✅ Keep contexts <100KB
- ✅ Be explicit, avoid assumptions
- ✅ Version your schema
- ❌ Don't embed large files
- ❌ Don't include secrets

**Handoff Patterns:**
- Sequential: Clean, linear progression
- Parallel: Concurrent tasks with merge
- Conditional: Route based on results

**Error Handling:**
- Save partial progress
- Create checkpoints before risky operations
- Implement rollback strategies

**Performance:**
- Use lazy loading for metadata
- Implement incremental updates
- Cache frequently accessed contexts

**Security:**
- Never save secrets in context
- Use secret references instead
- Implement access control
- Sanitize before saving

**Testing:**
- Validate required fields
- Check for secrets
- Verify size limits
- Test workflow integration

---

**Best Practices Version**: 1.0
**Last Updated**: 2025-01-15
