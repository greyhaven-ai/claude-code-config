# Milestone Tracking Framework

Framework for 30/60/90 day milestones - success criteria, assessment methods, red flags, and intervention strategies.

## Milestone Overview

| Milestone | Primary Goal | Success Criteria | Intervention Threshold |
|-----------|--------------|------------------|------------------------|
| **30-Day** | Productivity | Shipping features independently | < 50% expected velocity |
| **60-Day** | Technical Depth | Leading medium features | No growth trajectory |
| **90-Day** | Full Integration | Fully productive team member | Performance concerns |

## 30-Day Milestone

### Success Criteria

**Technical**:
- [ ] Shipped 3+ features independently
- [ ] Code quality strong (< 2 feedback rounds per PR)
- [ ] Test coverage maintained (80%+)
- [ ] Understands core architecture

**Collaboration**:
- [ ] Comfortable asking questions
- [ ] Participating in code reviews
- [ ] Contributing to team discussions
- [ ] Building relationships with team

**Velocity**:
- Junior: 40-60% of team average
- Mid: 60-80% of team average
- Senior: 80-100% of team average

### Assessment Template

**Manager Preparation**:
```markdown
# 30-Day Review: [Name]

## Data to Review
- Linear issues: [X completed, Y in progress]
- PRs merged: [count], avg feedback rounds: [count]
- Test coverage: [percentage]
- Code reviews given: [count]
- Meeting participation: [notes]

## Qualitative Observations
- Team feedback: [summary]
- Buddy feedback: [summary]
- Manager observations: [summary]
```

**Meeting Agenda** (45 minutes):
```markdown
# 30-Day Check-in: [Name]

## Part 1: Progress Review (20 min)

Manager: "Let's review your first 30 days."

**Technical**:
- What have you shipped?
- What's the quality been like?
- Where are you still learning?

**Team**:
- How's the team integration?
- Are you comfortable asking questions?
- Who have you connected with?

**Velocity**:
- Are you meeting expectations?
- What's blocking you?

## Part 2: Feedback (15 min)

Manager: "What's going well?"
New hire: [strengths, wins, positive experiences]

Manager: "What's challenging?"
New hire: [struggles, confusion, gaps]

Manager: "What support do you need?"
New hire: [requests, adjustments]

## Part 3: Forward-Looking (10 min)

Manager: "Here's my feedback on your progress..."
[Specific, actionable feedback]

Manager: "Next 30 days, let's focus on..."
[2-3 specific goals]

Manager: "Any questions about expectations or goals?"
New hire: [questions, concerns]
```

### Outcome Examples

**Exceeding Expectations** (9-10/10):
```
Alex has exceeded all 30-day expectations.

Technical:
- 8 features shipped (target: 5)
- Code quality excellent (avg 1.2 feedback rounds)
- 100% test coverage maintained

Team:
- Strong collaboration
- Proactive in discussions
- Great PR reviews

Velocity: 65% of team average (junior target: 50%)

Next 30 days: Take on medium feature, mentor next junior hire
```

**Meeting Expectations** (7-8/10):
```
Jordan is meeting 30-day expectations well.

Technical:
- 5 features shipped (target: 5)
- Code quality good (avg 1.8 feedback rounds)
- 85% test coverage

Team:
- Collaborating well
- Still building confidence in discussions

Velocity: 70% of team average (mid target: 70%)

Next 30 days: Lead design discussion, increase participation
```

**Below Expectations** (5-6/10):
```
Sam is below 30-day expectations - needs support.

Technical:
- 3 features shipped (target: 5)
- Code quality inconsistent (avg 3.5 feedback rounds)
- 70% test coverage (target: 80%)

Team:
- Not asking enough questions (red flag)
- Isolated (red flag)

Velocity: 35% of team average (target: 60%)

**Intervention Plan**:
- Daily check-ins with manager (next 2 weeks)
- Pair programming 3x/week
- Smaller tasks to build confidence
- Address psychological safety concerns

Follow-up: 2 weeks
```

### Red Flags at 30 Days

**Technical Red Flags**:
- Not shipping features (< 40% expected velocity)
- Consistently poor code quality (> 3 feedback rounds)
- Not writing tests or low coverage
- Same mistakes repeatedly (not learning)

**Behavioral Red Flags**:
- Not asking questions (sign of fear, not competence)
- Isolated (not connecting with team)
- Defensive to feedback (growth mindset issue)
- Missing deadlines consistently

