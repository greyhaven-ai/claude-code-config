# Example: Senior Engineer Fast-Track Onboarding

Fast-track onboarding focused on architecture understanding and early technical leadership.

## Context

**New Hire**: Jordan Kim - Senior Backend Engineer
**Background**: 8 years experience, 3 years as tech lead, ex-Stripe
**Start Date**: March 1, 2024
**Team**: Backend (6 engineers: 3 senior, 2 mid, 1 junior)
**Focus**: Architecture, technical leadership, mentoring

**Key Differences from Junior Onboarding**:
- Skip basics (assumes experience with Git, PRs, etc.)
- Focus on architecture and system design
- Earlier technical leadership opportunities
- Compressed timeline (productivity Week 2 vs Week 8)
- Peer mentorship (not buddy system)

## Pre-Boarding: Architecture Immersion

### Pre-Start Reading Materials

```markdown
# Jordan Kim - Pre-Boarding Package

Welcome! Since you're joining as Senior Engineer, we've prepared
architecture-focused materials to accelerate your ramp-up.

## Must-Read (Before Day 1)
- Architecture Decision Records (ADRs) - all 23 decisions
- System architecture diagrams (Mermaid)
- Database schema and multi-tenant design
- API design standards
- Performance SLOs and monitoring strategy

## Nice-to-Have
- Recent postmortems (last 6 months)
- Technical roadmap (next 6 months)
- Team RFC process documentation

## Your First Week
We'll focus on architecture understanding, not basic setup.
You'll present your architectural observations to the team
and lead your first design review in Week 2.

Questions before you start? Reply to this email.
```

**Jordan's Pre-Start Questions**:
- "What are the biggest architectural challenges right now?" (Answer: Multi-tenancy scaling, query performance)
- "How do you handle database migrations in production?" (Answer: Automated with rollback, documented in runbooks)
- "What's the incident response process?" (Answer: On-call rotation, runbooks, blameless postmortems)

## Day 1: Strategic Onboarding

### Morning: Executive Context (9:00 AM)

**CTO 30-Min Session**:
```markdown
# CTO Session: Jordan Kim Onboarding

## Business Context
- Current: 500 customers, 50K daily active users
- Next 12 months: 5K customers target (10x growth)
- Key challenge: Multi-tenant scaling
- Revenue model: B2B SaaS ($100-$10K/month tiers)

## Technical Strategy
- Edge-first architecture (Cloudflare Workers)
- PostgreSQL with row-level security (PlanetScale)
- React frontends (TanStack ecosystem)
- Focus: Performance, reliability, developer experience

## Your Role
- Technical leadership on backend team
- Architecture input (you'll join architecture review board)
- Mentoring mid/junior engineers
- Own critical systems (auth, billing, core API)

## First 30 Days
- Understand current architecture deeply
- Identify 2-3 improvements (quick wins)
- Lead first design review (Week 3)
- Join on-call rotation (Week 4)
```

### Manager 1:1: Technical Deep Dive (10:00 AM)

**Engineering Manager Session**:
```markdown
# Technical Onboarding: Senior Engineer

## Architecture Tour
- Multi-tenant isolation strategy (RLS policies)
- Authentication flow (JWT + refresh tokens)
- API gateway pattern (Cloudflare Workers)
- Data layer (PostgreSQL + Redis caching)
- Observability (Prometheus + Grafana + DataDog)

## Current Pain Points
1. Query performance degradation (N+1 issues)
2. Database connection pooling limits
3. Multi-tenant data isolation verification
4. Deployment rollback speed (currently 15 min)
5. Observability gaps in edge layer

## Your First Technical Tasks
- Week 1: Architectural analysis and recommendations
- Week 2: Design doc for query optimization
- Week 3: Lead design review for new feature
- Week 4: Implement one architectural improvement

## Peer Network
- Sarah (Senior Frontend): Component architecture expert
- Marcus (Senior Backend): Original architect, 4 years here
- Lisa (Staff Engineer): System design, mentorship
```

