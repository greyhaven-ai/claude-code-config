# Feature Development Handoff Example

Complete multi-agent workflow for feature development with context handoffs.

**Workflow**: Design → Implement → Test → Deploy
**Duration**: 4-6 hours
**Agents**: 4 (backend-architect, tdd-typescript, test-generator, devops-troubleshooter)
**Context Handoffs**: 3

---

## Workflow Overview

```
User Request → Backend Architect → TDD TypeScript → Test Generator → DevOps Deploy
                    ↓ save              ↓ save           ↓ save          ↓
                 context-1           context-2        context-3        ✅ Complete
```

---

## Phase 1: Architecture Design

**Agent**: `backend-architect`
**Goal**: Design API endpoints and data model

**User Input**:
"Add user preferences feature: users can save theme (light/dark), language (en/es/fr), and notification settings (email, push)."

**Agent Work**:
1. Analyzes requirements
2. Designs database schema
3. Plans API endpoints
4. Creates OpenAPI spec

**Output**:
```typescript
// Designed schema
interface UserPreferences {
  user_id: string;
  theme: 'light' | 'dark';
  language: 'en' | 'es' | 'fr';
  notifications: {
    email: boolean;
    push: boolean;
  };
  updated_at: Date;
}

// Planned endpoints
GET    /api/v1/users/:id/preferences
PUT    /api/v1/users/:id/preferences
PATCH  /api/v1/users/:id/preferences
```

**Decisions Made**:
- Use JSONB column in PostgreSQL for preferences (flexibility)
- PUT for full replace, PATCH for partial update
- Include updated_at for conflict resolution
- Rate limit: 10 requests/minute per user

**Context Save** (`context-001-design.json`):
```json
{
  "version": "1.0",
  "workflow_id": "feature-user-prefs-20250115",
  "timestamp": "2025-01-15T10:30:00Z",
  "current_agent": "backend-architect",
  "next_agent": "tdd-typescript",
  "phase": "design-complete",

  "files_modified": [
    "docs/api/user-preferences.md",
    "docs/architecture/decisions/adr-012-user-prefs-storage.md"
  ],

  "decisions": [
    "Use JSONB for flexibility in preferences structure",
    "Implement both PUT (full) and PATCH (partial) updates",
    "Rate limit to 10 req/min per user to prevent abuse",
    "Include updated_at for optimistic locking"
  ],

  "data_model": {
    "table": "user_preferences",
    "columns": {
      "id": "UUID PRIMARY KEY",
      "user_id": "UUID REFERENCES users(id)",
      "preferences": "JSONB NOT NULL",
      "created_at": "TIMESTAMP DEFAULT NOW()",
      "updated_at": "TIMESTAMP DEFAULT NOW()"
    },
    "indexes": [
      "user_id (unique)",
      "updated_at"
    ]
  },

  "api_spec": {
    "endpoints": [
      {
        "method": "GET",
        "path": "/api/v1/users/:id/preferences",
        "auth_required": true,
        "rate_limit": "10/minute",
        "response": "UserPreferences"
      },
      {
        "method": "PUT",
        "path": "/api/v1/users/:id/preferences",
        "auth_required": true,
        "body": "UserPreferencesUpdate",
        "response": "UserPreferences"
      },
      {
        "method": "PATCH",
        "path": "/api/v1/users/:id/preferences",
        "auth_required": true,
        "body": "Partial<UserPreferencesUpdate>",
        "response": "UserPreferences"
      }
    ]
  },

  "pending_actions": [
    "Implement API endpoints with TDD approach",
    "Create database migration",
    "Add validation for preference values",
    "Implement rate limiting middleware"
  ],

  "constraints": [
    "Must maintain backward compatibility",
    "Performance: GET should be < 50ms",
    "Must handle concurrent updates (optimistic locking)"
  ]
}
```

**Handoff Message**:
"Design complete. Data model uses JSONB for flexibility. Three endpoints designed (GET/PUT/PATCH). Ready for TDD implementation. Key constraints: < 50ms response, handle concurrency, rate limiting."

---

## Phase 2: TDD Implementation

**Agent**: `tdd-typescript-implementer`
**Goal**: Implement API endpoints following TDD

**Context Restore**:
```typescript
// Agent loads context-001-design.json
const context = await loadContext('feature-user-prefs-20250115');

console.log('Previous agent:', context.current_agent);
console.log('Decisions:', context.decisions);
console.log('Next steps:', context.pending_actions);
console.log('Constraints:', context.constraints);
```

