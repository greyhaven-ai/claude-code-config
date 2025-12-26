# Tool Audit Checklist

Use this checklist to evaluate and optimize your tool set.

## Phase 1: Inventory (Score: /20)

- [ ] **All tools listed** with name, description, parameters (4 pts)
- [ ] **Usage data collected** - which tools are called most/least (4 pts)
- [ ] **Dependencies mapped** - which tools are used together (4 pts)
- [ ] **Error rates documented** - which tools fail most often (4 pts)
- [ ] **Success metrics baseline** - current task completion rate (4 pts)

## Phase 2: Analysis (Score: /30)

### Consolidation Candidates
- [ ] **CRUD patterns identified** - create/read/update/delete groups (5 pts)
- [ ] **Query variations found** - similar search/list tools (5 pts)
- [ ] **Workflow sequences mapped** - tools always used together (5 pts)

### Problem Detection
- [ ] **Low-usage tools flagged** - <5% of total calls (5 pts)
- [ ] **High-error tools identified** - >10% error rate (5 pts)
- [ ] **Overlapping tools found** - similar functionality (5 pts)

## Phase 3: Consolidation Design (Score: /25)

- [ ] **Target tool count defined** - aim for 2-7 tools (5 pts)
- [ ] **New tool interfaces drafted** - clear parameters (5 pts)
- [ ] **Action/type patterns applied** - consolidation strategies (5 pts)
- [ ] **Backward compatibility considered** - migration path (5 pts)
- [ ] **Edge cases handled** - error scenarios documented (5 pts)

## Phase 4: Validation (Score: /15)

- [ ] **Use cases tested** - all workflows work with new tools (5 pts)
- [ ] **Parameter clarity validated** - no ambiguous selections (5 pts)
- [ ] **Performance acceptable** - no significant overhead (5 pts)

## Phase 5: Implementation (Score: /10)

- [ ] **Rollout plan created** - phased deployment (3 pts)
- [ ] **Metrics tracking enabled** - before/after comparison (4 pts)
- [ ] **Documentation updated** - tool descriptions current (3 pts)

---

## Scoring Guide

| Score | Rating | Action |
|-------|--------|--------|
| 90-100 | Excellent | Minor optimization only |
| 75-89 | Good | Target specific improvements |
| 60-74 | Needs Work | Significant consolidation needed |
| <60 | Critical | Major redesign required |

---

## Quick Audit Questions

Answer these to quickly assess tool set health:

1. **How many tools do you have?**
   - 1-3: Optimal
   - 4-7: Good
   - 8-15: Needs consolidation
   - 15+: Critical

2. **What's your tool success rate?**
   - 95%+: Excellent
   - 85-94%: Good
   - 70-84%: Needs improvement
   - <70%: Redesign needed

3. **How many tools are rarely used?** (<5% of calls)
   - 0-1: Good
   - 2-3: Consider removal
   - 4+: Definitely consolidate

4. **Do you have CRUD patterns?** (create/read/update/delete variants)
   - No: Good
   - 1 set: Consider consolidation
   - Multiple sets: High priority consolidation

5. **Are tool names consistent?**
   - All snake_case or camelCase: Good
   - Mixed casing: Fix immediately

---

## Common Issues & Fixes

| Issue | Detection | Fix |
|-------|-----------|-----|
| Too many tools | Count > 10 | Consolidate with action params |
| Low success rate | <85% | Reduce tool count, clarify descriptions |
| Feature creep | Many unused tools | Remove or consolidate low-usage |
| Naming confusion | Inconsistent patterns | Standardize to verb_noun |
| Overlapping tools | Similar functionality | Merge into single tool |
| Poor descriptions | Vague or missing | Add clear what/when/returns |

---

## Tool Reduction Targets

| Current Count | Target Count | Expected Success Improvement |
|---------------|--------------|------------------------------|
| 20+ | 5-7 | +30-50% |
| 15-19 | 4-6 | +25-35% |
| 10-14 | 3-5 | +15-25% |
| 7-9 | 2-4 | +10-15% |
| 4-6 | 2-3 | +5-10% |

---

*Use this checklist quarterly or when success rates drop below 90%*