### Afternoon: Architecture Deep Dive with Staff Engineer

**Whiteboarding Session with Lisa (Staff Engineer)**:
```markdown
# Architecture Walkthrough

## System Components
[Mermaid diagram on whiteboard]

Client → Cloudflare Workers (Auth + Gateway)
       → FastAPI Backend
       → PostgreSQL (RLS) + Redis Cache
       → External APIs (Stripe, SendGrid)

## Multi-Tenancy Design
- Tenant ID in JWT claims
- RLS policies on all tables
- Connection pooling per tenant (limited to 100)
- Data isolation verified in tests

## Scalability Bottlenecks (Your Focus Areas)
1. **Query Performance**: Some endpoints have N+1 queries
   - Example: GET /orders loads items individually
   - Impact: 2000ms p95 latency (target: 500ms)

2. **Connection Pooling**: Hitting limits at 200 concurrent users
   - Current: 100 connections max
   - Need: Connection pooling optimization

3. **Edge Caching**: Not leveraging Cloudflare Cache API enough
   - Opportunity: Cache reads for 1 hour
   - Impact: Could reduce DB load by 70%

## Questions for Jordan
"What patterns have you seen at Stripe for these problems?"

Jordan's insights:
- "For N+1: Use eager loading (selectinload in SQLAlchemy)"
- "For pooling: pgBouncer in transaction mode + smaller pool"
- "For caching: Cache-aside pattern with TTL + invalidation"
```

**Day 1 Output**: Jordan created [architectural-observations.md]

```markdown
# Architectural Observations - Jordan Kim (Day 1)

## Strengths
- Clean separation: Edge (Workers) + Backend (FastAPI) + Data (PostgreSQL)
- Security-first: RLS for multi-tenancy is excellent
- Modern stack: TypeScript, Python, infrastructure-as-code
- Observability: Good instrumentation with Prometheus/Grafana

## Improvement Opportunities

### 1. Query Performance (High Impact, Medium Effort)
**Problem**: N+1 queries causing 2000ms p95 latency
**Solution**: Eager loading with selectinload
**Impact**: 2000ms → 300ms (85% improvement)
**Timeline**: Week 2 implementation

### 2. Connection Pooling (High Impact, Low Effort)
**Problem**: Hitting 100 connection limit at 200 users
**Solution**: PgBouncer transaction mode
**Impact**: Support 2000+ concurrent users
**Timeline**: Week 3 implementation

### 3. Edge Caching (Medium Impact, Low Effort)
**Problem**: Not using Cloudflare Cache API
**Solution**: Cache GET requests with Cache-Control headers
**Impact**: 70% reduction in DB queries
**Timeline**: Week 3 implementation

## Questions for Team
1. Why RLS instead of separate schemas per tenant?
   (Answer: RLS more maintainable, tested in production)
   
2. Have you considered read replicas for reporting queries?
   (Answer: Yes, on roadmap for Q2)
   
3. What's the plan for international expansion?
   (Answer: Multi-region deployment in Q3)

## Recommendations
Let's discuss these in Friday's architecture review.
I can lead design doc for query optimization if helpful.
```

**Team Reaction**: "This is gold. Exactly what we need. Let's prioritize #1 and #2."

## Week 1: Architecture Analysis

### Monday-Wednesday: Code Deep Dive

```bash
# Jordan's exploration approach
cd backend/

# Find all database queries
grep -r "session.exec" --include="*.py" | wc -l
# Result: 247 queries

# Find N+1 patterns
grep -r "for.*in.*:" app/ -A 5 | grep "session.exec" | wc -l
# Result: 34 potential N+1 queries (need review)

# Check connection pooling config
grep -r "pool_size" config/
# Result: pool_size=20 (too small!)

# Review monitoring dashboards
open https://grafana.greyhaven.io
# Identified: Query latency spikes correlate with user activity
```

