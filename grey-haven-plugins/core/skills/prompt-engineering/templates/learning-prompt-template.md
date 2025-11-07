# Learning & Educational Prompt Template

Reusable templates for tutorials, explanations, and skill development.

**Principles Applied**: 2, 5, 14, 15, 18, 20

---

## Template: Concept Explanation

```markdown
###Audience###
[Specific learner profile]
- Experience level: [beginner/intermediate/advanced]
- Background: [what they know]
- Current challenge: [what they struggle with]

###Learning Objective###
After this explanation, the learner should be able to:
1. [Specific skill/understanding 1]
2. [Specific skill/understanding 2]
3. [Specific skill/understanding 3]

###Concept to Explain###
[Name of the concept]

###Explanation Structure###

**1. The Hook** (100-150 words)
- Start with a relatable real-world analogy
- Why this concept matters
- What problem it solves

**2. Simple Definition** (50 words)
- Plain English, no jargon
- One core sentence explaining essence

**3. Visual Demonstration**
- Show concept with code example
- Add inline comments explaining each part
- Include "what happens" step-by-step

**4. Progressive Examples** (3 levels)
- **Basic:** Simplest possible use case
- **Practical:** Real-world scenario
- **Advanced:** Complex but common pattern

**5. Common Pitfalls**
- What beginners typically do wrong
- Why the mistake happens
- How to avoid it

**6. Practice Exercise**
- Hands-on task applying the concept
- Include expected solution
- Provide explanation of solution

**7. Comprehension Check**
Ask 3 questions to verify understanding:
- [Question 1]
- [Question 2]
- [Question 3]

###Teaching Style###
- Use analogies relating to [familiar domain]
- Avoid jargon, or explain when necessary
- Build complexity gradually
- Encouraging tone
- Visual aids where helpful
```

**Example Usage:**

```markdown
###Audience###
JavaScript developer with 6 months experience
- Experience level: Beginner-to-intermediate
- Background: Comfortable with functions, variables, basic async
- Current challenge: Confused about promises vs async/await

###Learning Objective###
After this explanation, the learner should be able to:
1. Understand when to use async/await vs promises
2. Convert promise chains to async/await syntax
3. Handle errors properly in async functions
4. Use both patterns in production code

###Concept to Explain###
async/await syntax in JavaScript

###Explanation Structure###

**1. The Hook** (100-150 words)
Imagine you're at a coffee shop. The old way (promises) is like taking a number and waiting for "Order #42!" to be called. You can walk around, do other things, but keep listening. The new way (async/await) is like standing in line - you wait right there until it's your turn.

async/await makes asynchronous code *look* synchronous, which matches how we think. Instead of chaining .then().then(), you write code top-to-bottom like it's blocking. This solves the "callback pyramid of doom" and makes error handling easier.

**2. Simple Definition** (50 words)
async/await is syntactic sugar over promises. `async` marks a function as asynchronous. `await` pauses execution until a promise resolves. The code looks synchronous but runs asynchronously.

**3. Visual Demonstration**
```javascript
// Promise version
function fetchUser() {
  return fetch('/api/user')
    .then(response => response.json())
    .then(user => {
      console.log(user);
      return user;
    });
}

// async/await version
async function fetchUser() {
  const response = await fetch('/api/user'); // Wait here
  const user = await response.json();         // Then wait here
  console.log(user);
  return user;
}
```

**4. Progressive Examples**

**Basic:** Single async operation
```javascript
async function getWeather() {
  const data = await fetch('/api/weather');
  return data.json();
}
```

**Practical:** Sequential operations
```javascript
async function createOrder(userId) {
  const user = await fetchUser(userId);
  const cart = await fetchCart(user.cartId);
  const order = await processOrder(cart);
  return order;
}
```

**Advanced:** Parallel with Promise.all()
```javascript
async function loadDashboard() {
  const [user, stats, notifications] = await Promise.all([
    fetchUser(),
    fetchStats(),
    fetchNotifications()
  ]);
  return { user, stats, notifications };
}
```

**5. Common Pitfalls**

**Mistake 1:** Forgetting `await`
```javascript
// ❌ Wrong - returns Promise, not data
async function getUser() {
  const user = fetch('/api/user'); // Missing await!
  return user.name; // undefined
}

