# Analysis Workflows

Step-by-step workflows for conducting security reviews, clarity refactorings, and synthesis analysis.

## Security Review Workflow

### Pre-Analysis (15 minutes)

**1. Gather Context**:
- [ ] Identify critical components (auth, payment, data handling)
- [ ] Review architecture diagram
- [ ] Identify external dependencies
- [ ] List sensitive data types (PII, credentials, payment info)

**2. Setup Tools**:
```bash
# Python
pip install bandit safety

# JavaScript
npm install -g eslint-plugin-security

# Multi-language
brew install semgrep
```

**3. Create Checklist**:
- [ ] OWASP Top 10 coverage
- [ ] Authentication/authorization
- [ ] Input validation
- [ ] Cryptography
- [ ] Data protection

### Automated Scan (30 minutes)

**Run Security Scanners**:
```bash
# Python: Bandit
bandit -r app/ -f json -o security-report.json

# Python: Safety (dependencies)
safety check --json > vulnerability-report.json

# JavaScript: npm audit
npm audit --json > npm-audit.json

# Multi-language: Semgrep
semgrep --config auto app/ --json > semgrep-report.json
```

**Analyze Results**:
```python
import json

# Parse reports
with open("security-report.json") as f:
    bandit_report = json.load(f)

# Count by severity
critical = len([r for r in bandit_report["results"] if r["issue_severity"] == "HIGH"])
high = len([r for r in bandit_report["results"] if r["issue_severity"] == "MEDIUM"])
medium = len([r for r in bandit_report["results"] if r["issue_severity"] == "LOW"])

print(f"Critical: {critical}, High: {high}, Medium: {medium}")
```

### Manual Review (2-4 hours)

**1. Authentication (30 min)**:
- [ ] Check password hashing (bcrypt/argon2, not MD5)
- [ ] Verify session management
- [ ] Check JWT implementation
- [ ] Review login rate limiting
- [ ] Check password reset flow

```python
# Look for weak hashing
git grep -n "md5\|sha1\|hashlib"

# Look for hardcoded secrets
git grep -n "password.*=.*[\"']" --and --not -e "password_hash"
git grep -n "secret.*=.*[\"']"
git grep -n "api_key.*=.*[\"']"
```

**2. Input Validation (30 min)**:
- [ ] Check SQL injection (parameterized queries?)
- [ ] Check XSS (output encoding?)
- [ ] Check command injection
- [ ] Validate file uploads

```python
# Look for SQL injection
git grep -n "execute.*f[\"']" | grep SELECT
git grep -n "execute.*\+" | grep SELECT

# Look for command injection
git grep -n "os.system\|subprocess.*shell=True"
```

**3. Data Protection (30 min)**:
- [ ] Check encryption in transit (HTTPS)
- [ ] Check encryption at rest
- [ ] Review logging (no sensitive data)
- [ ] Check database encryption
- [ ] Review backups

```python
# Look for logging sensitive data
git grep -n "log.*password\|log.*ssn\|log.*credit_card"
```

**4. Access Control (30 min)**:
- [ ] Check authorization on all endpoints
- [ ] Verify multi-tenant isolation
- [ ] Check direct object references
- [ ] Review admin functions
- [ ] Check CORS configuration

```python
# Look for missing auth
git grep -n "@app\.\(get\|post\|put\|delete\)" | \
  xargs -I {} bash -c 'echo {} && git blame -L $(echo {} | cut -d: -f2),+10 $(echo {} | cut -d: -f1) | grep -q "Depends.*auth" || echo "  ⚠️ Missing auth"'
```

**5. Dependencies (30 min)**:
- [ ] Check for known vulnerabilities
- [ ] Verify all dependencies updated
- [ ] Review license compliance

### Generate Security Scorecard (15 minutes)

```python
def calculate_security_score(findings):
    """Calculate security score from findings."""
    critical = len([f for f in findings if f["severity"] == "critical"])
    high = len([f for f in findings if f["severity"] == "high"])
    medium = len([f for f in findings if f["severity"] == "medium"])

    # Deduct points for each issue
    score = 100
    score -= critical * 20  # -20 per critical
    score -= high * 10      # -10 per high
    score -= medium * 5     # -5 per medium

    return max(0, score)

score = calculate_security_score(findings)
print(f"Security Score: {score}/100")

if score < 70:
    print("⛔️ CRITICAL: Do not deploy")
elif score < 85:
    print("⚠️ WARNING: Address issues before production")
else:
    print("✅ PASS: Production ready")
```

### Fix and Verify (Variable Time)

**Prioritize**:
1. Critical (P0): Fix immediately (SQL injection, hardcoded secrets)
2. High (P1): Fix before deployment (weak auth, missing validation)
3. Medium (P2): Fix soon (info disclosure, weak configs)