**Findings Documented**: Jordan created Linear issues for each finding
- GH-456: N+1 query in /orders endpoint
- GH-457: N+1 query in /users/{id}/activity
- GH-458: Increase connection pool size
- GH-459: Add query performance monitoring

### Thursday: Architecture Presentation to Team

**30-Minute Presentation**:
```markdown
# Week 1 Findings: Backend Performance Opportunities

## Overview
Analyzed codebase for performance bottlenecks. Found 3 high-impact improvements.

## Finding #1: N+1 Queries (Highest Impact)
**Location**: GET /orders endpoint
**Current**:
- 1 query for orders
- N queries for order items (N=avg 5 items/order)
- Result: 6 queries per request, 2000ms p95

**Proposed Fix**:
```python
# Before: N+1
orders = session.exec(select(Order)).all()
for order in orders:
    items = session.exec(select(OrderItem).where(...)).all()  # N queries

# After: Eager loading
orders = session.exec(
    select(Order).options(selectinload(Order.items))
).all()  # 2 queries total
```

**Impact**: 2000ms → 300ms (85% improvement)

## Finding #2: Connection Pool Size
**Current**: pool_size=20, max_overflow=10 (30 total)
**Problem**: Hitting limits at 200 concurrent users
**Proposed**: pool_size=50, max_overflow=50 + PgBouncer

**Impact**: Support 2000+ concurrent users

## Finding #3: Missing Edge Caching
**Opportunity**: GET endpoints cacheable for 1 hour
**Implementation**: Cache-Control headers + Cloudflare Cache API
**Impact**: 70% reduction in database queries

## Next Steps
- Design doc for query optimization (next week)
- Implement fixes in priority order
- Add query performance monitoring
```

**Team Feedback**:
- "This is exactly what we needed"
- "How did you find all N+1 queries so fast?" (Jordan: "grep + manual review + experience")
- "Can you lead the implementation?" (Jordan: "Absolutely")

### Friday: First Design Doc

**Jordan Created**: [RFC-023-query-optimization.md]

```markdown
# RFC-023: Query Performance Optimization

**Author**: Jordan Kim
**Status**: Proposed
**Created**: March 8, 2024

## Problem
Multiple endpoints suffer from N+1 query problems, causing 2000ms p95 latency.
This affects user experience and limits scalability.

## Proposed Solution

### Phase 1: Eager Loading (Week 2)
Add selectinload to all relationship queries:
- Orders → OrderItems
- Users → UserProfiles
- Projects → ProjectMembers

**Implementation**: SQLAlchemy selectinload option

### Phase 2: Query Monitoring (Week 3)
Add query performance tracking:
- Log slow queries (>100ms)
- Alert on N+1 patterns
- Dashboard for query analysis

**Implementation**: SQLAlchemy event listeners + Prometheus metrics

### Phase 3: Database Indexes (Week 4)
Add missing indexes identified during analysis:
- order_items.order_id
- project_members.user_id
- activities.tenant_id, created_at

## Migration Strategy
- Deploy with feature flag (gradual rollout)
- Monitor query performance
- Rollback if p95 latency increases

## Success Metrics
- p95 latency: 2000ms → 300ms
- Query count per request: 50% reduction
- Database CPU utilization: 30% reduction

## Alternatives Considered
1. Read replicas: Overkill for current scale
2. Materialized views: Too complex for maintenance
3. Caching: Doesn't solve root cause

## Timeline
- Week 2: Implementation
- Week 3: Monitoring
- Week 4: Indexes + full rollout
```

**Team Review**: Approved unanimously. "Best design doc we've seen in a while."

## Week 2: First Implementation

**Jordan Implemented Query Optimization** (GH-456):
- Added selectinload to 12 endpoints
- Reduced query count by 60%
- Latency improvement: 2000ms → 320ms
- Zero production incidents
- Code review: 1 round, approved by 3 engineers

**Team Impact**:
- "Users are reporting app feels faster"
- "Database CPU dropped 25%"
- "This is a game-changer"

## Week 3: Technical Leadership

