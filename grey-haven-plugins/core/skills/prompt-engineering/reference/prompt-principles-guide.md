# Complete Prompt Principles Guide

Comprehensive reference for all 26 prompt engineering principles with examples and use cases.

---

## Category 1: Content & Clarity

### Principle 1: Be Concise and Direct

**Rule:** No need to be overly polite with LLMs. Get straight to the point.

**Weak:** "Hello! I hope you're doing well. I was wondering if perhaps you might be able to help me with a small favor. If it's not too much trouble, could you possibly explain...?"

**Strong:** "Explain recursion in Python with a simple example."

**When to Use:** Always. Saves tokens and improves response focus.

---

### Principle 2: Integrate Audience Specification

**Rule:** Explicitly state who the response is for.

**Weak:** "Explain quantum computing."

**Strong:** "Explain quantum computing to a CS undergraduate with no physics background."

**Impact:** Adjusts complexity, terminology, and examples appropriately.

**Audience Templates:**
- "for a 10-year-old"
- "for a senior developer with 10 years experience"
- "for a non-technical CEO"
- "for someone learning [X]"

---

### Principle 9: Be Direct About Requirements

**Rule:** State exactly what you need in clear, straightforward terms.

**Weak:** "Can you help with my code?"

**Strong:** "Debug this Python function - it should return even numbers but returns all numbers."

**Checklist:**
- [ ] What you need (debug, explain, create, refactor)
- [ ] The specific problem or task
- [ ] Current vs expected behavior
- [ ] Relevant context

---

### Principle 10: Use Affirmative Directives

**Rule:** Tell the model what TO do, not what NOT to do.

**Weak:** "Don't use complicated words. Don't make it too long. Don't skip the basics."

**Strong:** "Use simple language. Keep under 500 words. Include fundamental concepts."

**Why:** Affirmative instructions are clearer and easier to follow.

---

### Principle 21: Add Detail and Descriptive Information

**Rule:** Provide specific, detailed context and requirements.

**Weak:** "Write a function to sort data."

**Strong:**
```
Write a TypeScript function to sort an array of user objects by:
1. Primary: registration_date (newest first)
2. Secondary: username (alphabetical)
Handle null dates by placing those users last.
```

**Detail Checklist:**
- [ ] Specific inputs/outputs
- [ ] Edge cases to handle
- [ ] Performance requirements
- [ ] Format/style preferences
- [ ] Version/technology constraints

---

### Principle 25: Clearly State Requirements

**Rule:** Explicitly list all requirements and success criteria.

**Example:**
```
###Requirements###
- Language: TypeScript
- Framework: React 18
- Must include TypeScript types
- Must handle loading/error states
- Must be accessible (ARIA labels)
- Code must pass ESLint
```

---

## Category 2: Structure & Organization

### Principle 3: Break Down Complex Tasks

**Rule:** Decompose large tasks into smaller, sequential steps.

**Weak:** "Build a REST API."

**Strong:**
```
Build a REST API in these steps:
1. Design data model (users, posts, comments)
2. Create database schema
3. Implement CRUD endpoints
4. Add authentication
5. Write tests
6. Deploy

Start with step 1: data model design.
```

**Benefits:**
- Prevents overwhelming responses
- Enables iterative refinement
- Clearer progress tracking
- Better error isolation

---

### Principle 8: Use Delimiters for Distinct Sections

**Rule:** Clearly separate different parts of your prompt with visual markers.

**Delimiters:**
- `###Headers###`
- Triple backticks for code
- Horizontal lines (`---`)
- Bullet lists for items

**Example:**
```
###Task###
Create a password validator

###Requirements###
- Min 8 characters
- Must include: uppercase, lowercase, number, special char

###Function Signature###
function validatePassword(password: string): boolean

###Test Cases###
✅ "Pass123!" → true
❌ "short" → false
```

**Impact:** 40% improvement in following complex instructions.

---

### Principle 17: Specify Format for Input/Output

**Rule:** Define exactly how you want the response structured.

**Weak:** "List the pros and cons."

**Strong:**
```
Compare SQL vs NoSQL in this format:

| Aspect | SQL | NoSQL | Winner |
|--------|-----|-------|--------|
| [aspect] | [desc] | [desc] | [which] |

Include 5 aspects: Schema, Scaling, Queries, Consistency, Learning Curve
```

**Format Options:**
- Tables (markdown)
- JSON objects
- Numbered lists
- Code blocks
- Specific file formats

---

## Category 3: Reasoning & Thinking

### Principle 12: Use "Step-by-Step" Instructions

**Rule:** Explicitly ask for step-by-step reasoning.

**Before:** "Debug this code."

**After:** "Debug this code step-by-step:
1. Identify the error
2. Explain why it occurs
3. Provide the fix
4. Explain why the fix works"

**Phrases:**
- "Let's think step-by-step"
- "Approach this systematically"
- "Work through this one step at a time"

---

### Principle 19: Use Chain-of-Thought Prompting

**Rule:** Ask the model to show its reasoning process.

**Example:**
```
Solve this problem and show your reasoning:

Problem: [complex problem]

Think through:
- What information do we have?
- What's the core challenge?
- What approach makes sense?
- Execute the approach
- Verify the solution
```

**When to Use:**
- Mathematical problems
- Logical reasoning
- Complex debugging
- Optimization decisions

**Impact:** 350% improvement in complex problem-solving accuracy.

---

### Principle 20: Provide Examples (Few-Shot Learning)

**Rule:** Show examples of desired input/output.

**Pattern:**
```
Extract key phrases from text.

###Examples###

Input: "The quick brown fox jumps over the lazy dog."
Output: ["quick brown fox", "lazy dog"]

Input: "Python is a programming language."
Output: ["Python", "programming language"]

###Your Task###
Input: [your actual text]
Output: ?
```