**When to Intervene**:
- 2+ red flags → Immediate intervention (don't wait for 60-day)
- 3+ red flags → Serious performance conversation + PIP consideration

## 60-Day Milestone

### Success Criteria

**Technical Depth**:
- [ ] Leading medium features end-to-end
- [ ] Understanding architectural tradeoffs
- [ ] Proactively improving code quality
- [ ] Technical expert in one area

**Leadership** (if applicable):
- [ ] Mentoring newer team members
- [ ] Leading design discussions
- [ ] Contributing to architecture decisions
- [ ] Improving team processes

**Velocity**:
- Junior: 70-80% of team average
- Mid: 90-100% of team average
- Senior: 100-120% of team average + force multiplier

### Assessment Template

**Manager Preparation**:
```markdown
# 60-Day Review: [Name]

## Progress Since 30-Day
- Features shipped: [count]
- Technical growth areas: [list]
- Leadership contributions: [examples]
- Team impact: [observations]

## Trend Analysis
- Is velocity increasing? [yes/no, by how much]
- Is code quality improving? [yes/no, evidence]
- Is confidence growing? [yes/no, examples]
- Is scope increasing? [simple → medium → complex]
```

**Meeting Agenda** (45 minutes):
```markdown
# 60-Day Check-in: [Name]

## Part 1: Growth Assessment (20 min)

Manager: "You've been here 2 months. Let's talk growth."

**Technical Depth**:
- What complex problems have you solved?
- Where do you feel expert now?
- What's still challenging?

**Leadership**:
- Have you mentored anyone?
- Are you contributing to design discussions?
- What have you improved beyond your tasks?

**Trajectory**:
- How do you compare to your 30-day self?
- What's improved most?

## Part 2: Career Discussion (15 min)

Manager: "Let's talk about your career trajectory."

- What do you want to be known for?
- What skills do you want to develop?
- Where do you see yourself in 6-12 months?
- How can I support your growth?

## Part 3: Performance Rating (10 min)

Manager: "Here's my assessment of your performance..."
[Honest, specific feedback with examples]

Manager: "Next 30 days, focus on..."
[2-3 growth goals aligned with career aspirations]
```

### Outcome Examples

**Exceptional** (9-10/10):
```
Jordan has been exceptional - promoting to Tech Lead.

Technical:
- Led design for 3 major features
- Query optimization: 85% latency reduction
- Architectural proposals adopted by team

Leadership:
- Mentoring 2 mid-level engineers
- Leading design reviews effectively
- Raised team's technical bar

Impact: 150% of team average + force multiplier

Next: Tech Lead role, leading performance initiative
```

**Strong** (8-9/10):
```
Alex is performing strongly - on track.

Technical:
- Shipped user profile editor (complex, 2 weeks)
- Code quality consistently high
- Technical depth growing

Leadership:
- Mentored new junior hire
- Speaking at tech talk on accessibility
- Contributing to hiring

Velocity: 85% of team average (ahead of curve)

Next: Lead medium project, join interviewing rotation
```

**Concerns** (6-7/10):
```
Sam's progress has stalled - intervention needed.

Technical:
- Velocity flat (40% at 30 days, 45% at 60 days)
- Not taking on larger scope
- Struggling with ambiguity

Behavioral:
- Still not asking enough questions
- Isolated from team
- Defensive to feedback

**Action Plan**:
- Structured improvement plan (30 days)
- Clear expectations and milestones
- Daily manager check-ins
- Consider role fit conversation

Decision point: 90 days
```

### Red Flags at 60 Days

**Stagnation**:
- No velocity improvement from 30-day
- No scope increase (still doing simple tasks)
- Not demonstrating growth

**Recurring Issues**:
- Same feedback every PR (not learning)
- Same mistakes repeatedly
- No improvement from 30-day feedback

**Culture Misalignment**:
- Not collaborating well
- Negative attitude
- Not receptive to feedback

**When to Consider Exit**:
- No improvement from 30-day intervention
- Multiple red flags persist
- Not meeting minimum bar for role

## 90-Day Milestone

### Success Criteria

**Full Productivity**:
- [ ] Velocity at or above team average
- [ ] Handling full complexity range
- [ ] Contributing to team success
- [ ] Fully integrated team member

**Growth Trajectory**:
- [ ] Clear strengths identified
- [ ] Development plan established
- [ ] Career path alignment
- [ ] Future potential evident

**Team Contribution**:
- [ ] Positive team culture impact
- [ ] Helping others succeed
- [ ] Improving processes/tools
- [ ] Building relationships across teams

### Formal Performance Review

**Review Structure** (60 minutes):
```markdown
# 90-Day Performance Review: [Name]

## Part 1: Performance Assessment (30 min)

Manager: "This is your formal 90-day performance review."

**Technical Contributions**:
- Features shipped: [list major accomplishments]
- Code quality: [assessment with examples]
- Technical growth: [areas of expertise]
- Velocity: [compared to expectations]

**Team Collaboration**:
- Code reviews: [quality and quantity]
- Mentoring: [who have you helped]
- Communication: [clarity, proactivity]
- Culture fit: [team values alignment]

**Growth Trajectory**:
- Strengths: [2-3 clear strengths]
- Development areas: [2-3 growth opportunities]
- Progress: [30-day vs 60-day vs 90-day comparison]

## Part 2: Performance Rating (10 min)

Manager: "Your overall performance rating is [X/10]."
[Specific examples supporting the rating]

**Rating Scale**:
- 9-10: Exceptional (promoting, fast-track)
- 8-9: Strong (on track, exceeding expectations)
- 7-8: Solid (meeting expectations)
- 6-7: Concerns (improvement needed)
- < 6: Not meeting bar (PIP or exit)

## Part 3: Future Planning (20 min)

Manager: "Let's talk about your next 6 months."

**Career Trajectory**:
- What role fits your strengths?
- What skills to develop?
- Promotion timeline (if applicable)
- Growth opportunities

**Development Plan**:
- Technical skills: [specific goals]
- Leadership skills: [specific goals]
- Timeline: [milestones]
- Support: [resources, coaching]

**Next Steps**:
- Documentation of review
- Salary/promotion decisions
- Ongoing 1:1 cadence
```

### Rating Examples

**Exceptional (9-10/10) - Promote**:
```
Jordan exceeded all expectations - immediate Tech Lead promotion.

90-Day Achievements:
- Query optimization: saved $10K/month in infrastructure
- Mentored 2 engineers effectively
- Led 4 design reviews
- Raised team's technical standards

Trajectory: Promoting to Tech Lead, on track for Staff in 12-18 months.
```

**Strong (8-9/10) - On Track**:
```
Alex performed strongly - on track for mid-level promotion at 18 months.

90-Day Achievements:
- 23 issues completed (153% of target)
- 100% test coverage maintained
- Leading accessibility initiatives
- Mentoring next junior hire

Trajectory: Continue growth, mid-level promotion at 18 months.
```

**Solid (7-8/10) - Meeting Bar**:
```
Casey is meeting expectations - continue current trajectory.

90-Day Achievements:
- 18 issues completed (120% of target)
- Good code quality
- Collaborating well

Trajectory: Solid performer, meeting expectations, continue development.
```

**Concerns (6-7/10) - PIP**:
```
Sam is not meeting expectations - formal Performance Improvement Plan.

90-Day Issues:
- Velocity: 50% of target (should be 80%+)
- Code quality: inconsistent
- Team fit: concerns about collaboration

**30-Day PIP**:
- Clear expectations and metrics
- Daily manager check-ins
- Specific deliverables
- Decision point: 30 days

Outcome: Improve to meet bar OR exit.
```

## Intervention Strategies

### Early Intervention (30-Day Red Flags)

**Immediate Actions**:
1. Increase 1:1 frequency (daily or 3x/week)
2. Pair programming for knowledge transfer
3. Reduce task complexity temporarily
4. Address psychological safety concerns

**Example Conversation**:
```
Manager: "I've noticed you're not asking many questions. What's going on?"
New hire: "I don't want to seem incompetent."
Manager: "That's the problem. Not asking questions IS incompetent. Asking is how you learn. From now on, I want 5 questions per day. Seriously."
```

### Mid-Course Correction (60-Day Concerns)

**Structured Improvement Plan** (not PIP, softer):
1. Clear 30-day goals with metrics
2. Weekly check-ins to track progress
3. Additional resources (pairing, training)
4. Honest feedback about expectations

**Example Plan**:
```markdown
# 30-Day Improvement Plan: Sam

## Goals (Next 30 Days)
1. Velocity: Ship 5 features (vs 3 last month)
2. Quality: < 2 feedback rounds per PR (vs 3.5)
3. Collaboration: Give 10 code reviews (vs 2)

## Support
- Pair programming 3x/week with Sarah
- Daily manager check-ins (15 min)
- Smaller, clearer tasks

## Check-in: 2 weeks (progress update)
## Decision Point: 30 days (on track OR formal PIP)
```

### Formal PIP (90-Day Performance Issues)

**When to PIP**:
- Not meeting minimum bar after 90 days
- No improvement from 60-day intervention
- Clear performance gap with no progress

**PIP Structure** (30-60 days):
```markdown
# Performance Improvement Plan: [Name]

## Current Performance
[Specific gaps with examples]

## Expected Performance
[Clear, measurable expectations]

## Success Metrics
[Objective criteria for meeting bar]

## Timeline
- Week 1-2: [specific milestones]
- Week 3-4: [specific milestones]
- End of PIP: [decision criteria]

## Support
- Daily manager check-ins
- Resources and training
- Clear feedback loops

## Outcomes
- Success: Continue employment, performance improves
- Failure: Transition out of company
```

---

Related: [Onboarding Best Practices](onboarding-best-practices.md) | [Linear API Patterns](linear-api-patterns.md) | [Buddy System Guide](buddy-system-guide.md) | [Return to INDEX](INDEX.md)
