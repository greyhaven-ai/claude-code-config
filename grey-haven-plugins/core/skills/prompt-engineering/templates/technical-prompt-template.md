# Technical Task Prompt Template

Reusable template for code, debugging, architecture, and technical tasks.

**Principles Applied**: 3, 7, 8, 12, 17, 19, 21, 25

---

## Template: Code Implementation

```markdown
###Task###
Implement [functionality description] in [language/framework]

###Requirements###
**Functional:**
- [Feature requirement 1]
- [Feature requirement 2]
- [Feature requirement 3]

**Technical:**
- Language: [version]
- Framework: [if applicable]
- Must support: [constraints]
- Must handle: [edge cases]

###Function Signature### (if applicable)
[Expected signature with types]
```[language]
[signature here]
```

###Examples###
**Input:** [example input]
**Output:** [expected output]

**Input:** [edge case]
**Output:** [expected behavior]

###Test Cases###
✅ Valid cases:
- [case 1]
- [case 2]

❌ Invalid cases (should handle):
- [case 1]
- [case 2]

###Coding Standards###
- Style: [style guide to follow]
- Naming: [conventions]
- Comments: [documentation level]
- Error handling: [approach]

###Deliverables###
1. [Specific output 1]
2. [Specific output 2]
3. [Specific output 3]
```

**Use When:**
- Implementing new features
- Creating utilities or helpers
- Building components

**Example Usage:**

```markdown
###Task###
Implement email validation function in TypeScript with comprehensive error messages

###Requirements###
**Functional:**
- Validate email format (RFC 5322)
- Return detailed validation result
- Support internationalized domains

**Technical:**
- Language: TypeScript 5.3
- Framework: None (pure function)
- Must support: Unicode characters in local part
- Must handle: null, undefined, empty string

###Function Signature###
```typescript
function validateEmail(email: string | null | undefined): {
  isValid: boolean;
  errors: string[];
}
```

###Examples###
**Input:** "user@example.com"
**Output:** { isValid: true, errors: [] }

**Input:** "invalid@"
**Output:** { isValid: false, errors: ["Missing domain part"] }

###Test Cases###
✅ Valid cases:
- "simple@example.com"
- "user.name+tag@example.co.uk"
- "user@subdomain.example.com"

❌ Invalid cases (should handle):
- "" (empty string) → "Email is required"
- null → "Email cannot be null"
- "@example.com" → "Missing local part"
- "user@" → "Missing domain part"

###Coding Standards###
- Style: Prettier (100 char line length)
- Naming: camelCase
- Comments: JSDoc for function
- Error handling: Collect all errors, don't fail fast

###Deliverables###
1. TypeScript function with types
2. JSDoc comment explaining parameters
3. Unit tests (Vitest)
4. Usage example
```

---

## Template: Debugging

```markdown
###Problem###
[One-line description of the issue]

###Code###
```[language]
[Paste problematic code]
```

###Error###
[Exact error message or unexpected behavior]

###Expected Behavior###
[What should happen instead]

###Environment###
- Language: [version]
- Framework: [if applicable]
- OS: [if relevant]
- Dependencies: [relevant packages with versions]

###What I've Tried###
1. [Debugging step 1]
2. [Debugging step 2]
3. [Debugging step 3]

###Task###
1. Identify the root cause
2. Explain why the error occurs
3. Provide the corrected code
4. Explain why the fix works
5. Add a test case to prevent regression

Think through this step-by-step.
```

**Use When:**
- Fixing bugs
- Understanding errors
- Investigating unexpected behavior

---

## Template: Architecture Design

