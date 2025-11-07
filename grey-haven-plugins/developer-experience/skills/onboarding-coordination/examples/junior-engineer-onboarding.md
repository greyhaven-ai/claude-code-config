# Example: Junior Frontend Engineer Onboarding Success

Complete 90-day onboarding journey for a junior engineer from nervous first day to confident contributor.

## Context

**New Hire**: Alex Chen - Junior Frontend Engineer
**Background**: CS degree, 6-month internship, first full-time role
**Start Date**: January 15, 2024
**Team**: Frontend (5 engineers: 2 senior, 2 mid, 1 junior)
**Stack**: React 19, TanStack Start, TypeScript, Vite

**Challenges**:
- First full-time engineering role (high anxiety)
- Limited production experience
- Unfamiliar with Grey Haven stack (TanStack Start)
- Remote work (never met team in person)

## Pre-Boarding (Week Before Start)

### Automated Setup

```bash
# Create Linear account
linear user invite --email "alex.chen@greyhaven.io" --role member

# Add to GitHub organization
gh api /orgs/greyhaven/memberships/alex.chen@greyhaven.io -X PUT -f role=member

# Create pre-boarding Linear issues
linear issue create \
  --title "Pre-boarding: Setup for Alex Chen" \
  --team "Engineering" \
  --label "onboarding" \
  --priority 1
```

**Results**:
- ✅ All accounts created 3 days before start
- ✅ Laptop shipped and delivered on time
- ✅ Welcome email sent
- ✅ Buddy introduced herself 2 days before start

## Day 1: Welcome & Setup

### Manager 1:1 (9:00 AM)

Topics covered:
- Team overview and mission
- Role expectations
- Success metrics: First PR within 3 days
- Support system (buddy, manager, team)

**Alex's Response**:
- Excited: "Working with modern React and TanStack"
- Nervous: "Making mistakes, asking too many questions"
- Need: "Clear expectations, patient code reviews"

### Buddy Introduction (11:00 AM)

Sarah Martinez (Senior Frontend Engineer) became Alex's buddy:
- Daily 15-minute check-ins
- Code review mentorship
- Pair programming sessions
- Safe space for any questions

### Environment Setup

```bash
# Install tools
brew install git node@20 gh wrangler

# Configure Git
git config --global user.name "Alex Chen"
git config --global user.email "alex.chen@greyhaven.io"

# Clone repositories
gh repo clone greyhaven/frontend-app
cd frontend-app && npm install

# Run dev server
npm run dev  # Success!
```

### First Commit

```bash
# Update team.md
git checkout -b add-alex-to-team
# Edit docs/team.md to add Alex's info
git commit -m "docs: add Alex Chen to team page"
git push -u origin add-alex-to-team

# Create PR
gh pr create --title "Add Alex Chen to team page"
```

**Day 1 Results**:
- ✅ Environment working (dev server running)
- ✅ First commit pushed
- ✅ First PR created
- ✅ Met whole team
- ✅ Feeling: "Nervous but excited"

## Week 1: Foundations

### Learning Checklist

- [x] Read architecture docs
- [x] Watch tech talk: "Our Frontend Architecture"
- [x] Explore component library
- [x] Understand TanStack Router and Query
- [x] Learn development workflow
- [x] Understand code review process

### First Issue: GH-156

**Task**: "Add loading spinner to Login button"

**Implementation**:
```typescript
// src/components/LoginForm.tsx
import { useState } from 'react';
import { Spinner } from '@/components/ui/Spinner';
import { Button } from '@/components/ui/Button';

export function LoginForm() {
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    try {
      await login(email, password);
    } catch (error) {
      setError(error.message);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <Button 
        type="submit" 
        disabled={isSubmitting}
        aria-busy={isSubmitting}
      >
        {isSubmitting ? (
          <>
            <Spinner size="sm" /> Logging in...
          </>
        ) : 'Log in'}
      </Button>
    </form>
  );
}
```

**Code Review from Sarah**:
```markdown
Great first PR! A few suggestions:

1. Add aria-busy for accessibility ✅
2. Show error message to user ✅
3. Add test for error scenario ✅
4. Use isSubmitting instead of isLoading ✅

Approved! Excellent work.
```

**PR Stats**:
- Time to merge: 26 hours
- Feedback rounds: 1
- Test coverage: 100%
- Alex's feeling: "Intense but satisfying!"

### Week 1 Retrospective

**What Went Well**:
- Environment setup smooth (pairing helped)
- First PR merged successfully
- Team is welcoming and patient
- Detailed but kind code reviews

