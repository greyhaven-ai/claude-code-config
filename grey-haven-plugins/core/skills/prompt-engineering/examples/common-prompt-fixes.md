# Common Prompt Fixes - Quick Reference

Fast transformations for the most common prompt weaknesses. Copy-paste these patterns for immediate improvements.

---

## Fix 1: Add Specificity

### Pattern: Vague → Specific

**Before:**
```
Write about AI.
```

**After:**
```
Write a 500-word article about how generative AI is transforming software development, focusing on code completion tools like GitHub Copilot. Target audience: mid-level developers. Include 3 specific examples and cite recent studies from 2024.
```

**Principles:** 1 (concise), 2 (audience), 21 (detailed), 25 (requirements)

**Quick Template:**
```
Write a [length] [format] about [specific topic], focusing on [angle]. Target audience: [who]. Include [specific elements]. [Additional constraints].
```

---

## Fix 2: Break Down Complex Tasks

### Pattern: Single Request → Multi-Step

**Before:**
```
Create a full website for my business.
```

**After:**
```
Create a business website following these steps:

1. **Discovery:**
   - What: Coffee shop website
   - Goal: Online ordering + store locator
   - Pages needed: Home, Menu, Locations, Contact

2. **Design:**
   - Style: Modern, warm, mobile-first
   - Colors: Browns/creams (coffee theme)
   - Layout: Single-page scroll design

3. **Technical:**
   - Framework: React + TanStack
   - Features: Menu filtering, Google Maps integration
   - Hosting: Cloudflare Pages

4. **Content:**
   - Hero: "Artisan Coffee, Crafted Daily"
   - Menu: 15 items with photos
   - 3 locations with hours

Let's start with step 1: confirming requirements before design.
```

**Principles:** 3 (breakdown), 8 (structure), 12 (step-by-step), 21 (detail)

**Quick Template:**
```
Create [deliverable] following these steps:

1. **[Phase 1]:** [Specific tasks]
2. **[Phase 2]:** [Specific tasks]
3. **[Phase 3]:** [Specific tasks]

Let's start with step 1: [first action].
```

---

## Fix 3: Provide Examples

### Pattern: No Examples → Few-Shot Learning

**Before:**
```
Extract names from this text.
```

**After:**
```
Extract person names from the following text. Return as a JSON array.

###Examples###

Input: "John met Sarah at the cafe. They discussed the project with Michael."
Output: ["John", "Sarah", "Michael"]

Input: "The meeting included Dr. Smith, Prof. Johnson, and Ms. Lee."
Output: ["Dr. Smith", "Prof. Johnson", "Ms. Lee"]

###Text to Process###
[Your text here]

###Output Format###
Return only the JSON array, no additional text.
```

**Principles:** 7 (few-shot), 8 (delimiters), 17 (format), 20 (examples)

**Quick Template:**
```
[Task description]

###Examples###
Input: [example 1 input]
Output: [example 1 output]

Input: [example 2 input]
Output: [example 2 output]

###Your Input###
[actual input]

###Output Format###
[exact format specification]
```

---

## Fix 4: Add Structure with Delimiters

### Pattern: Wall of Text → Organized Sections

**Before:**
```
I need help with my Python code that reads a CSV file and processes the data to calculate statistics and then saves the results to a new file but I'm getting errors and don't know why.
```

**After:**
```
###Problem###
Python script fails when processing CSV data and saving results.

###Current Code###
[Paste code here]

###Error Message###
FileNotFoundError: [Errno 2] No such file or directory: 'output.csv'

###Expected Behavior###
1. Read data from input.csv
2. Calculate mean, median, mode
3. Save statistics to output.csv

###Environment###
- Python 3.11
- Libraries: pandas, numpy
- OS: macOS

###What I've Tried###
- Verified input.csv exists
- Checked file permissions
- Printed debug output (path looks correct)

###Question###
Why is the output file path not being created, and how do I fix it?
```

**Principles:** 8 (delimiters), 3 (breakdown), 21 (detail), 9 (direct)

**Quick Template:**
```
###Problem###
[One-line description]

###Code/Context###
[Relevant code or information]

###Error###
[Exact error message]

###Expected###
[What should happen]

###Environment###
[Relevant setup details]

###What I've Tried###
[Debugging steps taken]

###Question###
[Specific question]
```

---

## Fix 5: Specify Output Format

### Pattern: Any Format → Structured Output

**Before:**
```
Give me information about REST APIs.
```

**After:**
```
Create a REST API reference guide with this exact structure:

###Format###

**1. Overview** (100 words)
   - What is REST
   - Why use it

**2. HTTP Methods** (table format)
   | Method | Purpose | Example | Safe | Idempotent |
   |--------|---------|---------|------|------------|
   | GET    | [desc]  | [ex]    | Yes  | Yes        |
   [etc.]

**3. Status Codes** (grouped list)
   - 2xx Success: [codes with meanings]
   - 4xx Client Errors: [codes with meanings]
   - 5xx Server Errors: [codes with meanings]

**4. Best Practices** (numbered list)
   1. [Practice 1 with example]
   2. [Practice 2 with example]

**5. Code Example**
   ```typescript
   // Complete working example
   ```

Keep total length to 800-1000 words.
```