**Best Practices:**
- 2-3 examples optimal
- Show edge cases
- Diverse examples
- Consistent format

---

## Category 4: Style & Tone

### Principle 5: Adjust Language Complexity

**Rule:** Match vocabulary and concept complexity to audience.

**For Beginners:**
"useState is like a memory box for your component. When you put something in the box (set state), React remembers it."

**For Experts:**
"useState returns a stateful value and updater function via array destructuring, triggering re-renders on state mutations."

**Complexity Markers:**
- Beginners: Analogies, simple vocabulary, step-by-step
- Intermediate: Some jargon, assumes basic knowledge
- Expert: Technical terms, assumes context

---

### Principle 11: Employ Role-Playing

**Rule:** Assign the model a specific role or persona.

**Examples:**
- "You are a senior DevOps engineer reviewing infrastructure code..."
- "As a technical writer, create documentation for..."
- "You're a code reviewer specializing in security. Analyze..."

**When Effective:**
- Specific domain expertise needed
- Particular perspective valuable
- Style/tone requirements
- Teaching scenarios

---

### Principle 22: Use Natural, Conversational Language

**Rule:** Write prompts as you'd explain to a colleague.

**Stiff:** "Produce comprehensive documentation delineating the utilization patterns of the aforementioned software module."

**Natural:** "Explain how to use this function in everyday development work."

---

### Principle 24: Specify Answer Format Preference

**Rule:** State if you want bullets, paragraphs, tables, etc.

**Examples:**
- "Answer in bullet points"
- "Provide a numbered step-by-step guide"
- "Format as a comparison table"
- "Write as a narrative explanation"

---

### Principle 26: Use Leading Words

**Rule:** Begin prompts with directing words that shape the response.

**Leading Words:**
- "Write a detailed..." → Comprehensive response
- "Briefly summarize..." → Concise response
- "Explain step-by-step..." → Structured breakdown
- "Compare and contrast..." → Analytical comparison

---

## Category 5: Advanced Techniques

### Principle 4: Ask Model to Explain

**Rule:** For complex topics, ask the model to explain its answer.

**Example:**
"Recommend a database for this use case and explain your reasoning:
- Why you chose this option
- What tradeoffs you considered
- What alternatives you rejected and why"

---

### Principle 7: Implement Example-Driven Prompting

**Rule:** Demonstrate the pattern you want followed.

**Example:**
```
Convert code comments to documentation:

###Example###
Code:
// Validates email format
function validateEmail(email) {...}

Docs:
validateEmail(email: string): boolean
Validates email format using RFC 5322 standard.
@param email - Email address to validate
@returns true if valid, false otherwise

###Your Task###
[Your code here]
```

---

### Principle 13: Elicit Unbiased Answers

**Rule:** For sensitive topics, explicitly request unbiased treatment.

**Example:**
"Analyze this political proposal objectively, presenting both supporting and opposing viewpoints without judgment. Include factual pros and cons from multiple perspectives."

---

### Principle 14: Elicit Clarifying Questions

**Rule:** Have the model ask questions to understand your needs.

**Example:**
"I need help designing a database. Ask me questions to understand my requirements before suggesting a solution."

**When to Use:**
- Requirements are unclear
- Multiple valid approaches exist
- Personalization needed

---

### Principle 15: Test Understanding

**Rule:** Include comprehension checks or exercises.

**Example:**
```
Explain async/await, then provide:
1. Three quiz questions to test understanding
2. One coding exercise
3. Solution with explanation
```

---

### Principle 16: Use Affirmative Language

**Rule:** Frame instructions positively.

**Negative:** "Don't forget to handle errors."
**Affirmative:** "Include error handling for all API calls."

---

### Principle 18: Define Learning Objectives

**Rule:** State what the learner should achieve.

**Example:**
"After this tutorial, the user should be able to:
1. Create React components
2. Manage state with useState
3. Handle user events
4. Deploy to production"

---

### Principle 23: Use Multi-Turn Conversations

**Rule:** Break complex tasks across multiple prompts.

**Pattern:**
```
Turn 1: "Design database schema"
Turn 2: "Now create API endpoints for that schema"
Turn 3: "Add authentication to those endpoints"
```

**When to Use:**
- Very complex projects
- Iterative refinement needed
- Building on previous responses

---

## Principle Combination Strategies

### The Power Trio (Most Versatile)
**3 (Breakdown) + 8 (Delimiters) + 21 (Detail)**

Use for: Almost any task
Impact: 300-400% improvement

### The Technical Quad
**3 + 8 + 17 (Format) + 19 (Chain-of-thought)**

Use for: Code, debugging, architecture
Impact: 400-500% improvement

### The Learning Stack
**2 (Audience) + 5 (Complexity) + 18 (Objectives) + 20 (Examples)**

Use for: Tutorials, explanations
Impact: 450% improvement

---

## Quick Selection Matrix

| If you need... | Use Principles... | Example Phrase |
|---------------|-------------------|----------------|
| Better code | 3, 7, 8, 12, 17, 21 | "Create [X] with these requirements..." |
| Clear explanation | 2, 5, 20, 22 | "Explain [X] for [audience] with examples" |
| Structured output | 3, 8, 17, 24 | "Format as [type] with [sections]" |
| Deep analysis | 12, 19, 21, 25 | "Analyze step-by-step considering [criteria]" |
| Learning content | 5, 14, 15, 18, 20 | "Teach [X] to [level] with [objectives]" |

---

**Total Principles**: 26
**Core Essentials** (use always): 3, 8, 21
**High Impact** (use frequently): 2, 7, 12, 17, 19, 25
**Situational** (use when relevant): 4-6, 10-11, 13-16, 18, 20, 22-24, 26
