# Onboarding Plan Template

Copy-paste ready template for creating personalized onboarding plans. Replace all [placeholders] with actual details.

---

# Onboarding Plan: [Full Name] - [Role Title]

## Overview

- **New Hire**: [Full Name]
- **Role**: [Frontend Engineer / Backend Engineer / Full-Stack Engineer / DevOps Engineer]
- **Experience Level**: [Junior (0-2 years) / Mid-Level (2-5 years) / Senior (5+ years)]
- **Start Date**: [YYYY-MM-DD]
- **Buddy**: [Buddy Name] ([buddy-email@greyhaven.io](mailto:buddy-email@greyhaven.io))
- **Manager**: [Manager Name] ([manager-email@greyhaven.io](mailto:manager-email@greyhaven.io))
- **Team**: [Team Name] ([X] engineers: [breakdown by level])

## Pre-Boarding (Before Day 1)

**Timeline**: Complete 3 days before start date

### Automation Checklist
- [ ] Create Linear account and add to [Team] workspace
- [ ] Add to GitHub organization (`greyhaven`) and relevant repositories
- [ ] Add to Slack workspace (channels: #engineering, #general, #[team-name], #random)
- [ ] Send welcome email with Day 1 logistics
- [ ] Ship laptop and equipment (arrives 2 days before start)
- [ ] Create Linear onboarding issues (use `create-onboarding.sh` script)
- [ ] Introduce buddy via email (2 days before start)

### Welcome Email Draft

```
Subject: Welcome to Grey Haven! Your first day is [Date]

Hi [First Name],

We're excited to have you join [Team Name] as [Role] on [Start Date]!

**Your First Day**:
- **9:00 AM**: Welcome meeting with me (30 min) - [Zoom link]
- **10:00 AM**: Meet your buddy, [Buddy Name] (15 min)
- **11:00 AM**: IT setup and environment configuration
- **12:00 PM**: Lunch (we'll order in!)
- **1:00 PM**: Team intro meeting (30 min)
- **3:00 PM**: First commit with buddy's help

**Before You Start**:
Here are some reading materials to get familiar with our stack:
- Architecture documentation: [link]
- Recent team blog posts: [link]
- Tech stack overview: [link]

[Buddy Name] will reach out tomorrow to introduce themselves.

**Equipment**: Your laptop and monitor should arrive on [Date - 2 days before start]. If they don't, email IT@greyhaven.io immediately.

**Questions?** Reply to this email anytime.

Looking forward to working with you!

[Manager Name]
[Manager Title]
```

---

## Day 1: Welcome & Setup

**Goal**: Working dev environment + first commit

### Morning (9:00 AM - 12:00 PM)

**9:00 - 9:30 AM: Manager Welcome Meeting**
- Team overview and mission
- Role expectations and success metrics
- Support system (buddy, manager, team)
- First week goals
- Q&A

**10:00 - 10:15 AM: Buddy Introduction**
- Get to know each other
- Schedule daily check-ins (4:00 PM Week 1)
- Buddy explains their role
- Set communication preferences (Slack, in-person, etc.)

**10:15 AM - 12:00 PM: IT Setup**
- Laptop setup and configuration
- Install core tools (Homebrew, Git, Node, Python, Claude Code)
- Configure 2FA for all accounts
- Test access to all systems

### Afternoon (1:00 PM - 5:00 PM)

**1:00 - 1:30 PM: Team Intro Meeting**
- Everyone introduces themselves (name, role, fun fact)
- Team overview (current projects, upcoming work)
- Q&A about team culture and processes

**2:00 - 4:00 PM: Environment Setup with Buddy**
- Clone grey-haven repositories
- Run setup script: `./scripts/setup-dev-environment.sh`
- Verify dev servers running (frontend and backend)
- Install Claude Code plugins from marketplace

**4:00 - 4:30 PM: First Commit**
- Update `docs/team.md` with your name and info
- Create branch: `git checkout -b add-[firstname]-to-team`
- Commit and push
- Create PR: `gh pr create --title "Add [Name] to team page"`

**4:30 - 5:00 PM: Daily Buddy Check-in**
- How was your first day?
- Any questions before end of day?
- Plan for tomorrow

### Day 1 Success Metrics
- [ ] Dev environment working (can run dev servers)
- [ ] First commit pushed
- [ ] First PR created
- [ ] Met whole team
- [ ] Feeling: Nervous but excited (normal!)

---

## Week 1: Foundations

**Goal**: First PR merged, comfortable with team

### Learning Objectives (40% of time)

- [ ] Review Grey Haven architecture documentation
- [ ] Watch recorded tech talks on stack ([TanStack Start / FastAPI / Cloudflare Workers])
- [ ] Read code review guidelines and PR process
- [ ] Study [specific technology] documentation
- [ ] Understand multi-tenant architecture (RLS, tenant_id)

### Doing Objectives (60% of time)

- [ ] Complete "good-first-issue" (Linear label: `onboarding`, `good-first-issue`)
- [ ] Shadow buddy on code review (watch, ask questions)
- [ ] Pair program on small feature with buddy
- [ ] Write tests for your changes (aim for 100% coverage)
- [ ] Deploy to staging environment with buddy
- [ ] Present learnings in Friday standup (5 min)

### Daily Schedule

**Monday - Friday**:
- Morning standup (9:00 AM)
- Focus work (blocks of 2-3 hours)
- Buddy check-in (4:00 PM, 15 minutes)

**Suggested First Issue** (assign on Day 1):
- [Issue ID]: [Simple UI improvement / Documentation update / Small bug fix]
- Expected completion: End of Week 1
- Buddy: Available for pairing anytime

### Week 1 Milestone: First PR Merged ✅

**Success Criteria**:
- PR merged and deployed
- Tests written and passing
- < 2 rounds of feedback (indicates good mentorship)
- Code follows team standards

---

## Week 2-4: Building Momentum

**Goal**: Independent contribution on small features

### Technical Growth

- [ ] Own 2-3 Linear issues independently (no pairing needed)
- [ ] Participate in sprint planning (understand scope and estimation)
- [ ] Review others' PRs (start giving feedback, learn by reviewing)
- [ ] Write tests for all features (maintain 80%+ coverage)
- [ ] Document a process you learned (share knowledge back)

### Team Integration

- [ ] Lead daily standup once (practice communication)
- [ ] Coffee chat with 2-3 team members (build relationships)
- [ ] Attend design discussion (even if just listening)
- [ ] Ask questions in team chat (model curiosity)

### Buddy Schedule

**Week 2-4**: Check-ins 2-3x per week (Monday, Wednesday, Friday)
- Progress on current work
- Any blockers or confusion
- Feedback on PRs
- Growing independence

### Week 4 Milestone: First Feature Shipped ✅

**Success Criteria**:
- Shipped 2-3 features independently
- Growing confidence
- Asking good questions
- Team integration strong

---

## 30-Day Milestone

**Date**: [30 days from start date]

**Manager 1:1**: 45 minutes

### Review Topics

**Technical Progress**:
- Velocity: [X issues completed, target: Y]
- Code quality: [Avg feedback rounds per PR]
- Test coverage: [Percentage]
- Architecture understanding: [Assessment]

**Team Integration**:
- Comfortable asking questions? [Yes/No]
- Building relationships? [Assessment]
- Contributing to discussions? [Assessment]
- Team feedback: [Summary from buddy and peers]

**Feedback Session**:
- What's going well?
- What's challenging?
- What support do you need?
- Manager feedback and coaching
- Next 30 days focus areas

### Success Criteria for 30 Days

**Junior Engineers**:
- Velocity: 40-60% of team average
- Shipped 3-5 features independently
- Code quality consistent (< 2 feedback rounds)
- Comfortable with team

**Mid-Level Engineers**:
- Velocity: 60-80% of team average
- Shipped 5-7 features, some medium complexity
- Leading small features end-to-end
- Contributing to code reviews

**Senior Engineers**:
- Velocity: 80-100% of team average
- Leading medium/complex features
- Architectural contributions
- Mentoring others

---

## 60-Day Milestone

**Date**: [60 days from start date]

**Manager 1:1**: 45 minutes

### Review Topics

**Technical Depth**:
- Leading medium features end-to-end
- Understanding architectural tradeoffs
- Proactively improving code quality
- Technical expert in one area

**Leadership** (Mid/Senior):
- Mentoring newer team members
- Leading design discussions
- Contributing to architecture decisions
- Improving team processes

**Career Discussion**:
- What do you want to be known for?
- What skills to develop next?
- 6-12 month trajectory
- How can I support your growth?

### Success Criteria for 60 Days

**Junior Engineers**:
- Velocity: 70-80% of team average
- Owning medium features
- Mentoring next junior hire
- Strong team integration

**Mid-Level Engineers**:
- Velocity: 90-100% of team average
- Leading medium features
- Technical depth in 1-2 areas
- Contributing to architecture

**Senior Engineers**:
- Velocity: 100-120% of team average + force multiplier
- Leading complex features
- Architectural contributions
- Mentoring 1-2 engineers

---

## 90-Day Milestone

**Date**: [90 days from start date]

**Formal Performance Review**: 60 minutes

### Review Topics

**Performance Assessment**:
- Technical contributions (features shipped, impact)
- Code quality and velocity
- Team collaboration
- Growth trajectory

**Performance Rating**: [Scale 1-10]
- 9-10: Exceptional (promoting, fast-track)
- 8-9: Strong (exceeding expectations)
- 7-8: Solid (meeting expectations)
- 6-7: Concerns (improvement needed)
- < 6: Not meeting bar (PIP or exit)

**Future Planning**:
- Career trajectory (promotion timeline)
- Development plan (skills to build)
- Next 6 months goals
- Support and resources

### Success Criteria for 90 Days

**All Levels**:
- Fully productive team member
- Velocity at or above team average (for level)
- Handling full complexity range
- Positive team culture impact
- Clear strengths identified

---

## Onboarding Resources

### Documentation
- Architecture: [link to architecture docs]
- Development workflow: [link to workflow docs]
- Code standards: [link to code style guide]
- Testing guide: [link to testing docs]

### Tools
- Linear: [workspace link]
- GitHub: [org link]
- Slack: [workspace link]
- Claude Code: [plugin marketplace link]

### People
- **Manager**: [Name] - Career, performance, team questions
- **Buddy**: [Name] - Daily technical help, safe space for questions
- **Tech Lead**: [Name] - Architecture, complex technical questions
- **Team**: #[team-channel] on Slack

### Common Questions

**Q: When should I ask for help?**
A: Immediately! Try for 15-30 minutes, then ask. Don't struggle for hours.

**Q: How do I know if my PR is ready?**
A: Tests passing, lint passing, you've self-reviewed. Then create PR.

**Q: What if I disagree with PR feedback?**
A: Ask questions! "Why do you suggest this?" Dialog is good.

**Q: How do I handle mistakes?**
A: Everyone makes them. Own it, fix it, learn from it. No blame culture.

---

## Emergency Contacts

- **IT Issues**: it@greyhaven.io
- **HR Questions**: hr@greyhaven.io
- **Manager**: [manager-email@greyhaven.io](mailto:manager-email@greyhaven.io) (Slack: @[manager])
- **Buddy**: [buddy-email@greyhaven.io](mailto:buddy-email@greyhaven.io) (Slack: @[buddy])

---

**Template Version**: 2.0
**Last Updated**: 2025-01-07

Related: [Buddy Checklist Template](buddy-checklist-template.md) | [Milestone Check-in Templates](milestone-check-in-templates.md) | [Return to INDEX](INDEX.md)