**Principles:** 8 (delimiters), 17 (format), 21 (detail), 25 (requirements)

**Quick Template:**
```
Create [topic] guide with this exact structure:

###Format###

**1. [Section 1]** ([constraint])
   - [Elements]

**2. [Section 2]** ([format type])
   [Format specification]

**3. [Section 3]** ([style])
   [Requirements]

[Overall constraints]
```

---

## Fix 6: Add Context and Audience

### Pattern: Generic → Targeted

**Before:**
```
Explain async/await.
```

**After:**
```
###Audience###
Junior developer with 6 months JavaScript experience, familiar with callbacks and promises, but struggling with async/await syntax.

###Goal###
Understand when and how to use async/await in real-world scenarios.

###Explanation Requirements###

1. **Concept Introduction** (200 words)
   - What problem async/await solves
   - How it relates to promises they already know

2. **Syntax Breakdown** (with annotations)
   ```javascript
   // Explain each line
   async function example() {
     const data = await fetch('...');
     return data;
   }
   ```

3. **Common Patterns** (3 examples)
   - Sequential API calls
   - Parallel operations with Promise.all()
   - Error handling with try/catch

4. **Common Mistakes** (what to avoid)
   - Forgetting await
   - Not handling errors
   - Blocking when you should be parallel

5. **Practice Exercise**
   - Convert callback code to async/await
   - Include solution

###Style###
- Use analogies (compare to real-world waiting)
- No jargon without explanation
- Include visual flow diagrams if helpful
- Encouraging tone
```

**Principles:** 2 (audience), 5 (clarity level), 3 (breakdown), 21 (detail), 11 (tone)

**Quick Template:**
```
###Audience###
[Experience level, background, current understanding]

###Goal###
[What they should be able to do after]

###Explanation Requirements###
1. [Section 1] ([constraints])
2. [Section 2] ([format])
3. [Section 3] ([examples])

###Style###
- [Tone/approach]
- [Language level]
- [Additional guidelines]
```

---

## Fix 7: Add Reasoning Instructions

### Pattern: Direct Answer → Explained Reasoning

**Before:**
```
Is this code secure?
```

**After:**
```
###Task###
Perform a security analysis of the following code, explaining your reasoning for each finding.

###Code###
[Code here]

###Analysis Approach###

For each potential issue:
1. Identify the code pattern
2. Explain why it's a security concern
3. Describe the attack scenario
4. Rate severity (Critical/High/Medium/Low)
5. Provide secure alternative with explanation

###Security Checklist###
☐ SQL injection vulnerabilities
☐ XSS (cross-site scripting)
☐ CSRF protection
☐ Input validation
☐ Output encoding
☐ Authentication/Authorization
☐ Secret management
☐ Error information disclosure

###Output Format###

**Issue 1: [Name]**
- **Location:** Line X
- **Pattern:** [What code is doing]
- **Why it's vulnerable:** [Explanation]
- **Attack scenario:** [How it could be exploited]
- **Severity:** [Level]
- **Fix:**
  ```typescript
  // Secure version with explanation
  ```

###Summary###
- Overall security score: X/10
- Critical issues: [count]
- Recommendation: [Deploy/Fix first/Refactor]

Think through each check systematically, explaining your security reasoning at each step.
```

**Principles:** 19 (chain-of-thought), 3 (breakdown), 12 (step-by-step), 17 (format), 8 (structure)

**Quick Template:**
```
###Task###
[Analysis task]

###Analysis Approach###
For each [item]:
1. [Observation step]
2. [Reasoning step]
3. [Impact step]
4. [Solution step]

###Checklist###
☐ [Item 1]
☐ [Item 2]

###Output Format###
[Structured format with reasoning sections]

Think through each check systematically, explaining your reasoning.
```

---

## Fix 8: Use Affirmative Instructions

### Pattern: Don't Do X → Do Y Instead

**Before:**
```
Write a tutorial. Don't make it too long. Don't use jargon. Don't skip the basics.
```

**After:**
```
Write a tutorial with these characteristics:

✓ Length: 800-1000 words (8-10 minute read)
✓ Language: Plain English, explain technical terms when first used
✓ Structure: Start with fundamentals before advanced concepts
✓ Include: Code examples, visual diagrams, real-world use case
✓ Tone: Encouraging and accessible
✓ Format: Step-by-step with clear headings
```

**Principles:** 16 (affirmative directives), 21 (specific), 17 (format)

**Quick Template:**
```
[Task] with these characteristics:

✓ [Positive requirement 1]
✓ [Positive requirement 2]
✓ [Positive requirement 3]
✓ [Positive requirement 4]
```

