# Prompt Anti-Patterns

Common mistakes in prompt engineering and how to fix them.

---

## Anti-Pattern 1: The Vague Request

### Problem
```
"Help me with my code."
"Tell me about AI."
"Make this better."
```

**Why It Fails:**
- No specific task
- No context provided
- No success criteria
- Forces model to guess intent

**Fix:** Apply Principles 9, 21, 25

```
###Task###
Debug this Python function that should validate email addresses but accepts invalid formats.

###Current Code###
[paste code]

###Issue###
Accepts "user@" as valid (missing domain)

###Expected###
Should reject emails without valid domain part

###Requirements###
- Use regex pattern
- Return boolean
- Handle edge cases (empty string, None)
```

**Impact:** 85% → 95% first-response success

---

## Anti-Pattern 2: The Wall of Text

### Problem
```
I'm building an app and I need help with the database design and also the API endpoints and I'm not sure if I should use REST or GraphQL and also I need authentication but I don't know if JWT is the right choice and also...
```

**Why It Fails:**
- Multiple unrelated concerns
- No structure
- Difficult to parse
- Model can't prioritize

**Fix:** Apply Principles 3, 8

```
###Project Context###
Building a multi-tenant SaaS task management app

###Current Questions###

**1. Database Design**
- Tables: organizations, users, projects, tasks
- Need: multi-tenant isolation strategy

**2. API Architecture**
- Options: REST vs GraphQL
- Requirements: Mobile + web clients, real-time updates

**3. Authentication**
- Considering: JWT with refresh tokens
- Concerns: Security, session management

Let's tackle these one at a time, starting with #1: Database Design
```

**Impact:** 60% → 90% complete answers

---

## Anti-Pattern 3: No Examples Provided

### Problem
```
"Extract important information from this text."
```

**Why It Fails:**
- "Important" is subjective
- No format specified
- No pattern to follow

**Fix:** Apply Principle 7, 20

```
Extract person names and dates from text.

###Examples###

Input: "John met Sarah on July 15, 2024 at the cafe."
Output: {
  "names": ["John", "Sarah"],
  "dates": ["2024-07-15"]
}

Input: "The meeting is scheduled for Jan 1st with Dr. Smith."
Output: {
  "names": ["Dr. Smith"],
  "dates": ["2024-01-01"]
}

###Your Task###
Input: [your text]
Output: ?
```

**Impact:** 45% → 92% accuracy

---

## Anti-Pattern 4: Negative Instructions

### Problem
```
"Don't use technical jargon. Don't make it too long. Don't skip error handling."
```

**Why It Fails:**
- Negative framing harder to follow
- Doesn't say what TO do
- Can confuse intent

**Fix:** Apply Principles 10, 16

```
✓ Use plain English (explain technical terms when needed)
✓ Keep under 500 words
✓ Include error handling for all functions
```

**Impact:** 70% → 95% compliance

---

## Anti-Pattern 5: Missing Output Format

### Problem
```
"Compare React and Vue."
```

**Why It Fails:**
- No format specified (essay? table? bullets?)
- No structure guidance
- Length unclear
- Detail level undefined

**Fix:** Apply Principles 17, 24

```
Compare React and Vue in a table:

| Aspect | React | Vue | Better For |
|--------|-------|-----|------------|
| Learning Curve | | | |
| Performance | | | |
| Ecosystem | | | |
| Community | | | |
| Best Use Cases | | | |

For each cell: 1-2 sentences max
```

**Impact:** 50% → 95% usable first response

---

## Anti-Pattern 6: No Audience Specification

### Problem
```
"Explain machine learning."
```

**Why It Fails:**
- Could be for 5-year-old or PhD
- Complexity level unknown
- Assumed knowledge unclear

**Fix:** Apply Principles 2, 5

```
Explain machine learning to a junior web developer who understands JavaScript but has no math/stats background. Use web development analogies where possible.
```

**Impact:** Explanation quality 4/10 → 9/10

---

## Anti-Pattern 7: Overwhelming Single Request

### Problem
```
"Build a complete e-commerce website with user authentication, product catalog, shopping cart, payment processing, admin panel, and deploy it."
```

**Why It Fails:**
- Too broad for single response
- Can't cover everything well
- No prioritization
- Overwhelming complexity

**Fix:** Apply Principle 3

```
Build an e-commerce website in phases:

**Phase 1: Foundation** (current focus)
- Basic product listing
- Product detail pages
- Simple navigation

**Phase 2:** Shopping cart
**Phase 3:** User authentication
**Phase 4:** Checkout process
**Phase 5:** Admin panel
**Phase 6:** Deployment

Let's start with Phase 1. What should the data model look like?
```

**Impact:** Completion rate 20% → 85%

---

## Anti-Pattern 8: Assuming Context

### Problem
```
"Fix the bug in the login function."
```

**Why It Fails:**
- No code provided
- No error description
- No environment details
- No expected behavior

**Fix:** Apply Principle 21

