# Buddy System Guide

Comprehensive guide to implementing and maintaining an effective buddy system for developer onboarding.

## What is a Buddy System?

**Buddy**: A peer (not manager, not senior mentor) assigned to help new hire navigate first 90 days

**Purpose**:
- Provide safe space for "basic" questions
- Share tactical knowledge (where things are, how team works)
- Build social connection (friend at work = retention)
- Model team culture (how we really work vs documentation)

**Not a Buddy**:
- Not their manager (power dynamic inhibits questions)
- Not their mentor (buddies are tactical, mentors are strategic)
- Not their tech lead (buddies are peers, not evaluators)

## Buddy Selection Criteria

### Must-Have Qualities

1. **Patience**: Doesn't mind answering same question 3 times
2. **Empathy**: Remembers being confused and lost
3. **Communication**: Can explain concepts clearly
4. **Availability**: Has bandwidth for daily check-ins
5. **Voluntary**: Wants to do it (not forced)

### Experience Level

**Ideal**: 1-3 years at company
- Not too junior (remembers onboarding but has knowledge)
- Not too senior (peers feel less intimidating)

**Examples**:
- ✅ Sarah (2 years, mid-level) → Great buddy for Alex (junior)
- ✅ Marcus (3 years, senior) → Great buddy for Jordan (senior peer)
- ❌ CTO → Too senior, power dynamic
- ❌ New hire from 6 months ago → Too junior, limited knowledge

### Selection Process

```bash
# Step 1: Identify potential buddies
CANDIDATES=(
  "Sarah Martinez (2 years, frontend)"
  "Mike Chen (3 years, backend)"
  "Lisa Park (2 years, full-stack)"
)

# Step 2: Ask for volunteers
# Send email: "Would you like to buddy with our new hire?"

# Step 3: Match based on:
# - Technical alignment (frontend buddy for frontend hire)
# - Personality fit (energetic buddy for shy new hire)
# - Availability (not on critical deadline)
```

## Buddy Responsibilities by Week

### Week 1: Daily Check-ins (15 min/day)

**Monday (Day 1)**:
```
Buddy: "Hi! I'm Sarah, your buddy for the next few months."
Buddy: "My role is to help you with anything - no question is too small."
Buddy: "Let's pair on environment setup now, then daily check-ins at 4 PM."

[Pair on setup for 2 hours]

Buddy [4 PM]: "How was your first day?"
New hire: "Overwhelming but exciting!"
Buddy: "That's normal. Tomorrow we'll work on your first issue together."
```

**Tuesday-Friday**:
```
Daily 4 PM check-in (15 minutes):
- How was today?
- Any questions before EOD?
- What's on your plate for tomorrow?
- Need any unblocking?

Examples:
- "How do I run tests again?" → Show them, write it down
- "I'm stuck on this bug" → Pair debug for 30 min
- "Is it okay to push to main?" → Explain branch workflow
```

**End of Week 1 Retrospective**:
```
Buddy: "You made it through Week 1! Let's reflect."

What went well?
- "Environment setup was smooth"
- "First PR merged!"

What was hard?
- "TanStack Query syntax confusing"
- "Not sure when to ask for help"

Next week:
- "I'll share some TanStack Query resources"
- "Ask me anytime - Slack, tap my shoulder, whatever"
```

### Week 2-4: Check-ins 2-3x/week (20 min each)

**Monday/Wednesday/Friday Pattern**:
```
Monday: "How was the weekend? What are you working on this week?"
Wednesday: "How's the feature going? Any blockers?"
Friday: "What did you ship this week? Anything for next week?"
```

**During Week 2-4**:
- [ ] Review every PR (detailed feedback, not just LGTM)
- [ ] Pair program 1-2 times per week
- [ ] Introduce to other team members
- [ ] Include in relevant meetings
- [ ] Share context ("Why we made this decision")

