# Full-Stack Feature Development Workflow

**Purpose**: Complete feature development from requirements to deployment with coordinated frontend, backend, and database work.

**When to Use**: Building new features that span multiple layers of the stack.

**Duration**: 1-3 days for small features, 1-2 weeks for complex features

**Agents Involved**: 5-7 agents orchestrated in phases

---

## Prerequisites

- [ ] Feature requirements defined in Linear issue
- [ ] Design mockups available (if UI changes)
- [ ] Database schema changes identified (if needed)
- [ ] API contract discussed with team

## Phase 1: Planning & Design (Sequential)

### Step 1.1: Requirements Analysis
**Agent**: `business-analyst` or manual review
**Input**: Linear issue with feature description
**Output**: Detailed requirements document

```
Analyze the feature requirements and create:
- User stories with acceptance criteria
- Technical requirements
- API contract definition (if new endpoints)
- Database schema changes (if needed)
- Success metrics
```

### Step 1.2: Architecture Design
**Agent**: `docs-architect` (Opus)
**Input**: Requirements document from Step 1.1
**Output**: Architecture design document

```
Design the technical architecture:
- Component interaction diagram (Mermaid)
- API endpoint definitions (OpenAPI)
- Database schema changes (migration plan)
- Frontend component structure
- State management approach
```

**Validation Criteria**:
- [ ] All components identified
- [ ] Data flow documented
- [ ] API contract complete
- [ ] Team review completed

## Phase 2: Database & Backend (Sequential)

### Step 2.1: Database Migration (If Needed)
**Agent**: `data-validator` or manual SQL
**Input**: Schema design from Phase 1
**Output**: PlanetScale migration

```bash
# Create PlanetScale branch
pscale branch create <database> feature/<branch-name>

# Write migration
# File: migrations/YYYYMMDD_feature_name.sql

# Apply migration
pscale migrate create <database> feature/<branch-name> --migration-file migrations/YYYYMMDD_feature_name.sql

# Test migration
pscale shell <database> feature/<branch-name>
```

**Validation Criteria**:
- [ ] Migration tested on branch
- [ ] Rollback plan documented
- [ ] Indexes added for performance
- [ ] Data validation checks pass

### Step 2.2: Backend API Implementation
**Agent**: `tdd-python` or `tdd-typescript` (TDD approach)
**Input**: API contract from Phase 1
**Output**: Implemented API endpoints with tests

**For Cloudflare Workers + Hono**:
```typescript
// 1. Write failing test first
describe('POST /api/features', () => {
  it('creates a new feature', async () => {
    const response = await app.request('/api/features', {
      method: 'POST',
      body: JSON.stringify({ name: 'Feature' }),
      headers: { 'Content-Type': 'application/json' }
    });
    expect(response.status).toBe(201);
  });
});

// 2. Implement minimal code to pass
app.post('/api/features', async (c) => {
  const body = await c.req.json();
  // Implementation
  return c.json({ id: 'feat_123', ...body }, 201);
});

// 3. Refactor for quality
```

**For Python + FastAPI**:
```python
# 1. Write failing test
def test_create_feature():
    response = client.post("/api/features", json={"name": "Feature"})
    assert response.status_code == 201

# 2. Implement
@app.post("/api/features", status_code=201)
async def create_feature(feature: FeatureCreate):
    return await feature_service.create(feature)

# 3. Refactor
```

**Validation Criteria**:
- [ ] All tests passing (minimum 80% coverage)
- [ ] API contract matches OpenAPI spec
- [ ] Error handling implemented
- [ ] Input validation with Pydantic/Zod
- [ ] Code review completed

## Phase 3: Frontend Implementation (Parallel with Backend)

### Step 3.1: Component Development
**Agent**: `react-tanstack-tester` or `project-scaffolder`
**Input**: Design mockups and API contract
**Output**: React components with tests

```typescript
// 1. Generate component scaffold
/project-scaffolder --type react-component --name FeatureList

// 2. Implement with TanStack Query
import { useQuery } from '@tanstack/react-query';

export function FeatureList() {
  const { data, isLoading } = useQuery({
    queryKey: ['features'],
    queryFn: () => fetch('/api/features').then(r => r.json())
  });

  if (isLoading) return <Spinner />;

  return (
    <ul>
      {data.map(feature => (
        <FeatureCard key={feature.id} feature={feature} />
      ))}
    </ul>
  );
}

// 3. Write tests
describe('FeatureList', () => {
  it('renders features from API', async () => {
    render(<FeatureList />);
    await waitFor(() => {
      expect(screen.getByText('Feature 1')).toBeInTheDocument();
    });
  });
});
```