```markdown
###Context###
Design [system component] for [use case/domain]

**Scale:**
- Users: [number]
- Requests: [volume]
- Data: [size]
- Uptime: [requirement]

**Constraints:**
- Budget: [if applicable]
- Technology: [must use / can't use]
- Time: [timeline]

###Requirements###

**Functional:**
- [Feature 1]
- [Feature 2]
- [Feature 3]

**Non-Functional:**
- Performance: [metrics]
- Scalability: [targets]
- Reliability: [SLA]
- Security: [requirements]

###Tech Stack###
**Preferred:**
- [Technology 1] (reason)
- [Technology 2] (reason)

**Open to:**
- Alternatives if better fit

###Deliverables###
1. **Architecture Diagram:**
   - Component breakdown
   - Data flow
   - Integration points

2. **Technology Choices:**
   - Specific tools/frameworks
   - Rationale for each
   - Tradeoffs considered

3. **Data Model:**
   - Schema design
   - Relationships
   - Indexing strategy

4. **API Design:**
   - Endpoints
   - Request/response formats
   - Authentication approach

5. **Deployment Strategy:**
   - Infrastructure
   - CI/CD pipeline
   - Monitoring approach

###Design Principles###
- [Principle 1, e.g., "Microservices over monolith"]
- [Principle 2, e.g., "Event-driven architecture"]
- [Principle 3, e.g., "Database per service"]

Let's approach this systematically, starting with the data model, then services, then integration.
```

**Use When:**
- System design
- Technology selection
- Infrastructure planning

---

## Template: Code Review

```markdown
###Code to Review###
```[language]
[Paste code here]
```

###Review Criteria###

**Performance** (Priority: [High/Medium/Low])
- [ ] Unnecessary re-renders/re-computation
- [ ] Expensive operations in hot paths
- [ ] Memory leaks or excessive allocation
- [ ] Inefficient algorithms (O(n²) where O(n) possible)

**Security** (Priority: Critical)
- [ ] Input validation
- [ ] SQL injection / XSS vulnerabilities
- [ ] Authentication/Authorization gaps
- [ ] Secret exposure
- [ ] CSRF protection

**Maintainability** (Priority: High)
- [ ] Code complexity (cyclomatic < 10)
- [ ] Clear naming
- [ ] Proper abstraction
- [ ] DRY (Don't Repeat Yourself)
- [ ] Single Responsibility Principle

**Best Practices** (Priority: Medium)
- [ ] Framework patterns followed
- [ ] Error handling comprehensive
- [ ] Logging appropriate
- [ ] Type safety (TypeScript/type hints)

###Output Format###

For each issue:
**[SEVERITY] Category - Location**
- **Issue:** [What's wrong]
- **Impact:** [Why it matters]
- **Fix:**
  ```[language]
  // Corrected code
  ```

###Summary###
- Overall Score: [X/10]
- Critical Issues: [count]
- Recommendation: [Deploy / Fix First / Refactor]
```

**Use When:**
- Reviewing pull requests
- Code quality checks
- Security audits

---

## Template: Performance Optimization

```markdown
###Current Performance###
[Describe current state with metrics]

**Baseline Metrics:**
- Response time: [P50, P95, P99]
- Throughput: [requests/sec]
- Resource usage: [CPU/Memory/Network]

###Target Performance###
- Response time: [targets]
- Throughput: [target]
- Resource usage: [constraints]

###Code/System to Optimize###
```[language]
[Paste relevant code]
```

###Constraints###
- Cannot change: [API contract, database, etc.]
- Must maintain: [backward compatibility, etc.]
- Budget: [infrastructure costs]

###Optimization Approach###

Analyze and optimize in this order:

1. **Identify Bottlenecks:**
   - Profile the code
   - Identify hot paths
   - Measure database queries
   - Check network calls

2. **Algorithm Optimization:**
   - Improve time complexity
   - Reduce unnecessary computation
   - Cache expensive operations

3. **Database Optimization:**
   - Eliminate N+1 queries
   - Add indexes
   - Optimize query structure

4. **Infrastructure:**
   - Caching layers
   - Connection pooling
   - Async processing

###Deliverables###
1. Performance analysis with bottlenecks identified
2. Optimized code with explanations
3. Before/after benchmark results
4. Validation that functionality unchanged
```

**Use When:**
- Optimizing slow code
- Meeting performance SLAs
- Reducing resource costs

---

## Quick Selection Guide

| Task Type | Use Template | Key Sections |
|-----------|--------------|--------------|
| Build feature | Code Implementation | Requirements, Test Cases, Standards |
| Fix bug | Debugging | Error, Environment, What I've Tried |
| Design system | Architecture | Context, Scale, Deliverables |
| Review code | Code Review | Criteria, Output Format |
| Speed up | Performance | Metrics, Approach, Deliverables |

---

**Total Templates**: 5 core technical templates
**Avg Fill Time**: 2-5 minutes
**Success Rate**: 90%+ first-response quality