**Example PR Review** (Week 2):
```
Sarah's Review on Alex's PR:

Great work! A few things to improve:

1. Tests: Add test for error case (when API fails)
   Why: We test happy path AND error path

2. Naming: `handleClick` → `handleLoginSubmit`
   Why: Specific names are more maintainable

3. Accessibility: Add aria-label to button
   Why: Screen readers need text

Let me know if you want to pair on the tests!

Approved after changes.
```

### Week 5-8: Weekly Check-ins (30 min)

**Focus Shifts**:
- Less tactical ("how do I...") → More strategic ("should I...")
- Less pair programming → More architecture discussions
- Less hand-holding → More independence

**Weekly Check-in Template**:
```
Buddy: "What did you ship this week?"
New hire: "I finished the user profile editor!"

Buddy: "Nice! What was challenging?"
New hire: "Form validation was tricky."

Buddy: "What are you working on next?"
New hire: "Dashboard redesign - it's complex."

Buddy: "Want to review your approach together?"
New hire: "Yes, that would help."

[30 min architecture discussion]
```

### Week 9-12: Bi-weekly Check-ins (casual)

**Transition to Independence**:
- Formal buddy relationship ending
- Continuing as colleagues/friends
- Check-ins become organic, not scheduled

**Final Check-in** (Week 12):
```
Buddy: "You've come so far since Day 1!"
New hire: "I was so nervous. Thanks for everything."

Buddy: "What helped most?"
New hire: "Daily check-ins Week 1. Knowing you had my back."

Buddy: "What advice for next new hire?"
New hire: "Ask questions early. Everyone wants to help."

Buddy: "We're colleagues now. Still here if you need me."
```

## Buddy Training

### Pre-Buddy Orientation (30 minutes)

**Topics to Cover**:
1. **Your Role**: Peer support, not evaluation
2. **Time Commitment**: 15 min/day Week 1, decreasing over time
3. **Boundaries**: Escalate to manager if performance issues
4. **Resources**: Onboarding checklist, buddy guide, Linear issues

**Training Script**:
```
Manager: "Thanks for volunteering to buddy with Alex!"

Manager: "Your role is tactical support - answer questions, pair program, share context. You're not evaluating them - I handle performance."

Manager: "Week 1 is most intense: daily 15-min check-ins. After that, 2-3x/week, then weekly."

Manager: "If you notice red flags (not asking questions, missing deadlines), tell me. But your job is support, not assessment."

Manager: "Any questions?"

Buddy: "What if they ask something I don't know?"

Manager: "Perfect - figure it out together or find someone who knows. That models learning."
```

### Buddy Resources Checklist

Provide buddies with:
- [ ] Onboarding timeline (Day 1, Week 1, 30/60/90)
- [ ] New hire's Linear issues (so you know their tasks)
- [ ] Team documentation (architecture, processes)
- [ ] Communication guidelines (when to Slack vs pair)
- [ ] Escalation process (when to involve manager)

## Common Buddy Challenges

### Challenge 1: "They're not asking questions"