**Validation Criteria**:
- [ ] Component tests passing
- [ ] Responsive design implemented
- [ ] Accessibility (ARIA) labels added
- [ ] Loading and error states handled
- [ ] Storybook story created (if applicable)

### Step 3.2: State Management Integration
**Agent**: Manual or `code-quality-analyzer` for review
**Input**: Components from Step 3.1
**Output**: Integrated state management

```typescript
// TanStack Query for server state
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

// Zustand for client state (if needed)
import { create } from 'zustand';

interface FeatureStore {
  selectedFeature: string | null;
  setSelectedFeature: (id: string | null) => void;
}

const useFeatureStore = create<FeatureStore>((set) => ({
  selectedFeature: null,
  setSelectedFeature: (id) => set({ selectedFeature: id })
}));
```

**Validation Criteria**:
- [ ] Server state managed by TanStack Query
- [ ] Client state minimal and necessary
- [ ] No prop drilling
- [ ] Performance optimized (memoization where needed)

## Phase 4: Integration & Testing (Sequential)

### Step 4.1: Integration Testing
**Agent**: `test-generator` + manual E2E tests
**Input**: Completed frontend and backend
**Output**: E2E tests with Playwright

```typescript
// test/e2e/feature.spec.ts
import { test, expect } from '@playwright/test';

test('create feature end-to-end', async ({ page }) => {
  // Navigate to feature page
  await page.goto('/features');

  // Click create button
  await page.click('[data-testid="create-feature-btn"]');

  // Fill form
  await page.fill('[name="name"]', 'New Feature');
  await page.fill('[name="description"]', 'Feature description');

  // Submit
  await page.click('[type="submit"]');

  // Verify creation
  await expect(page.locator('text=New Feature')).toBeVisible();
});
```

**Validation Criteria**:
- [ ] E2E tests pass locally
- [ ] E2E tests pass in CI
- [ ] Critical user flows tested
- [ ] Error scenarios tested

### Step 4.2: API Documentation Update
**Agent**: `docs-architect`
**Input**: Implemented APIs
**Output**: Updated OpenAPI spec and documentation

```bash
# Generate API documentation
/doc-generate-api --format openapi --deploy cloudflare-pages

# Validate coverage
/doc-coverage --scope api --threshold 90
```

**Validation Criteria**:
- [ ] OpenAPI spec updated
- [ ] Code examples added
- [ ] Interactive docs deployed
- [ ] API documentation coverage > 90%

## Phase 5: Code Quality & Security (Parallel)

### Step 5.1: Code Quality Review
**Agent**: `code-quality-analyzer`
**Input**: All feature code
**Output**: Quality report with refactoring suggestions

```bash
/quality-pipeline --scope "src/features/new-feature/**"
```

**Checks**:
- [ ] No code smells detected
- [ ] Complexity metrics acceptable
- [ ] DRY principles followed
- [ ] Proper error handling
- [ ] Logging added for debugging

### Step 5.2: Security Scan
**Agent**: `security-analyzer` (Opus)
**Input**: Feature code and dependencies
**Output**: Security audit report

```bash
/security-scan --depth comprehensive --area "src/features/new-feature"
```

**Checks**:
- [ ] No SQL injection vulnerabilities
- [ ] Input sanitization implemented
- [ ] Authentication/authorization enforced
- [ ] No sensitive data in logs
- [ ] Dependencies up to date

## Phase 6: Deployment (Sequential)

### Step 6.1: Staging Deployment
**Agent**: Manual or deployment automation
**Input**: Merged feature branch
**Output**: Feature deployed to staging

```bash
# Deploy backend (Cloudflare Workers)
cd backend
wrangler deploy --env staging

# Deploy frontend (Cloudflare Pages)
cd frontend
pnpm run build
wrangler pages deploy dist --project-name app-staging

# Deploy database migration (PlanetScale)
pscale deploy-request create <database> feature/<branch-name>
pscale deploy-request deploy <database> <DR-number>
```

