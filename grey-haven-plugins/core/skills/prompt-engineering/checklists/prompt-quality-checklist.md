# Prompt Quality Checklist

Comprehensive checklist for verifying prompt quality before submission.

---

## Pre-Submission Checklist

Use this checklist to evaluate any prompt before sending to an LLM.

### Section 1: Content Clarity (Principles 1, 2, 9, 21, 25)

**Essential Elements:**

- [ ] **Task is specific** (not "help me" or "tell me about X")
  - Clear action verb (explain, create, debug, compare, etc.)
  - Specific topic or deliverable
  - Example: ✅ "Debug this login function" vs ❌ "Help with code"

- [ ] **Audience specified** (who is this for?)
  - Experience level stated
  - Background/context provided
  - Example: ✅ "For junior developer" vs ❌ No audience mentioned

- [ ] **Requirements explicitly stated**
  - What must be included
  - What constraints apply
  - Success criteria defined
  - Example: ✅ "Must support TypeScript, < 100 lines" vs ❌ Vague requirements

- [ ] **Relevant context provided**
  - Technology versions
  - Environment details
  - Constraints or limitations
  - Why you need this
  - Example: ✅ "React 18 + TypeScript for production SaaS" vs ❌ "React app"

- [ ] **Detail level appropriate**
  - Specific enough to avoid ambiguity
  - Not so detailed it's overwhelming
  - Includes examples where helpful
  - Example: ✅ "Validate emails per RFC 5322" vs ❌ "Validate emails"

**Score:** ___/5

---

### Section 2: Structure & Organization (Principles 3, 8, 17)

**Structural Elements:**

- [ ] **Complex tasks broken down**
  - Multi-step tasks split into phases
  - Clear sequence defined
  - One focus per step
  - Example: ✅ "Step 1: Design schema, Step 2: Create API" vs ❌ "Build everything"

- [ ] **Delimiters used for sections**
  - `###Headers###` for major sections
  - Code blocks properly fenced
  - Lists for related items
  - Clear visual separation
  - Example: ✅ Uses ###Task###, ###Requirements### vs ❌ Wall of text

- [ ] **Output format specified**
  - Exact structure desired (table, list, code, etc.)
  - Format template provided if applicable
  - Length/detail level indicated
  - Example: ✅ "Return as JSON with fields: name, age" vs ❌ "Give me the data"

**Score:** ___/3

---

### Section 3: Reasoning & Examples (Principles 12, 19, 20)

**Thinking Guidance:**

- [ ] **Step-by-step requested** (if applicable)
  - Uses "step-by-step" or "think through"
  - Numbered sequence for complex tasks
  - Reasoning process requested
  - Example: ✅ "Debug step-by-step: 1) Identify bug..." vs ❌ "Fix this"

- [ ] **Chain-of-thought prompted** (for complex problems)
  - Asks for reasoning
  - Requests explanation of approach
  - "Walk through your thinking"
  - Example: ✅ "Explain your reasoning at each step" vs ❌ Direct answer only

- [ ] **Examples provided** (when pattern matters)
  - 2-3 examples of desired format
  - Shows edge cases
  - Demonstrates expected style
  - Example: ✅ Shows input/output examples vs ❌ No examples

**Score:** ___/3

---

### Section 4: Style & Tone (Principles 5, 10, 11, 22, 24, 26)

**Expression Quality:**

- [ ] **Language complexity appropriate**
  - Matches audience level
  - Technical terms explained if needed
  - Simple when possible
  - Example: ✅ Adjusts vocabulary to audience vs ❌ Assumes expertise

- [ ] **Affirmative directives used**
  - Says what TO do, not what NOT to do
  - Positive framing
  - Clear direction
  - Example: ✅ "Use simple language" vs ❌ "Don't use complex words"

- [ ] **Role assignment** (if beneficial)
  - Specific expertise requested
  - Perspective defined
  - Helpful for domain tasks
  - Example: ✅ "As a security expert, review..." vs ❌ Generic request