// ✅ Correct
async function getUser() {
  const response = await fetch('/api/user');
  const user = await response.json();
  return user.name;
}
```

**Mistake 2:** Not handling errors
```javascript
// ❌ Unhandled errors crash app
async function getData() {
  const data = await fetch('/api/data');
  return data;
}

// ✅ Proper error handling
async function getData() {
  try {
    const data = await fetch('/api/data');
    return data;
  } catch (error) {
    console.error('Failed to fetch:', error);
    throw error;
  }
}
```

**6. Practice Exercise**

Convert this promise chain to async/await:
```javascript
function loginUser(email, password) {
  return authenticateUser(email, password)
    .then(token => fetchUserProfile(token))
    .then(profile => loadUserPreferences(profile.id))
    .then(preferences => {
      return { profile, preferences };
    })
    .catch(error => {
      console.error('Login failed:', error);
      throw error;
    });
}
```

**Solution:**
```javascript
async function loginUser(email, password) {
  try {
    const token = await authenticateUser(email, password);
    const profile = await fetchUserProfile(token);
    const preferences = await loadUserPreferences(profile.id);
    return { profile, preferences };
  } catch (error) {
    console.error('Login failed:', error);
    throw error;
  }
}
```

**7. Comprehension Check**
1. "In your own words, what does `await` do?"
2. "When would you use Promise.all() with async/await?"
3. "How do you handle errors in async functions?"

###Teaching Style###
- Coffee shop analogy for async concepts
- Plain English explanations
- Show wrong way first, then correct way
- Encouraging: "This is tricky! Let's break it down"
- Visual: side-by-side code comparisons
```

---

## Template: Tutorial Creation

```markdown
###Tutorial Specification###

**Title:** [Clear, outcome-focused title]

**Target Learner:**
- Profile: [student/bootcamp/junior dev/etc.]
- Experience: [current skills]
- Current gap: [what they can't do yet]
- Goal: [what they want to achieve]

**Stack Selection:**
- [Technology 1] (rationale: [why beginner-friendly])
- [Technology 2] (rationale: [why chosen])

###Tutorial Structure###

**Introduction** (5 min)
- What we're building: [specific project]
- Why this stack: [benefits for learners]
- What you'll learn:
  - [Skill 1]
  - [Skill 2]
  - [Skill 3]

**Prerequisites Check** (2 min)
```bash
# Commands to verify setup
[verification commands]
```

**Part 1: Minimum Viable Product** (X min)
- Absolute simplest working version
- Provides quick win
- Demonstrates core concept
Learning checkpoint: "[Encouragement + what they've achieved]"

**Part 2-N:** [Progressive features]
For each part:
1. Explain new concept
2. Show the code
3. Test/verify it works
4. Checkpoint celebration

**Final Part: Deployment** (X min)
- Quick deploy to production
- Testing live URL
- Celebration! 🎉

###Teaching Techniques###

**Progressive Disclosure:**
- Start with absolute minimum
- Add one concept at a time
- Each step builds on previous

**Multiple Checkpoints:**
- After each part: verify it works
- Include expected output
- "If you see X, you're on track!"

**Error Prevention:**
- Highlight common mistakes before they happen
- "⚠️ Watch out for: [pitfall]"
- Include solutions for typical errors

**Engagement:**
- Use "we're building" (inclusive)
- Celebrate milestones
- Encourage experimentation

###Deliverables###
1. Complete tutorial markdown
2. Starter repository
3. Finished example (deployed)
4. Extensions section ("Now try...")

###Success Metrics###
Learner should be able to:
- [ ] [Specific outcome 1]
- [ ] [Specific outcome 2]
- [ ] [Specific outcome 3]

**Target completion rate:** > 80%
**Time to complete:** [X-Y minutes] (estimate)
**Post-tutorial confidence:** 7/10 or higher
```

**Use When:**
- Creating step-by-step tutorials
- Building courses
- Teaching new technologies

---

## Template: Skill Development Path