**Verify Fixes**:
```bash
# Re-run scanners after each fix
bandit -r app/ -f json -o security-report-fixed.json

# Compare before/after
python compare_reports.py security-report.json security-report-fixed.json
```

## Clarity Refactoring Workflow

### Identify Complexity Hotspots (30 minutes)

**Run Complexity Analysis**:
```bash
# Python
radon cc app/ -a -s | grep -E "C|D|F"  # Show C-grade or worse

# JavaScript
npx es6-plato -r -d reports src/

# Output
app/orders.py - process_order - Complexity: 47 (Grade F)  ← Refactor first!
app/payments.py - charge_card - Complexity: 38 (Grade F)
app/products.py - search - Complexity: 29 (Grade E)
```

**Prioritize by Impact**:
```
Function             Complexity  LOC  Calls  Priority
---------------------------------------------------
process_order()      47          187  450    P0 (high complexity, high usage)
charge_card()        38          142  380    P0
search_products()    29          98   120    P1
validate_user()      24          76   200    P1
update_profile()     22          89   45     P2 (lower usage)
```

### Apply Refactoring Rules (2-3 hours per function)

**For each complex function**:

**1. Apply Guard Clauses** (30 min):
- Extract all validation to guard clauses at top
- Convert nested ifs to early returns
- Flatten nesting from 8-16 levels to 1-2 levels

**2. Extract Functions** (45 min):
- Identify distinct responsibilities
- Extract each responsibility to focused function
- Give functions descriptive names
- Aim for < 20 lines per function

**3. Add Explaining Variables** (15 min):
- Extract complex conditions to variables
- Name variables to explain intent
- Make boolean logic self-documenting

**4. Replace Magic Numbers** (15 min):
- Find all magic numbers
- Create named constants at module top
- Replace numbers with constants

**5. Measure Improvement** (15 min):
```bash
# Re-measure complexity
radon cc app/orders.py

# Before: Complexity 47
# After:  Complexity 7 (-85%)
```

### Example Timeline

**Day 1: process_order() function**:
- 09:00-09:30: Analyze function, identify responsibilities
- 09:30-10:00: Apply guard clauses
- 10:00-11:00: Extract 8 focused functions
- 11:00-11:30: Add explaining variables
- 11:30-12:00: Replace magic numbers with constants
- 12:00-12:30: Write tests for new functions
- 12:30-13:00: Verify behavior unchanged

**Result**: Complexity 47 → 7, Maintainability 42 → 87

### Quality Gates

**Before merging refactored code**:
- [ ] Complexity reduced by > 50%
- [ ] All tests pass
- [ ] No behavior changes (confirmed by tests)
- [ ] Code review approved
- [ ] Maintainability index > 70

## Synthesis Analysis Workflow

### Map Dependencies (1 hour)

**Generate Dependency Graph**:
```bash
# Python
pydeps app/ --show-deps --cluster

# JavaScript
npx madge --image deps.png src/

# Manual analysis
python analyze_imports.py app/
```

**Identify Issues**:
```python
import ast
import os
from collections import defaultdict

def analyze_imports(directory):
    """Analyze imports across all Python files."""
    imports = defaultdict(list)

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                with open(path) as f:
                    tree = ast.parse(f.read())

                for node in ast.walk(tree):
                    if isinstance(node, ast.ImportFrom):
                        imports[path].append(node.module)

    return imports

# Detect circular dependencies
def find_cycles(imports):
    cycles = []
    for file, deps in imports.items():
        for dep in deps:
            if file in imports.get(dep, []):
                cycles.append((file, dep))
    return cycles
```

### Detect Architectural Violations (1-2 hours)

**Check Layer Violations**:
```python
def check_layer_violations():
    """Check if API layer skips service layer."""
    violations = []

    api_files = glob.glob("app/api/**/*.py", recursive=True)

    for api_file in api_files:
        with open(api_file) as f:
            content = f.read()

        # Check for direct repository imports
        if "from repositories" in content or "import repositories" in content:
            violations.append(f"{api_file}: API imports repository directly")

        # Check for direct database imports
        if "from database" in content or "import sqlalchemy" in content:
            violations.append(f"{api_file}: API imports database directly")

    return violations
```

### Find Code Duplication (1 hour)

**Run Duplication Detection**:
```bash
# Python
pylint app/ --disable=all --enable=duplicate-code --min-similarity-lines=6

# JavaScript
npx jscpd src/ --min-lines 6 --threshold 5

# Output
Duplication detected (12.4%):
- app/users.py:45-67 duplicates app/orders.py:123-145 (23 lines)
- app/validation.py:12-25 duplicates app/api/users.py:89-102 (14 lines)
```

