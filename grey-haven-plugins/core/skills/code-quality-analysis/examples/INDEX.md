# Code Quality Analyzer Examples

Real-world code quality analysis scenarios demonstrating security review, clarity refactoring, and synthesis analysis.

## Files in This Directory

### [security-review-example.md](security-review-example.md)
Complete security review of an authentication service, finding and fixing 12 vulnerabilities including SQL injection, XSS, weak authentication, and insecure cryptography.

**Scenario**: FastAPI authentication service with multiple security issues
**Mode**: Security Review
**Result**: 12 vulnerabilities found (3 critical, 5 high, 4 medium), security score improved from 42/100 to 95/100

### [clarity-refactoring-example.md](clarity-refactoring-example.md)
Systematic code clarity improvement using 10 refactoring rules to transform complex, nested code into readable, maintainable functions.

**Scenario**: E-commerce order processing service with high complexity
**Mode**: Clarity Refactoring
**Result**: Cyclomatic complexity reduced from 47 to 8, readability score improved from 35/100 to 92/100

### [synthesis-analysis-example.md](synthesis-analysis-example.md)
Cross-file analysis identifying architectural issues, inconsistent patterns, and hidden dependencies across a multi-module codebase.

**Scenario**: User management system with 5 modules showing inconsistent patterns
**Mode**: Synthesis Analysis
**Result**: 18 cross-file issues found, 6 architectural improvements, consistency score improved from 58/100 to 89/100

### [complete-quality-audit.md](complete-quality-audit.md)
Full codebase quality audit combining all three modes to transform a legacy codebase into a maintainable, secure system.

**Scenario**: Legacy e-commerce platform (12 files, 3,500 lines)
**Comprehensive Review**: Security + Clarity + Synthesis
**Result**: 47 total issues found and fixed, overall quality score 38/100 → 91/100, prevented 2 production incidents

## Usage

Each example includes:
- **Before**: Original problematic code with clear issues
- **Analysis**: Step-by-step identification of problems with explanations
- **After**: Improved code with specific changes highlighted
- **Metrics**: Quantitative before/after comparison
- **Lessons**: Key takeaways and patterns to recognize

---

Return to [agent documentation](../code-quality-analyzer.md)