**Red Flag**: New hire seems to understand everything (they don't)

**Why It Happens**:
- Fear of looking stupid
- Impostor syndrome
- Cultural norms ("don't bother people")

**Solution**:
```
Buddy: "You haven't asked any questions today. That's unusual."
New hire: "I didn't want to bother you."
Buddy: "My job is to be bothered! Seriously, ask me 100 questions."

[Proactively offer]
Buddy: "This is confusing - let me explain how it works."
[Models that confusion is normal]
```

### Challenge 2: "I don't have time"

**Red Flag**: Buddy skipping check-ins, rushing through reviews

**Why It Happens**:
- Underestimated time commitment
- Poor time management
- Critical deadline

**Solution**:
```
Buddy → Manager: "I'm swamped with Project X. Can we push back or reassign?"

Manager: "Let's reduce to 2x/week this week. I'll handle extra check-ins."

OR

Manager: "Let's find a different buddy. Thanks for being honest."
```

### Challenge 3: "We're not clicking"

**Red Flag**: Awkward interactions, new hire not opening up

**Why It Happens**:
- Personality mismatch
- Communication style differences
- Chemistry just isn't there

**Solution**:
```
Manager [to buddy]: "How's it going with Alex?"
Buddy: "Okay, but... we're not really connecting."

Manager: "That happens. Let's add a second buddy - Mike from backend. Sometimes new hires connect better with someone else."

[Add Mike as secondary buddy]

Result: Alex connects with Mike, Sarah steps back gracefully.
```

## Buddy Success Metrics

### Quantitative Metrics

**New Hire Outcomes**:
- Time to first PR: < 3 days
- PR feedback rounds: < 2 (well-mentored = fewer iterations)
- Questions asked: 10+/week (high = psychological safety)
- 30-day satisfaction: 4.5+/5

**Buddy Feedback**:
- Buddy satisfaction: 4+/5
- Would buddy again: Yes
- Time commitment acceptable: Yes

### Qualitative Feedback

**Good Signs**:
- "Sarah made me feel safe to ask anything"
- "Daily check-ins were a lifeline Week 1"
- "I learned more from pairing than docs"

**Warning Signs**:
- "I didn't want to bother my buddy"
- "Check-ins felt rushed"
- "I was on my own after Week 1"

## Buddy Recognition

**Why Recognize Buddies**:
- Buddying is extra work (acknowledge it)
- Models that mentorship is valued
- Encourages future volunteering

**Recognition Ideas**:
- Public shout-out in team meeting
- Written thank-you in performance review
- "Mentor of the Quarter" award
- Bonus or spot award
- Extra PTO day

**Example Recognition**:
```
Manager [in team meeting]:
"I want to recognize Sarah for amazing buddy work with Alex.
Alex shipped their first feature in Week 2 - that's Sarah's impact.
Thanks for investing in our team."

[Team applause]
```

## Buddy FAQs

**Q: What if my buddy is struggling?**
A: Tell their manager immediately. Don't wait for 30-day review.

**Q: What if they're not doing their work?**
A: Not your problem - tell manager. Your role is support, not evaluation.

**Q: What if they ask me something I don't know?**
A: "Great question! I don't know, let's find out together." Models learning.

**Q: How much time will this take?**
A: Week 1: ~2 hours/day. Week 2-4: ~3 hours/week. Week 5+: ~1 hour/week.

**Q: What if I'm too busy to buddy right now?**
A: Tell manager before committing. Declining is better than half-assing.

**Q: Can I buddy with someone on a different team?**
A: Yes, but also assign a same-team buddy for technical questions.

**Q: Should I be friends with my buddy?**
A: Friendly, yes. Best friends, not necessary. Professional support is enough.

## Buddy Checklist

### Week 1
- [ ] Introduce yourself (email before Day 1)
- [ ] Pair on environment setup (Day 1)
- [ ] Daily 15-min check-ins (4 PM)
- [ ] Pair on first issue
- [ ] Review first PR with detailed feedback
- [ ] Introduce to 2-3 team members
- [ ] End-of-week retrospective

### Week 2-4
- [ ] Check-ins 2-3x/week
- [ ] Review every PR
- [ ] Pair program 1-2x/week
- [ ] Share team context and history
- [ ] Include in team activities

### Week 5-8
- [ ] Weekly check-ins
- [ ] Architecture discussions
- [ ] Encourage independence
- [ ] Introduce to other teams

### Week 9-12
- [ ] Bi-weekly check-ins
- [ ] Transition to peer relationship
- [ ] Final check-in (Week 12)
- [ ] Provide feedback to manager

---

Related: [Onboarding Best Practices](onboarding-best-practices.md) | [Linear API Patterns](linear-api-patterns.md) | [Milestone Tracking](milestone-tracking.md) | [Return to INDEX](INDEX.md)