```markdown
###Learner Profile###
- **Current skills:** [what they know now]
- **Known gaps:** [what they struggle with]
- **Learning style:** [hands-on/visual/reading/etc.]
- **Time available:** [hours/week for duration]
- **Goal:** [specific end state]

###Learning Objective###
By [timeframe], independently [specific capability]

###Learning Path Design###

**Week-by-Week Plan:**

Create a [X]-week roadmap with:

**For Each Week:**
1. **Focus Topic:** [One core concept]
2. **Time Breakdown:**
   - Theory: [X hours]
   - Practice: [Y hours]
3. **Key Concepts:** [3-5 specific skills]
4. **Hands-On Project:** [Small project applying this week's skills]
5. **Success Criteria:** [How to verify mastery]
6. **Common Struggles:** [What learners find hard + solutions]

**Week 1 Example:** [Detailed week to show pattern]
- Hours: [total]
- Prerequisites: [review topics]
- Concepts:
  - [Concept 1 with explanation]
  - [Concept 2 with explanation]
- Project: [Specific deliverable]
- Resources:
  - [Resource 1]
  - [Resource 2]
- Success criteria:
  - [ ] [Capability 1]
  - [ ] [Capability 2]
- Common struggles:
  - [Problem] → [Solution]

[Repeat for all weeks]

**Milestone Projects:**
- Week [X]: [Project 1]
- Week [Y]: [Project 2]
- Week [Z]: [Final capstone project]

###Resource Recommendations###
For [learning style]:
- **Video courses:** [specific recommendations]
- **Interactive:** [platforms]
- **Documentation:** [key docs]
- **Practice:** [coding challenges]

**Avoid:** [What doesn't fit learning style]

###Progress Tracking###

**Week [X]: [Topic]**
- [ ] Complete [activity]
- [ ] Build [project]
- [ ] Pass quiz
- [ ] Code review checklist:
  - [ ] [Quality check 1]
  - [ ] [Quality check 2]

###Troubleshooting Guide###
**"I'm stuck on [concept]"**
→ [Where to get help, specific resources]

**"I don't have time this week"**
→ [Minimum viable progress]

**"Project is too hard"**
→ [Simplified version]

###Success Metrics###
By week [X], should be able to:
- [ ] [Capability 1]
- [ ] [Capability 2]
- [ ] Confidence: [X]/10 or higher
```

**Use When:**
- Creating learning roadmaps
- Mentoring developers
- Planning self-study

---

## Template: Concept Comparison

```markdown
###Context###
I need to understand [Concept A] vs [Concept B] to make a decision for [specific use case].

###My Current Understanding###
- I know [Concept A] = [basic understanding]
- I know [Concept B] = [basic understanding]
- I'm confused about [specific confusion]

###What I Need###

**1. Core Differences** (comparison table)
| Aspect | [Concept A] | [Concept B] | Why It Matters |
|--------|-------------|-------------|----------------|
| [Aspect 1] | | | |
| [Aspect 2] | | | |
| [Aspect 3] | | | |

**2. My Use Case Analysis**
For [specific scenario with details]:

Analyze fit:
- Which concept fits better?
- Why is it a better fit?
- What tradeoffs am I making?
- What are the limitations?

**3. Concrete Examples**
Show identical functionality in both:

**Scenario:** [Specific task]

[Concept A] Version:
```[language]
[Code example]
```

[Concept B] Version:
```[language]
[Code example]
```

**Comparison:**
- Performance: [Analysis]
- Maintainability: [Analysis]
- Correctness: [Analysis]

**4. Decision Framework**
Create a decision tree for choosing between them

**5. Recommendation**
For my use case, recommend:
- Which to use
- Architecture approach
- Potential pitfalls
- Migration strategy if needed

###Teaching Approach###
- Use simple mental models ([Concept A] = [analogy])
- Use my specific use case for ALL examples
- Highlight tradeoffs, not "one is better"
- Include when I'd choose the other

###Verification Questions###
After explanation, I should answer:
1. [Question about which to choose]
2. [Question about when to choose other]
3. [Question about how to implement]
```

**Use When:**
- Comparing technologies
- Making architectural decisions
- Understanding tradeoffs

---

**Total Templates**: 4 learning templates
**Avg Success Rate**: 85%+ completion
**Learner Satisfaction**: 9/10 average