- [ ] **Natural language**
  - Conversational tone
  - Not overly formal or robotic
  - Human-like phrasing
  - Example: ✅ "Explain how this works" vs ❌ "Elucidate the operational mechanics"

- [ ] **Format preference stated**
  - Bullets, paragraphs, tables, etc.
  - Desired length indicated
  - Style guidance provided
  - Example: ✅ "Answer in bullet points, < 200 words" vs ❌ No format specified

- [ ] **Leading words used**
  - Directs response style
  - Sets expectations
  - Guides detail level
  - Example: ✅ "Write a detailed analysis..." vs ❌ "Analysis"

**Score:** ___/6

---

### Section 5: Advanced Techniques (Principles 4, 6, 7, 13-15, 18, 23)

**Specialized Approaches:**

- [ ] **Explanation requested** (complex topics)
  - Asks "why" or "explain reasoning"
  - Seeks understanding, not just answer
  - Example: ✅ "Explain your technology choice" vs ❌ Just picks technology

- [ ] **Unbiased approach** (sensitive topics)
  - Explicitly requests objectivity
  - Asks for multiple perspectives
  - Example: ✅ "Present both sides objectively" vs ❌ Potentially biased framing

- [ ] **Clarifying questions** (unclear requirements)
  - Allows model to ask questions
  - Admits uncertainty
  - Example: ✅ "Ask me questions to clarify" vs ❌ Forces model to guess

- [ ] **Comprehension testing** (learning)
  - Includes quiz or practice
  - Tests understanding
  - Example: ✅ "Include 3 quiz questions" vs ❌ Explanation only

- [ ] **Learning objectives** (educational content)
  - Specific skills to gain
  - Measurable outcomes
  - Example: ✅ "Learner should be able to..." vs ❌ No objectives

- [ ] **Multi-turn awareness** (complex projects)
  - Acknowledges iterative process
  - Plans for refinement
  - Example: ✅ "Start with X, we'll refine later" vs ❌ Expects perfection first try

**Score:** ___/6

---

## Scoring Guide

**Total Score:** ___/23

### Quality Levels:

**20-23: Excellent Prompt** ✅
- Highly likely to get quality response on first try
- All essential elements present
- Well-structured and clear
- **Action:** Submit confidently

**15-19: Good Prompt** ✅
- Likely to get useful response
- Minor improvements possible
- Core elements covered
- **Action:** Submit, but note areas for future improvement

**10-14: Weak Prompt** ⚠️
- May get partial or unclear response
- Missing important elements
- Needs significant improvement
- **Action:** Revise before submitting

**0-9: Ineffective Prompt** ❌
- Unlikely to get useful response
- Critical elements missing
- Will require multiple clarifications
- **Action:** Restart with template from examples/

---

## Quick Improvement Checklist

If your score is < 15, apply these quick fixes:

### Priority 1 (Essential - Fix These First)

- [ ] Add specific task description (Principle 9)
- [ ] Include relevant context (Principle 21)
- [ ] State requirements clearly (Principle 25)

### Priority 2 (Important - Significant Impact)

- [ ] Use delimiters to structure (Principle 8)
- [ ] Break down complex tasks (Principle 3)
- [ ] Specify output format (Principle 17)

### Priority 3 (Helpful - Polish)

- [ ] Add examples if pattern matters (Principle 7, 20)
- [ ] Specify audience (Principle 2)
- [ ] Request step-by-step for complex tasks (Principle 12)

---

## Category-Specific Checklists

### For Technical Prompts (Code/Debug/Architecture)

**Must Have:**
- [ ] Language/framework with version
- [ ] Specific functionality or problem
- [ ] Expected behavior clearly defined
- [ ] Code examples or error messages
- [ ] Test cases or success criteria

