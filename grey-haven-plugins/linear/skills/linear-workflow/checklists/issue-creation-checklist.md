# Issue Creation Checklist

**Use before creating Linear issues.**

## Issue Content

### Title
- [ ] Title is specific and actionable
- [ ] Title starts with verb (Add, Fix, Update, etc.)
- [ ] Title describes user-facing change or technical goal
- [ ] Title is under 100 characters

### Description
- [ ] Description clearly explains what needs to be done
- [ ] Description includes "why" (motivation/user pain point)
- [ ] For bugs: steps to reproduce included
- [ ] For features: user story or use case included
- [ ] Technical implementation notes included (optional)

### Acceptance Criteria
- [ ] Acceptance criteria are specific and testable
- [ ] Each criterion starts with "User can..." or "System..."
- [ ] Multi-tenant isolation requirements specified
- [ ] Test coverage target specified (>80%)
- [ ] Performance requirements specified (if applicable)

### Technical Details

#### Multi-Tenant Considerations
- [ ] tenant_id requirements documented
- [ ] RLS policy requirements documented
- [ ] Tenant isolation testing specified

#### Database Changes (if applicable)
- [ ] Schema changes use snake_case field names
- [ ] Migration strategy documented
- [ ] Rollback plan documented
- [ ] Index requirements specified

#### Doppler Configuration
- [ ] Required environment variables listed
- [ ] Doppler environments specified (dev/test/staging/production)
- [ ] Secret rotation strategy noted (if applicable)

### Labels
- [ ] Type label assigned (feature/bug/chore/docs/refactor)
- [ ] Component label assigned (frontend/backend/database/auth)
- [ ] Priority label assigned (critical/high-priority/low-priority)
- [ ] Additional relevant labels added

### Estimate
- [ ] Story points assigned using Fibonacci sequence
- [ ] Estimate reflects complexity + uncertainty
- [ ] Issues >8 points broken into smaller issues
- [ ] Estimate discussed with team (if unclear)

### Relationships
- [ ] Related issues linked (Blocks/Blocked by)
- [ ] Parent epic linked (if part of larger feature)
- [ ] Dependencies documented

## Before Submitting

### Quality Check
- [ ] Title and description are clear to someone unfamiliar with context
- [ ] Technical jargon explained or avoided
- [ ] Links to relevant documentation included
- [ ] Screenshots/mockups attached (if applicable)

### Team Alignment
- [ ] Issue aligns with current sprint goals
- [ ] Issue priority discussed with team lead (if high-priority)
- [ ] Issue dependencies communicated to affected team members
- [ ] Issue assigned to appropriate team member (or left unassigned for triage)

## Post-Creation

### Issue Management
- [ ] Issue added to appropriate project/milestone
- [ ] Issue added to current cycle (if starting immediately)
- [ ] Issue status set correctly (Backlog/Todo)
- [ ] Team notified of new issue (if urgent)