**Led Design Review** (First Time):
- New feature: Bulk data export
- Jordan facilitated discussion
- Identified scalability concerns early
- Team: "Great facilitation, asked right questions"

**Mentored Mid-Level Engineer**:
- Pair programmed on complex feature
- Explained architectural patterns
- Code review with detailed feedback
- Mid-level engineer: "Learned more in 1 hour than last month"

## 30-Day Milestone: Technical Impact

### Achievements

**Technical Contributions**:
- 3 major performance improvements shipped
- Query optimization: 85% latency reduction
- Connection pooling: 10x capacity increase
- Edge caching: 70% DB load reduction

**Leadership Impact**:
- Led 2 design reviews (facilitated well)
- Mentored 2 mid-level engineers
- Created best design doc of the year
- Joined architecture review board

**Team Integration**:
- Trusted technical advisor
- Go-to person for architecture questions
- Raised team's technical bar

### Manager Feedback

```markdown
# 30-Day Review: Jordan Kim

## Performance: Exceptional (10/10)

**Technical Excellence**:
- Identified critical issues immediately
- High-quality implementations
- Best design doc we've ever seen
- Zero bugs in production

**Leadership**:
- Natural technical leader
- Great mentor
- Excellent facilitator
- Raises team standards

**Culture Fit**:
- Collaborative, not competitive
- Teaches, doesn't just tell
- Humble despite expertise

## Impact
Jordan's contributions in 30 days exceed most engineers' 6-month impact.
The query optimization alone saved $10K/month in infrastructure costs.

## Next 60 Days
- Tech lead for performance initiative
- Mentor 2 engineers formally
- Join on-call rotation
- Lead architecture decisions
```

## 60-Day: Technical Leadership

- Promoted to **Tech Lead** for backend team
- Leading performance initiative (3 engineers)
- Reduced p95 latency by 75% across all endpoints
- Mentoring formally: 2 mid-level engineers thriving

## 90-Day: Strategic Impact

- Architected next-gen multi-tenant system
- Speaking at company all-hands
- Interviewing senior candidates
- Considered for Staff Engineer promotion

## Results Comparison

| Metric | Junior (Alex) | Senior (Jordan) | Delta |
|--------|---------------|-----------------|-------|
| First commit | Day 1 | Day 1 | Same |
| First PR | Day 4 | Day 2 | 2x faster |
| Full productivity | Week 8 | Week 2 | 4x faster |
| Tech leadership | Week 60+ | Week 3 | 20x faster |
| Architecture impact | None (first 90 days) | Week 1 | Immediate |

## Key Differences

**Junior Onboarding (Alex)**:
- Focus: Learning tech stack, basic contributions
- Buddy system: Daily check-ins, hand-holding
- Complexity: Graduated (good-first-issues → features)
- Leadership: Not expected first 90 days
- Timeline: 12 weeks to full productivity

**Senior Onboarding (Jordan)**:
- Focus: Architecture, technical leadership
- Peer network: Technical equals, not mentors
- Complexity: Immediate high-impact work
- Leadership: Expected from Week 1
- Timeline: 2 weeks to full productivity

## Lessons Learned

**What Worked for Senior Onboarding**:
1. Architecture-first approach (not basic setup)
2. Pre-start reading materials (ADRs, system design)
3. CTO/Staff Engineer involvement (strategic context)
4. Early technical leadership opportunities
5. Trust and autonomy (not hand-holding)
6. Peer network (not buddy system)

**What to Avoid**:
- Don't treat like junior (they have experience)
- Don't over-explain basics (wastes their time)
- Don't delay technical leadership (they're ready)
- Don't micromanage (give autonomy)

**Jordan's Feedback**:
"Best onboarding I've had. You trusted my experience, gave me real problems to solve, and let me make an impact immediately. That's rare and valuable."

---

Related: [junior-engineer-onboarding.md](junior-engineer-onboarding.md) | [linear-automation-workflow.md](linear-automation-workflow.md) | [Return to INDEX](INDEX.md)