**Agent Work**:
Following RED-GREEN-REFACTOR cycle:

**Cycle 1**: GET /preferences endpoint
```typescript
// RED: Write failing test
describe('GET /api/v1/users/:id/preferences', () => {
  it('returns user preferences', async () => {
    const response = await request(app)
      .get('/api/v1/users/user-123/preferences')
      .set('Authorization', 'Bearer token');

    expect(response.status).toBe(200);
    expect(response.body).toMatchObject({
      user_id: 'user-123',
      theme: 'light',
      language: 'en'
    });
  });
});
// ❌ Test fails - endpoint doesn't exist

// GREEN: Minimal implementation
router.get('/users/:id/preferences', authenticate, async (req, res) => {
  const prefs = await db.getUserPreferences(req.params.id);
  res.json(prefs);
});
// ✅ Test passes

// REFACTOR: Add caching, validation
router.get('/users/:id/preferences',
  authenticate,
  validateUserId,
  cacheMiddleware({ ttl: 300 }),
  async (req, res) => {
    const prefs = await db.getUserPreferences(req.params.id);
    res.json(prefs);
  }
);
// ✅ All tests still pass
```

**Cycle 2-4**: PUT and PATCH endpoints (similar process)

**Context Save** (`context-002-implementation.json`):
```json
{
  "version": "1.0",
  "workflow_id": "feature-user-prefs-20250115",
  "timestamp": "2025-01-15T14:45:00Z",
  "current_agent": "tdd-typescript",
  "next_agent": "test-generator",
  "phase": "implementation-complete",

  "files_modified": [
    "src/api/routes/user-preferences.ts",
    "src/api/middleware/rate-limit.ts",
    "src/db/repositories/preferences.ts",
    "src/types/user-preferences.ts",
    "migrations/2025-01-15-user-preferences.sql"
  ],

  "test_results": {
    "total": 18,
    "passing": 18,
    "failing": 0,
    "coverage": {
      "line": 96,
      "branch": 94,
      "function": 100
    }
  },

  "decisions": [
    "Added caching (5min TTL) for GET endpoint",
    "Implemented optimistic locking with updated_at",
    "Used Zod for runtime validation",
    "Rate limiting uses Redis for distributed systems"
  ],

  "pending_actions": [
    "Generate comprehensive integration tests",
    "Add E2E tests for full user flows",
    "Test edge cases (concurrent updates, invalid data)",
    "Performance testing under load"
  ],

  "metrics": {
    "implementation_time": "3.5 hours",
    "test_count": 18,
    "code_loc": 420,
    "test_loc": 580
  }
}
```

**Handoff Message**:
"Implementation complete with 18 passing tests, 96% coverage. All three endpoints functional. Caching, validation, rate limiting implemented. Ready for comprehensive testing."

---

## Phase 3: Test Generation

**Agent**: `test-generator`
**Goal**: Create comprehensive test suite

**Context Restore**:
```typescript
const context = await loadContext('feature-user-prefs-20250115');
const implementedFiles = context.files_modified;
const coverageGaps = identifyGaps(context.test_results.coverage);
```

**Agent Work**:
1. Analyzes implementation
2. Identifies uncovered branches
3. Generates integration tests
4. Creates E2E test scenarios

**Generated Tests**:

**Integration Test**:
```typescript
describe('User Preferences Integration', () => {
  it('handles concurrent updates correctly', async () => {
    const userId = 'user-123';

    // Simulate two clients updating simultaneously
    const [update1, update2] = await Promise.allSettled([
      api.updatePreferences(userId, { theme: 'dark' }),
      api.updatePreferences(userId, { language: 'es' })
    ]);

    // One should succeed, one should get conflict (409)
    const statuses = [update1.status, update2.status].sort();
    expect(statuses).toEqual([200, 409]);

    // Final state should be consistent
    const final = await api.getPreferences(userId);
    expect(final.theme === 'dark' || final.language === 'es').toBe(true);
  });

  it('respects rate limits', async () => {
    const requests = Array(15).fill(null).map(() =>
      api.updatePreferences('user-123', { theme: 'dark' })
    );

    const results = await Promise.allSettled(requests);
    const rateLimited = results.filter(r => r.status === 429);

    expect(rateLimited.length).toBeGreaterThan(0); // Some rejected
  });
});
```