**Should Have:**
- [ ] Environment details (OS, dependencies)
- [ ] Coding standards to follow
- [ ] Performance requirements
- [ ] Example input/output

**Impact:** 85% → 95% first-response quality

---

### For Learning Prompts (Tutorials/Explanations)

**Must Have:**
- [ ] Target audience with experience level
- [ ] Learning objectives defined
- [ ] Concept to explain specified
- [ ] Desired explanation structure

**Should Have:**
- [ ] Examples requested
- [ ] Comprehension check included
- [ ] Progressive complexity (basic → advanced)
- [ ] Practice exercise

**Impact:** 70% → 90% learner success

---

### For Creative Prompts (Writing/Ideation)

**Must Have:**
- [ ] Target audience specified
- [ ] Tone/style guidelines
- [ ] Length requirements
- [ ] Purpose or use case

**Should Have:**
- [ ] Format preference (blog, email, etc.)
- [ ] Key points to cover
- [ ] Brand voice or examples
- [ ] Constraints or avoid-list

**Impact:** 60% → 85% satisfaction with output

---

### For Research Prompts (Analysis/Comparison)

**Must Have:**
- [ ] Research question specific
- [ ] Scope defined (what to include/exclude)
- [ ] Objectivity requested
- [ ] Output format (report, table, bullets)

**Should Have:**
- [ ] Evaluation criteria
- [ ] Use case context
- [ ] Sources or data to consider
- [ ] Decision framework

**Impact:** 65% → 90% actionable insights

---

## Common Issues Checklist

**If you're not getting good responses, check:**

**Issue: Responses are too general**
- [ ] Add more specific details (Principle 21)
- [ ] Provide context and use case (Principle 2)
- [ ] Include examples of what you want (Principle 7, 20)

**Issue: Wrong format or structure**
- [ ] Explicitly specify desired format (Principle 17)
- [ ] Show an example of format (Principle 7)
- [ ] Use delimiters to organize request (Principle 8)

**Issue: Missing important aspects**
- [ ] Break down into steps (Principle 3)
- [ ] List all requirements explicitly (Principle 25)
- [ ] Provide comprehensive context (Principle 21)

**Issue: Too basic or too complex**
- [ ] Specify audience level (Principle 2)
- [ ] Adjust language complexity (Principle 5)
- [ ] Provide background on current knowledge

**Issue: Need multiple clarifying exchanges**
- [ ] Be more direct about needs (Principle 9)
- [ ] Provide all relevant details upfront (Principle 21)
- [ ] Use structured format with sections (Principle 8)

---

## Final Validation

**Before hitting send, ask yourself:**

1. **Can someone else understand what I need?**
   - If you showed this prompt to a colleague, would they know what you want?
   - If NO → Add more context and specifics

2. **Is this the minimum information needed?**
   - Is every detail relevant?
   - Is anything missing that would change the answer?
   - If NO → Trim irrelevant info, add missing pieces

3. **Is the desired output clear?**
   - Would you recognize a good response if you saw it?
   - Do you know what "done" looks like?
   - If NO → Specify success criteria and format

4. **Is this appropriately scoped?**
   - Can this be answered in one response?
   - Or should it be broken into multiple steps?
   - If too large → Use Principle 3 to break down

5. **Have I made assumptions?**
   - Am I assuming the model knows my context?
   - Am I assuming technical knowledge level?
   - If YES → Make assumptions explicit

---

**Total Validation Checks:** ___/5

If all 5 are "YES" → **Ready to submit!** ✅

If any are "NO" → **Revise using the relevant section above**

---

**Quick Reference:**
- **Excellent prompt** (20+ score): Clear task, structured, specific, examples provided
- **Most common fixes**: Add delimiters (8), break down tasks (3), add details (21)
- **Biggest impact principles**: 3, 7, 8, 17, 19, 21, 25

**Template Library:** See [../templates/](../templates/) for ready-to-use formats
