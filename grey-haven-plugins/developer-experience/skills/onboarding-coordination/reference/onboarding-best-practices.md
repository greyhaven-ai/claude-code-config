# Onboarding Best Practices

Research-backed best practices for developer onboarding that accelerate time-to-productivity while building team connection and psychological safety.

## Core Principles

### 1. Psychological Safety First

**Why It Matters**: New hires won't ask questions or admit confusion if they fear judgment
- 73% of engineers who felt "safe to ask questions" reached full productivity 2x faster
- Anxiety is the #1 blocker to learning (neuroscience research)

**How to Create It**:
- Manager: "No question is too small. I'd rather you ask 100 times than guess wrong once."
- Buddy: "I still Google basic syntax. Everyone does. Let me show you."
- Team: Normalize mistakes - share your own onboarding blunders in team meeting

**Red Flag**: New hire apologizes for asking questions → Immediate intervention needed

### 2. Graduated Complexity

**Why It Matters**: Throwing complex work at new hires causes overwhelm and poor quality
- New hires given "hard" work first: 45% quality issues, 12 weeks to full productivity
- New hires given graduated complexity: 15% quality issues, 8 weeks to full productivity

**Progression**:
```
Week 1: Good-first-issues (UI fix, docs update)
Week 2: Small features (single component, simple API)
Week 3-4: Medium features (multiple components, backend integration)
Week 5-8: Complex features (architecture decisions, cross-team)
Week 9+: Full complexity (whatever the team needs)
```

**How to Judge Complexity**:
- **Simple**: 1-2 files, clear requirements, no architectural decisions
- **Medium**: 3-5 files, some ambiguity, minor design choices
- **Complex**: 5+ files, significant ambiguity, architecture impact

### 3. Automate Mechanics, Humanize Meaning

**Automate** (boring but necessary):
- Account creation (Linear, GitHub, Slack)
- Environment setup (scripts, not manual steps)
- Task tracking (automated Linear issue creation)
- Milestone reminders (Slack notifications)

**Humanize** (critical for success):
- Code review feedback (explain the "why")
- Architecture discussions (share context and history)
- Career conversations (understand goals and fears)
- Team integration (introduce to people, not just systems)

**Example**:
- ❌ Bad: "Your PR is missing tests. Please add them." (mechanical)
- ✅ Good: "Great work! Before merging, let's add tests. Here's why we test everything: [context]. I'll pair with you on the first one." (humanized)

### 4. Buddy System (Not Mentor)

**Buddy ≠ Mentor**:
- **Buddy**: Peer, daily check-ins, tactical help, safe space for "dumb" questions
- **Mentor**: Senior, monthly check-ins, career advice, strategic guidance

**Why Buddies Work**:
- Peers feel less intimidating than seniors
- Buddies remember recent onboarding struggles
- Daily contact builds trust faster

**Buddy Selection Criteria**:
- 1-3 years at company (not too junior, not too senior)
- Patient and empathetic (not just technically strong)
- Good communicator (can explain clearly)
- Volunteered (not assigned reluctantly)

### 5. Feedback Loops

**30/60/90 Day Check-ins** (formal):
- 30 days: "How's it going? What's working? What's not?"
- 60 days: "Are you growing? What support do you need?"
- 90 days: "Performance review. What's next for you?"

**Weekly 1:1s** (informal):
- Manager: "What went well this week? Any blockers?"
- New hire: "I learned X, struggled with Y, need help with Z"

**Daily Buddy Check-ins** (Week 1 only):
- Buddy: "How was today? Any questions before EOD?"
- 15 minutes, casual, safe space

## Experience Level Differences

### Junior Engineers (0-2 Years)

**Needs**:
- More hand-holding (pair programming, detailed feedback)
- Explicit expectations ("100% test coverage means every function tested")
- Confidence building (celebrate small wins)
- Technical fundamentals (Git workflow, PR process, testing)

**Timeline**:
- First PR: Week 1
- Independent work: Week 4
- Full productivity: Week 8-12