**Context Save** (`context-003-testing.json`):
```json
{
  "version": "1.0",
  "workflow_id": "feature-user-prefs-20250115",
  "timestamp": "2025-01-15T16:30:00Z",
  "current_agent": "test-generator",
  "next_agent": "devops-troubleshooter",
  "phase": "testing-complete",

  "files_modified": [
    "tests/integration/user-preferences.test.ts",
    "tests/e2e/preferences-flow.test.ts",
    "tests/performance/preferences-load.test.ts"
  ],

  "test_results": {
    "unit": { "total": 18, "passing": 18 },
    "integration": { "total": 12, "passing": 12 },
    "e2e": { "total": 5, "passing": 5 },
    "performance": {
      "avg_response_time": "42ms",
      "p95_response_time": "68ms",
      "p99_response_time": "95ms",
      "throughput": "450 req/sec"
    }
  },

  "final_coverage": {
    "line": 98,
    "branch": 97,
    "function": 100
  },

  "pending_actions": [
    "Deploy to staging environment",
    "Run smoke tests in staging",
    "Monitor error rates and performance",
    "Deploy to production with canary"
  ],

  "quality_gates_passed": {
    "coverage": true,
    "performance": true,
    "security": true,
    "accessibility": true
  }
}
```

**Handoff Message**:
"Testing complete. 35 tests total, all passing. 98% coverage. Performance within targets (< 50ms avg). Ready for deployment."

---

## Phase 4: Deployment

**Agent**: `devops-troubleshooter`
**Goal**: Deploy to staging and production

**Context Restore**:
```typescript
const context = await loadContext('feature-user-prefs-20250115');
const performanceMetrics = context.test_results.performance;
const qualityGates = context.quality_gates_passed;

// Verify all gates passed
if (!Object.values(qualityGates).every(passed => passed)) {
  throw new Error('Quality gates not met - cannot deploy');
}
```

**Agent Work**:
1. Creates deployment pipeline
2. Deploys to staging
3. Runs smoke tests
4. Deploys to production (canary)
5. Monitors rollout

**Deployment Steps**:
```yaml
# .github/workflows/deploy-user-prefs.yml
name: Deploy User Preferences Feature

on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Environment'
        required: true
        type: choice
        options:
          - staging
          - production

jobs:
  deploy:
    steps:
      - name: Run tests
        run: npm test

      - name: Check coverage
        run: npm run coverage -- --threshold=95

      - name: Deploy to staging
        if: inputs.environment == 'staging'
        run: |
          npx wrangler deploy --env staging
          npm run smoke-test:staging

      - name: Deploy to production (canary)
        if: inputs.environment == 'production'
        run: |
          npx wrangler deploy --env production --percentage 10
          npm run monitor:canary

      - name: Full rollout
        if: inputs.environment == 'production'
        run: npx wrangler deploy --env production --percentage 100
```

**Final Context** (`context-004-complete.json`):
```json
{
  "version": "1.0",
  "workflow_id": "feature-user-prefs-20250115",
  "timestamp": "2025-01-15T18:00:00Z",
  "current_agent": "devops-troubleshooter",
  "next_agent": null,
  "phase": "deployed",

  "deployment": {
    "staging": {
      "deployed_at": "2025-01-15T17:15:00Z",
      "smoke_tests": "passed",
      "url": "https://staging.example.com"
    },
    "production": {
      "canary_started": "2025-01-15T17:45:00Z",
      "canary_percentage": 10,
      "full_rollout": "2025-01-15T17:55:00Z",
      "url": "https://api.example.com"
    }
  },

  "monitoring": {
    "error_rate": "0.02%",
    "avg_latency": "38ms",
    "p99_latency": "89ms",
    "requests_served": 12500
  },

  "status": "complete",
  "total_duration": "7.5 hours",
  "agents_involved": 4,
  "context_handoffs": 3
}
```

---

## Lessons Learned

**What Went Well**:
- Clear context handoffs prevented re-work
- Performance targets met from design phase
- TDD approach caught issues early
- Automated deployment smooth

**Improvements for Next Time**:
- Could have parallelized testing and deployment prep
- Context size grew large - could compress history
- Should add rollback procedure to context

**Metrics**:
- **Time saved** vs starting fresh each phase: ~40%
- **Context restore success**: 100%
- **Quality maintained** across all handoffs: Yes

---

**Total Workflow Time**: 7.5 hours
**Agents Involved**: 4
**Context Saves**: 4
**Handoff Success Rate**: 100%
**Final Quality**: Production-ready
