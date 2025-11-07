# Prompt Engineering Reference

Complete reference materials for the 26 prompt engineering principles and advanced techniques.

## Quick Navigation

| Resource | Purpose | Best For |
|----------|---------|----------|
| [Prompt Principles Guide](prompt-principles-guide.md) | All 26 principles with examples | Complete reference |
| [Principle Combinations](principle-combinations.md) | How to combine principles effectively | Advanced users |
| [Anti-Patterns](prompt-anti-patterns.md) | Common mistakes to avoid | Troubleshooting |

## The 26 Prompt Engineering Principles

### Content & Clarity (Principles 1-2, 9-10, 21, 25)

**What to say and how clearly**

- **Principle 1**: No need to be polite - Be concise and direct
- **Principle 2**: Integrate audience specification
- **Principle 9**: Be clear about requirements (directness)
- **Principle 10**: Use affirmative directives (Do X, not Don't do X)
- **Principle 21**: Add detailed and descriptive information
- **Principle 25**: Clearly state requirements

### Structure & Organization (Principles 3, 8, 17)

**How to organize information**

- **Principle 3**: Break down complex tasks into simpler steps
- **Principle 8**: Use delimiters to clearly indicate distinct sections
- **Principle 17**: Specify desired format for structured input/output

### Reasoning & Thinking (Principles 12, 19, 20)

**How to guide model's thought process**

- **Principle 12**: Use "do step-by-step" or "think step-by-step"
- **Principle 19**: Use "chain-of-thought" prompting
- **Principle 20**: Provide examples (few-shot learning)

### Style & Tone (Principles 5, 11, 22, 24, 26)

**How to express requests**

- **Principle 5**: Adjust language complexity to audience
- **Principle 11**: Employ role-playing or persona
- **Principle 22**: Use natural, conversational language
- **Principle 24**: Specify preferred answer format (bullets, paragraphs, etc.)
- **Principle 26**: Use leading words (e.g., "Write a detailed...")

### Advanced Techniques (Principles 4, 6-7, 13-16, 18, 23)

**Specialized approaches**

- **Principle 4**: Ask model to explain itself (for complex topics)
- **Principle 6**: Use incentives or penalties (when appropriate)
- **Principle 7**: Implement example-driven prompting (few-shot)
- **Principle 13**: Elicit unbiased answers for sensitive topics
- **Principle 14**: Ask clarifying questions to understand user needs
- **Principle 15**: Test understanding with quizzes or problems
- **Principle 16**: Use affirmative language
- **Principle 18**: Clearly define learning objectives
- **Principle 23**: Use multi-turn conversations for complex tasks

## Quick Selection Guide

### By Task Type

**Technical/Code (Use Principles: 3, 7, 8, 12, 17, 19, 21)**
```
✓ Break down (3)
✓ Examples (7)
✓ Delimiters (8)
✓ Step-by-step (12)
✓ Format (17)
✓ Chain-of-thought (19)
✓ Detail (21)
```

**Creative/Writing (Use Principles: 2, 5, 11, 22, 24, 26)**
```
✓ Audience (2)
✓ Complexity (5)
✓ Role-play (11)
✓ Natural language (22)
✓ Format preference (24)
✓ Leading words (26)
```

**Learning/Education (Use Principles: 5, 14, 15, 18, 20)**
```
✓ Complexity level (5)
✓ Elicit questions (14)
✓ Test understanding (15)
✓ Learning objectives (18)
✓ Examples (20)
```

**Research/Analysis (Use Principles: 3, 8, 12, 13, 19, 21, 25)**
```
✓ Break down (3)
✓ Structure (8)
✓ Step-by-step (12)
✓ Unbiased (13)
✓ Reasoning (19)
✓ Detail (21)
✓ Requirements (25)
```

## Principle Effectiveness Matrix

| Principle | Frequency of Use | Impact Level | Complexity | Combine With |
|-----------|------------------|--------------|------------|--------------|
| 1 (Concise) | High | Medium | Low | All |
| 2 (Audience) | High | High | Low | 5, 18 |
| 3 (Breakdown) | Very High | Very High | Low | 8, 12 |
| 7 (Few-shot) | High | Very High | Medium | 17, 20 |
| 8 (Delimiters) | Very High | High | Low | 3, 17 |
| 12 (Step-by-step) | High | High | Low | 3, 19 |
| 19 (Chain-of-thought) | Medium | Very High | Medium | 12, 21 |
| 21 (Detail) | Very High | High | Low | All |

**Impact Levels:**
- **Very High**: Transforms weak prompts to strong (3, 7, 8, 19)
- **High**: Significant improvement (2, 12, 21, 25)
- **Medium**: Situational benefit (1, 5, 11, 17, 24)

## Common Combinations

**The "Technical Stack"** (for code/technical tasks):
```
3 (Breakdown) + 8 (Delimiters) + 17 (Format) + 21 (Detail)
```

**The "Learning Stack"** (for educational content):
```
2 (Audience) + 5 (Complexity) + 18 (Objectives) + 20 (Examples)
```

**The "Reasoning Stack"** (for analysis/problem-solving):
```
3 (Breakdown) + 12 (Step-by-step) + 19 (Chain-of-thought) + 21 (Detail)
```

**The "Creative Stack"** (for writing/ideation):
```
2 (Audience) + 11 (Role-play) + 22 (Natural) + 26 (Leading words)
```

## Anti-Patterns to Avoid

**Don't Do:**
- ❌ Vague requests without context
- ❌ Multiple unrelated questions in one prompt
- ❌ Negative instructions ("don't do X" instead of "do Y")
- ❌ Missing output format specification
- ❌ No audience or complexity level

**Do Instead:**
- ✅ Specific requests with full context (Principle 21)
- ✅ One focused topic per prompt (Principle 3)
- ✅ Affirmative directives (Principle 10, 16)
- ✅ Explicit format requirements (Principle 17)
- ✅ Target audience specified (Principle 2)

## Progressive Mastery Path

**Level 1: Beginner (Start Here)**
- Master: 1, 2, 3, 8, 21
- Focus: Clarity, structure, specificity
- Time: 1-2 weeks practice

**Level 2: Intermediate**
- Add: 7, 12, 17, 25
- Focus: Examples, steps, format, requirements
- Time: 2-4 weeks practice

**Level 3: Advanced**
- Add: 5, 11, 19, 20, 24
- Focus: Complexity control, reasoning, style
- Time: 4-8 weeks practice

**Level 4: Expert**
- Master all 26 principles
- Create custom combinations
- Teach others

## Resource Roadmap

1. **Start:** Read [Prompt Principles Guide](prompt-principles-guide.md)
2. **Practice:** Try [Common Fixes](../examples/common-prompt-fixes.md)
3. **Deepen:** Study [Principle Combinations](principle-combinations.md)
4. **Avoid:** Learn [Anti-Patterns](prompt-anti-patterns.md)
5. **Apply:** Use [Templates](../templates/) for common tasks

## Success Metrics

Track your improvement:
- **Week 1:** Can apply 5 basic principles
- **Month 1:** Consistently use 10-12 principles
- **Month 3:** Master all 26 principles
- **Month 6:** Create optimal combinations instinctively

**Measurement:**
- Compare before/after prompt quality scores
- Track reduction in follow-up clarifications needed
- Measure improvement in first-response quality
- Monitor task completion rates

---

**Principles Covered**: All 26
**Difficulty Levels**: Beginner → Expert
**Practice Time**: 1-6 months to mastery