**Challenges**:
- TanStack Query syntax (still learning)
- Understanding architecture
- Asking for help (getting better!)

**Goals Achieved**:
- ✅ First commit: Day 1 (target: Day 1) ✅
- ✅ First PR merged: Day 4 (target: Day 3) ⚡
- ✅ Comfortable with team: Yes!

## Week 2-4: Building Momentum

**Week 2 Accomplishments**:
- Completed 3 features independently
- GH-189: Password strength indicator (2 days)
- GH-201: Dark mode toggle (3 days)  
- GH-215: Accessibility fixes (1 day)

**Week 3 Growth**:
- First cross-team collaboration
- Coordinated with backend on API integration
- Learned API versioning and error handling

**Week 4 Leadership**:
- Led daily standup for first time
- Contributed to planning discussion
- Gained confidence in team participation

## 30-Day Milestone (February 15)

### Manager Feedback

**Progress**:
- ✅ Exceeded velocity (8 issues vs 5 target)
- ✅ Code quality strong (clean, tested, accessible)
- ✅ Team integration excellent
- ✅ Growth mindset evident

**Areas for Development**:
- Confidence (still apologizes for questions)
- Scope estimation (improving with practice)
- Proactivity (can suggest improvements)

**Feedback for Manager**:
"Daily check-ins with Sarah are invaluable. Code reviews are the best learning tool. Love the pairing sessions."

**Rating**: 9/10 - Excellent start!

**Alex's Reflection**:
"I was so nervous on day 1. Now I feel like I belong. The buddy system made all the difference."

## 60-Day Milestone: Technical Depth

**First Medium Feature (March)**: User profile editor
- 5 components, 12 API integrations
- Complex form validation
- Collaborated with design, backend, product
- Led design discussion
- Completed in 2 weeks (on time!)

**Mentoring Moment (March 20)**:
- New junior engineer joined
- Alex paired with them on first issue
- Explained codebase patterns
- "Feels good to help like Sarah helped me"

## 90-Day Milestone: Full Integration (April 15)

### Technical Achievements

- 23 Linear issues completed (15 target = 153%)
- 100% test coverage maintained
- 2 developer experience improvements
- Speaking at team tech talk on accessibility

### Team Integration

- Trusted for frontend decisions
- Mentoring next junior hire
- Leading accessibility initiatives
- Contributed to hiring interviews

### Final Review

**Manager Assessment**:
```markdown
Alex exceeded all expectations. Strong technical skills,
excellent collaboration, growth mindset, already contributing
to team culture.

Recommendation:
- Promote to Mid-Level at 18 months
- Assign as tech lead for accessibility
- Include in architecture discussions

Performance Rating: 10/10
```

## Results Summary

### Metrics

**Time to Productivity**:
- First commit: Day 1 ✅
- First PR: Day 4 ✅
- First feature: Week 2 ✅
- Full productivity: Week 8 (target: Week 12) ⚡

**Quality**:
- Avg feedback rounds: 1.2 (excellent)
- Test coverage: 100%
- Production bugs: 0 (first 90 days)
- Accessibility: 100% compliant

**Satisfaction**:
- 30-day: 9/10
- 60-day: 9.5/10
- 90-day: 10/10 ("Best onboarding ever")

**Team Impact**:
- Issues: 23 (153% of target)
- Features: 8 major, 15 minor
- DX improvements: 2
- Already mentoring next hire

### Key Success Factors

1. **Buddy System**: Daily check-ins critical
2. **Graduated Complexity**: Good-first-issues
3. **Patient Code Reviews**: Educational feedback
4. **Psychological Safety**: No question too small
5. **Early Wins**: Quick PR merge built confidence
6. **Clear Expectations**: Transparent milestones
7. **Automation**: Scripted setup, no toil

## Lessons Learned

**What Worked**:
- Buddy pairing on day 1 setup
- Good-first-issues ready
- Daily check-ins (not just weekly)
- Detailed PR feedback
- Formal 30/60/90 check-ins

**What to Improve**:
- More architectural context early
- Regular pair programming (2x/week)
- Earlier cross-team collaboration
- More product roadmap visibility

**Alex's Advice**:
"Ask all the questions. Everyone wants to help. First PR is scary but you'll feel amazing when it merges. Trust the process."

---

Related: [senior-engineer-onboarding.md](senior-engineer-onboarding.md) | [linear-automation-workflow.md](linear-automation-workflow.md) | [Return to INDEX](INDEX.md)