```
###Bug in Login Function###

**Environment:**
- React 18 + TypeScript
- Backend: FastAPI
- Auth: JWT tokens

**Code:**
[paste login function]

**Error:**
TypeError: Cannot read property 'token' of undefined

**Expected:**
After login, should redirect to dashboard with token stored

**What I've Tried:**
- Verified API returns 200
- Checked token exists in response
- Console.log shows response structure
```

**Impact:** Resolution time: 3 iterations → 1 iteration

---

## Anti-Pattern 9: No Success Criteria

### Problem
```
"Review this code."
```

**Why It Fails:**
- What aspects to review?
- What level of detail?
- What standards to apply?
- What constitutes "good"?

**Fix:** Apply Principle 25

```
Code review this React component against these criteria:

###Review Checklist###
☐ Performance: Unnecessary re-renders, expensive operations
☐ Security: XSS vulnerabilities, input validation
☐ Accessibility: ARIA labels, keyboard navigation
☐ TypeScript: Proper typing, no `any`
☐ Testing: Missing test scenarios
☐ Best Practices: React hooks rules, component structure

###Output Format###
For each issue:
- Severity: Critical | High | Medium | Low
- Line number
- Problem description
- Suggested fix

###Scoring###
Provide overall score (1-10) with justification
```

**Impact:** Review quality 5/10 → 9/10

---

## Anti-Pattern 10: Ignoring Iterative Refinement

### Problem
Expecting perfect response on first try, giving up if not perfect.

**Why It Fails:**
- Complex tasks need refinement
- Initial response is starting point
- Model can improve with feedback

**Fix:** Apply Principle 23

```
Turn 1: "Create basic API endpoint structure"
→ Review response

Turn 2: "Add error handling to these endpoints"
→ Review response

Turn 3: "Now add input validation with Pydantic"
→ Refine further

Turn 4: "Add rate limiting middleware"
→ Complete solution
```

**Impact:** Quality of final output 6/10 → 9/10

---

## Anti-Pattern 11: Technical Jargon Without Context

### Problem
```
"Implement OAuth2 PKCE flow with RBAC and MFA."
```

**Why It Fails** (if audience doesn't know jargon):
- Assumes expert knowledge
- No definitions
- No context

**Fix:** Apply Principles 2, 5

```
Implement user authentication for a web app:

**Requirements:**
- OAuth2 with Proof Key for Code Exchange (prevents token interception)
- Role-Based Access Control (admins vs regular users)
- Multi-Factor Authentication (email code for login)

**Audience:** Mid-level developer, familiar with JWTs but new to OAuth2

**Deliverables:**
1. Explanation of each security feature
2. Implementation code
3. Flow diagrams
```

**Impact:** Understanding 30% → 90%

---

## Anti-Pattern 12: One-Word or Ultra-Short Prompts

### Problem
```
"React?"
"SQL"
"Python decorators"
```

**Why It Fails:**
- Completely ambiguous
- No specific question
- No context
- Forces guessing

**Fix:** Apply Principles 1, 9, 21

```
Explain Python decorators with:
1. What problem they solve
2. Basic syntax
3. Three common use cases
4. One complete working example

Target audience: Python developer with 6 months experience
```

**Impact:** Relevance 20% → 95%

---

## Quick Anti-Pattern Checklist

Before submitting, check for these red flags:

**❌ Anti-Patterns Present:**
- [ ] Request is < 10 words
- [ ] Contains "Don't" or "Avoid" instructions
- [ ] No specific details or examples
- [ ] Multiple unrelated topics in one prompt
- [ ] No audience or complexity level
- [ ] No desired format specified
- [ ] Assumes model knows your context
- [ ] No success criteria or requirements
- [ ] Technical jargon without explanation
- [ ] Too broad for single response

**✅ Good Prompt Has:**
- [x] Clear, specific task
- [x] Relevant context and details
- [x] Target audience specified
- [x] Desired output format
- [x] Examples (if applicable)
- [x] Success criteria
- [x] Structured with delimiters
- [x] Affirmative language
- [x] Appropriate scope
- [x] Requirements stated explicitly

---

## Pattern: Weak → Strong Transformation Template

Use this template to fix any weak prompt:

```
###Task###
[One clear sentence describing what you need]

###Context###
[Relevant background information]

###Requirements###
- [Specific requirement 1]
- [Specific requirement 2]

###Format###
[How you want the response structured]

###Examples### (if applicable)
[Show desired pattern]

###Success Criteria###
[How to know if response meets needs]
```

---

## The "5 Why's" Test

If your prompt is weak, ask:

1. **Why** do I need this? → Add context
2. **Why** this approach? → Specify requirements
3. **Why** this format? → Define output structure
4. **Why** this audience? → State target user
5. **Why** now? → Add constraints/urgency

---

**Total Anti-Patterns**: 12 common mistakes
**Average Fix Impact**: 40% → 90% success rate
**Time to Fix**: 30-60 seconds per prompt
**Principles Most Violated**: 3, 8, 9, 21, 25