---

## Fix 9: Add Constraints and Requirements

### Pattern: Open-Ended → Bounded

**Before:**
```
Design a database schema.
```

**After:**
```
Design a PostgreSQL database schema for a task management SaaS with these constraints:

###Requirements###
- Support: 10,000+ organizations (multi-tenant)
- Entities: Organizations, Users, Projects, Tasks, Comments
- Must include: created_at, updated_at, soft deletes
- Naming: snake_case for all tables and columns

###Technical Constraints###
- PostgreSQL 15+
- Use UUID for primary keys
- Row-level security (RLS) for tenant isolation
- Indexes on foreign keys and frequently queried columns

###Performance Goals###
- Support 1M+ tasks total
- Query response < 100ms for single task
- Efficient bulk operations (1000+ tasks)

###Deliverables###
1. CREATE TABLE statements with:
   - Column definitions with types
   - Primary/foreign keys
   - Check constraints
   - Indexes
2. RLS policies for multi-tenancy
3. Sample queries demonstrating performance

###Success Criteria###
- All tables use snake_case naming
- RLS policies prevent cross-tenant access
- Foreign keys maintain referential integrity
```

**Principles:** 25 (requirements), 21 (detail), 8 (structure), 17 (deliverables)

**Quick Template:**
```
[Task] with these constraints:

###Requirements###
- [Functional requirement 1]
- [Functional requirement 2]

###Technical Constraints###
- [Technology/version]
- [Pattern/standard to use]

###Performance Goals###
- [Metric and target]

###Deliverables###
1. [Specific output 1]
2. [Specific output 2]

###Success Criteria###
- [Verification method 1]
- [Verification method 2]
```

---

## Fix 10: Combine Multiple Weak Prompts

### Pattern: Multiple Questions → Unified Request

**Before:**
```
What's the best way to handle errors in React?
Also, should I use error boundaries?
And what about async errors?
How do I log errors?
```

**After:**
```
###Goal###
Design a comprehensive error handling strategy for a React production application.

###Scope###

**1. Error Types to Handle:**
   - Render errors (component crashes)
   - Async errors (API calls, data fetching)
   - Event handler errors (button clicks, form submissions)
   - Third-party library errors

**2. Requirements:**
   - Prevent full app crashes
   - User-friendly error messages
   - Detailed error logging for debugging
   - Error recovery where possible

**3. Deliverables:**

   a) **Error Boundary Implementation**
      - Code example with TypeScript
      - Fallback UI component
      - Error reporting integration

   b) **Async Error Handling Pattern**
      - TanStack Query error handling
      - Global error interceptor
      - Retry logic example

   c) **Logging Strategy**
      - Error severity levels
      - Structured error objects
      - Integration with Sentry/monitoring

   d) **Best Practices Checklist**
      - Where to place error boundaries
      - What to log vs show users
      - Recovery strategies

###Context###
- Framework: React 18 + TypeScript
- Data fetching: TanStack Query
- Monitoring: Sentry
- Deployment: Cloudflare Pages

Provide complete, production-ready examples for each deliverable.
```

**Principles:** 3 (consolidate), 8 (structure), 21 (detail), 17 (format), 25 (requirements)

**Quick Template:**
```
###Goal###
[Overall objective that addresses all questions]

###Scope###

**1. [Category 1]:**
   - [Aspect from question 1]
   - [Aspect from question 2]

**2. [Category 2]:**
   - [Requirements]

**3. Deliverables:**
   a) [Answer to Q1 with format]
   b) [Answer to Q2 with format]
   c) [Answer to Q3 with format]

###Context###
[Environment/constraints]
```

---

## Quick Checklist: Is My Prompt Strong?

Use this before submitting any prompt:

**Content:**
- [ ] Specific topic (not "write about X")
- [ ] Target audience specified
- [ ] Desired outcome clear
- [ ] Context provided
- [ ] Constraints stated

**Structure:**
- [ ] Uses delimiters (###Headers###)
- [ ] Complex tasks broken down
- [ ] Steps numbered/ordered
- [ ] Examples included
- [ ] Output format specified

**Clarity:**
- [ ] Affirmative (Do X, not Don't X)
- [ ] Direct (includes relevant information)
- [ ] Detailed (specific requirements)
- [ ] Complete (no missing information)

**Reasoning:**
- [ ] Asks for explanations ("explain why")
- [ ] Requests step-by-step thinking
- [ ] Includes validation criteria

**Score:** [X]/16

- 14-16: Excellent prompt
- 10-13: Good prompt, minor improvements
- 6-9: Weak prompt, needs significant work
- 0-5: Ineffective prompt, restart with structure

---

**Total Fixes**: 10 patterns
**Principles Covered**: 16 of 26
**Time to Apply**: 30-60 seconds per fix
**Average Improvement**: 350% better responses