**Centralize Duplicates**:
```python
# Before: Duplicated in 3 files
# app/users.py, app/orders.py, app/products.py
def validate_email(email):
    if not email or "@" not in email:
        raise ValueError("Invalid email")

# After: Centralized
# shared/validators.py
def validate_email(email: str) -> None:
    """Central email validation."""
    if not email or "@" not in email:
        raise ValueError("Invalid email")
```

### Enforce Consistency (1-2 hours)

**Check Naming Conventions**:
```python
def check_naming_consistency():
    """Check for mixed naming conventions."""
    issues = []

    for file in glob.glob("app/**/*.py", recursive=True):
        with open(file) as f:
            tree = ast.parse(f.read())

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Check for camelCase (should be snake_case in Python)
                if re.match(r"[a-z]+[A-Z]", node.name):
                    issues.append(f"{file}: Function '{node.name}' uses camelCase")

    return issues
```

**Check Error Handling Consistency**:
```python
def check_error_patterns():
    """Check for mixed error handling patterns."""
    patterns = {
        "HTTPException": 0,
        "custom_exceptions": 0,
        "dict_errors": 0,
    }

    for file in glob.glob("app/api/**/*.py", recursive=True):
        with open(file) as f:
            content = f.read()

        if "raise HTTPException" in content:
            patterns["HTTPException"] += 1
        if "raise.*Error" in content:
            patterns["custom_exceptions"] += 1
        if 'return {"error"' in content:
            patterns["dict_errors"] += 1

    print(f"Error patterns found: {patterns}")
    if len([p for p in patterns.values() if p > 0]) > 1:
        print("⚠️ Inconsistent error handling detected")
```

### Generate Synthesis Report (30 minutes)

```python
def generate_synthesis_report():
    """Generate comprehensive synthesis analysis report."""
    report = {
        "circular_dependencies": find_cycles(analyze_imports("app/")),
        "layer_violations": check_layer_violations(),
        "duplication_percent": check_duplication(),
        "naming_issues": check_naming_consistency(),
        "consistency_score": calculate_consistency_score(),
    }

    print("=== Synthesis Analysis Report ===")
    print(f"Circular Dependencies: {len(report['circular_dependencies'])}")
    print(f"Layer Violations: {len(report['layer_violations'])}")
    print(f"Duplication: {report['duplication_percent']}%")
    print(f"Naming Issues: {len(report['naming_issues'])}")
    print(f"Consistency Score: {report['consistency_score']}/100")

    if report['consistency_score'] < 70:
        print("⛔️ REFACTORING REQUIRED")
    else:
        print("✅ ARCHITECTURE HEALTHY")
```

## Combined Audit Workflow (3 days)

### Day 1: Security

- 09:00-09:30: Setup and planning
- 09:30-10:00: Automated scans
- 10:00-13:00: Manual security review
- 13:00-14:00: Lunch
- 14:00-17:00: Fix critical vulnerabilities
- 17:00-17:30: Generate security scorecard

### Day 2: Clarity

- 09:00-09:30: Identify complexity hotspots
- 09:30-12:00: Refactor top 3 complex functions
- 12:00-13:00: Lunch
- 13:00-16:00: Refactor next 3 complex functions
- 16:00-17:00: Run tests, measure improvements

### Day 3: Synthesis

- 09:00-10:00: Map dependencies
- 10:00-11:30: Detect architectural violations
- 11:30-12:30: Find code duplication
- 12:30-13:30: Lunch
- 13:30-15:00: Enforce consistency
- 15:00-16:30: Fix highest-priority issues
- 16:30-17:30: Generate final report

## Quick Reference

### Security Review Checklist
- [ ] Run automated scanners (30 min)
- [ ] Manual OWASP Top 10 review (2 hours)
- [ ] Generate security scorecard (15 min)
- [ ] Fix critical vulnerabilities
- [ ] Re-scan to verify fixes

### Clarity Refactoring Checklist
- [ ] Identify complexity hotspots (30 min)
- [ ] Apply guard clauses (30 min)
- [ ] Extract functions (45 min)
- [ ] Add explaining variables (15 min)
- [ ] Replace magic numbers (15 min)
- [ ] Measure improvement (15 min)

### Synthesis Analysis Checklist
- [ ] Map dependencies (1 hour)
- [ ] Detect architectural violations (1-2 hours)
- [ ] Find code duplication (1 hour)
- [ ] Enforce consistency (1-2 hours)
- [ ] Generate synthesis report (30 min)

---

Related: [Security Checklist](security-checklist.md) | [Clarity Refactoring Rules](clarity-refactoring-rules.md) | [Architecture Patterns](architecture-patterns.md) | [Return to INDEX](INDEX.md)