**Common Mistakes**:
- Assuming they know basics (they don't - teach Git, testing, PR workflow)
- Too much autonomy too fast (they need structure)
- Skipping celebrations (they need positive reinforcement)

**Example Buddy Conversation**:
```
Buddy: "Let's walk through your first PR together. First, create a branch..."
[Step-by-step guidance]
Buddy: "Great job! You just shipped your first code. That's a big deal."
```

### Mid-Level Engineers (2-5 Years)

**Needs**:
- Context (architecture decisions, team history)
- Autonomy (trust them to figure things out)
- Growth opportunities (lead small features, mentor juniors)
- Team integration (cross-team collaboration)

**Timeline**:
- First PR: Day 2-3
- Independent work: Week 2
- Full productivity: Week 4-6

**Common Mistakes**:
- Too much hand-holding (they'll feel micromanaged)
- Assuming they know your stack (they need onboarding too, just faster)
- No growth opportunities (they'll get bored)

**Example Manager Conversation**:
```
Manager: "You've shipped 3 features. Ready to lead a medium project?"
Engineer: "Yes! What did you have in mind?"
Manager: "Here's the context... I trust you to figure out the approach. Let's review your design doc next week."
```

### Senior Engineers (5+ Years)

**Needs**:
- Strategic context (business goals, technical roadmap)
- Early leadership opportunities (design reviews, mentoring)
- Architectural input (participate in technical decisions)
- Peer network (connect with other seniors, not "buddy")

**Timeline**:
- First PR: Day 1-2
- Independent work: Immediately
- Full productivity: Week 2-4
- Technical leadership: Week 3-4

**Common Mistakes**:
- Treating like junior (they have experience - trust it)
- Delaying leadership (they're ready Week 1)
- No architectural involvement (they want to contribute strategically)

**Example CTO Conversation**:
```
CTO: "Here's our current architecture [diagram]. Biggest challenge: query performance. What patterns have you seen work at scale?"
Senior: "At my last company, we solved this with [pattern]. I could analyze your codebase and propose improvements."
CTO: "Do it. Present to the team Friday."
```

## Pre-Boarding (Before Day 1)

**Goal**: New hire feels welcome and prepared, not anxious

**Automate**:
- [ ] Create accounts (Linear, GitHub, Slack) - 3 days before start
- [ ] Ship equipment (laptop, monitor) - arrives 2 days before start
- [ ] Send welcome email - 1 week before start
- [ ] Create Linear onboarding issues - 1 week before start

**Personalize**:
- [ ] Manager sends personal welcome message
- [ ] Buddy introduces themselves via email
- [ ] Team adds welcome message in Slack
- [ ] Send reading materials (architecture docs, team culture)

**Welcome Email Template**:
```
Subject: Welcome to Grey Haven! Your first day is [Date]

Hi [Name],

We're excited to have you join the team on [Date]!

Here's what to expect on Day 1:
- 9:00 AM: Welcome meeting with me (30 min)
- 10:00 AM: Meet your buddy, [Buddy Name]
- 11:00 AM: IT setup and environment configuration
- 1:00 PM: Team intro meeting
- 3:00 PM: First commit (we'll help!)

Before you start, check out:
- Our architecture docs: [link]
- Recent team blog posts: [link]
- Your buddy [Name] will reach out tomorrow

Questions? Reply to this email.

Looking forward to working with you!
[Manager Name]
```

## Day 1 Framework

**Morning** (Focus: Welcome + Setup):
- 9:00 AM: Manager 1:1 (expectations, team overview)
- 10:00 AM: Buddy introduction (daily check-in schedule)
- 11:00 AM: IT setup (laptop, accounts, 2FA)

**Afternoon** (Focus: First Commit):
- 1:00 PM: Team intro meeting (names, roles, fun facts)
- 2:00 PM: Environment setup (pair with buddy)
- 3:00 PM: First commit (update team.md or docs)
- 4:00 PM: Buddy check-in (how was today?)

**Success Metric**: Dev environment working + first commit pushed

**Common Day 1 Failures**:
- ❌ Environment setup takes all day (automate it!)
- ❌ No first commit (feels like "wasted day")
- ❌ Information overload (keep meetings short)
- ❌ Lunch alone (buddy should eat with them)

## Week 1 Framework

**Goal**: First PR merged, comfortable with team

**Learning** (40% of time):
- Read architecture documentation
- Watch recorded tech talks
- Review code review guidelines
- Understand development workflow

**Doing** (60% of time):
- Complete "good-first-issue"
- Shadow buddy on code review
- Pair program on small feature
- Deploy to staging environment

**Social**:
- Daily standup participation
- Coffee chats with 2-3 team members
- Buddy check-ins (15 min/day)

**End of Week 1 Retrospective**:
```
Manager: "What went well this week?"
New hire: "I merged my first PR! Team is super welcoming."

Manager: "What was challenging?"
New hire: "TanStack Query syntax is still confusing."

Manager: "What support do you need?"
New hire: "More pair programming would help."

Manager: "Let's schedule 2 pairing sessions next week."
```

## Common Onboarding Mistakes

### Mistake 1: No Clear First Task

**Problem**: "Explore the codebase" is overwhelming
**Solution**: Assign specific "good-first-issue" on Day 1

**Before**:
```
Manager: "Spend the first week exploring the codebase."
New hire: [Confused, anxious, doesn't know where to start]
```

**After**:
```
Manager: "Your first task: Add loading spinner to Login button. Here's the Linear issue. Buddy will help."
New hire: [Clear goal, knows what success looks like]
```

### Mistake 2: Assuming Knowledge

**Problem**: "You know Git, right?" (they might not)
**Solution**: Teach fundamentals, even if redundant

**Common Assumptions** (often wrong):
- Git workflow (branches, PRs, rebasing)
- Testing best practices (what to test, how much)
- Code review etiquette (when to push back)
- Deployment process (staging, production, rollbacks)

**Better Approach**:
```
Buddy: "Let me show you our Git workflow, even if you've used Git before. Every team does it differently."
[Walk through branch naming, PR process, code review]
```

### Mistake 3: Information Overload

**Problem**: 8 hours of meetings on Day 1
**Solution**: Spread information over weeks, not days

**Bad Day 1 Schedule**:
```
9-10 AM: HR orientation
10-11 AM: Engineering overview
11-12 PM: Architecture deep-dive
12-1 PM: Lunch (alone)
1-2 PM: Security training
2-3 PM: Tools overview
3-4 PM: Code walkthrough
4-5 PM: Q&A
[New hire exhausted, retains 20% of information]
```

**Good Day 1 Schedule**:
```
9-10 AM: Manager 1:1
10-12 PM: Environment setup with buddy
12-1 PM: Lunch with team
1-3 PM: First commit (guided)
3-4 PM: Team intro (15 min) + exploration
4-5 PM: Buddy check-in
[New hire energized, has working environment + first commit]
```

### Mistake 4: No Feedback Loops

**Problem**: Wait until 90 days to discuss issues
**Solution**: Weekly check-ins with early course correction

**Timeline for Feedback**:
- Daily (Week 1): Buddy check-ins
- Weekly (Weeks 2-12): Manager 1:1s
- Monthly (30/60/90): Formal milestone reviews

**Early Warning Signs** (Week 2-4):
- Not asking questions (sign of fear, not understanding)
- Missing deadlines consistently (complexity too high?)
- Isolated (not connecting with team)
- Low PR activity (blocked? unclear expectations?)

## Success Metrics

**Time to Productivity**:
- First commit: < 1 day
- First PR merged: < 3 days
- First feature shipped: < 2 weeks
- Full productivity: < 8-12 weeks

**Quality Metrics**:
- PR feedback rounds: < 2 (well-mentored = fewer iterations)
- Test coverage: 100% (taught to test from Day 1)
- Production bugs: 0 in first 90 days (careful code review)

**Satisfaction**:
- 30-day feedback: 4+/5
- 60-day feedback: 4.5+/5
- 90-day retention: 95%+

**Team Impact**:
- Buddy satisfaction: 4+/5 ("rewarding to mentor")
- Manager satisfaction: "Exceeded expectations"
- Team culture: "Onboarding is a strength"

---

Related: [Linear API Patterns](linear-api-patterns.md) | [Buddy System Guide](buddy-system-guide.md) | [Milestone Tracking](milestone-tracking.md) | [Return to INDEX](INDEX.md)