**Validation Criteria**:
- [ ] Feature accessible on staging
- [ ] Database migration applied successfully
- [ ] Monitoring shows no errors
- [ ] Manual QA testing completed

### Step 6.2: Production Deployment
**Agent**: Manual with monitoring
**Input**: Validated staging deployment
**Output**: Feature live in production

```bash
# Production deployment (with gradual rollout)
wrangler deploy --env production

# Monitor deployment
/monitor-deployment --service api --duration 30m
```

**Validation Criteria**:
- [ ] Production deployment successful
- [ ] No increase in error rates
- [ ] Performance metrics acceptable
- [ ] User feedback positive

## Phase 7: Post-Deployment (Sequential)

### Step 7.1: Monitor & Observe
**Agent**: `observability-engineer`
**Input**: Production deployment
**Output**: Monitoring dashboard and alerts

```bash
# Set up monitoring
/monitor-setup --service new-feature --metrics "requests,errors,latency"

# Implement SLOs
/slo-implement --service new-feature --availability 99.9
```

**Validation Criteria**:
- [ ] Metrics dashboard created
- [ ] Alerts configured
- [ ] SLOs defined and tracked
- [ ] Error budget calculated

### Step 7.2: Documentation & Handoff
**Agent**: `docs-architect` + `onboarding-coordinator`
**Input**: Completed feature
**Output**: Documentation and team notification

**Documentation to Create**:
- [ ] User-facing documentation
- [ ] Technical documentation (architecture, decisions)
- [ ] Runbook for operations
- [ ] Linear issue marked as complete

**Team Notification**:
```markdown
# Feature Deployed: [Feature Name]

## What Changed
- New API endpoints: POST /api/features, GET /api/features/:id
- New UI components in /features route
- Database: Added features table

## Documentation
- API Docs: https://docs.greyhaven.com/api/features
- User Guide: https://docs.greyhaven.com/guides/features
- Runbook: https://docs.greyhaven.com/runbooks/features

## Monitoring
- Dashboard: https://grafana.greyhaven.com/d/features
- SLO: 99.9% availability (21.6min/month error budget)

## Team Impact
- Frontend team: New components available in /src/features
- Backend team: New service in /services/features
- QA team: E2E tests in /test/e2e/features
```

---

## Success Criteria

**Feature is considered complete when**:
- [ ] All tests passing (unit, integration, E2E)
- [ ] Code coverage > 80%
- [ ] Security scan clean
- [ ] API documentation complete
- [ ] Deployed to production
- [ ] Monitoring and alerts configured
- [ ] Team notified and documentation complete

## Rollback Plan

If issues occur in production:

```bash
# 1. Rollback Cloudflare Workers deployment
wrangler rollback --env production

# 2. Rollback database migration (if needed)
pscale branch delete <database> feature/<branch-name>

# 3. Notify team
# Post in Slack #incidents channel

# 4. Create incident postmortem
/incident-response --create-postmortem
```

## Metrics to Track

- **Development Velocity**: Time from start to production
- **Code Quality**: Test coverage, complexity, code review findings
- **Deployment Success**: Deployment frequency, success rate, rollback rate
- **Feature Health**: Error rate, latency, user adoption
- **Team Collaboration**: PR review time, blocker resolution time

---

## Template Usage

To use this workflow template:

1. **Create Linear Issue**: Define feature requirements
2. **Clone Template**: Copy this workflow and customize
3. **Execute Phases**: Follow phases sequentially or as marked parallel
4. **Track Progress**: Update checkboxes as you complete steps
5. **Document Decisions**: Add ADRs for significant architectural choices
6. **Review & Iterate**: Conduct retrospective after feature completion

## Customization Notes

**For simpler features**:
- Skip Phase 1.2 (Architecture Design) if straightforward
- Combine Phases 2 and 3 if single developer
- Reduce E2E testing scope

**For complex features**:
- Add spike/prototype phase before Phase 1
- Break into multiple sub-features with separate workflows
- Add performance testing phase
- Include load testing before production

**For urgent fixes**:
- Use simplified version with Phase 2 (Backend) and Phase 6 (Deployment) only
- Ensure tests and documentation added post-deployment
