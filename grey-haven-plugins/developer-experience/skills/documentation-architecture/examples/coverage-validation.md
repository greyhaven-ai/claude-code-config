# Example: Documentation Coverage Validation and Gap Analysis

Complete workflow for analyzing documentation coverage, identifying gaps, and establishing quality gates in CI/CD.

## Context

**Project**: FastAPI + TanStack Start SaaS Platform
**Problem**: Documentation coverage unknown, many functions and API endpoints undocumented
**Goal**: Establish 80% documentation coverage with CI/CD enforcement

**Initial State**:
- No visibility into documentation coverage
- 147 undocumented functions and 23 undocumented API endpoints
- New code merged without documentation requirements
- Partners complained about missing API documentation

## Step 1: TypeScript Documentation Coverage Analysis

```typescript
// scripts/analyze-ts-coverage.ts
import { Project } from "ts-morph";

function analyzeTypeScriptCoverage(projectPath: string) {
  const project = new Project({ tsConfigFilePath: `${projectPath}/tsconfig.json` });
  
  const result = { total: 0, documented: 0, undocumented: [] };

  project.getSourceFiles().forEach((sourceFile) => {
    // Analyze exported functions
    sourceFile.getFunctions().filter((fn) => fn.isExported()).forEach((fn) => {
      result.total++;
      const jsDocs = fn.getJsDocs();
      
      if (jsDocs.length > 0 && jsDocs[0].getDescription().trim().length > 0) {
        result.documented++;
      } else {
        result.undocumented.push({
          name: fn.getName() || "(anonymous)",
          location: `${sourceFile.getFilePath()}:${fn.getStartLineNumber()}`,
        });
      }
    });

    // Analyze interfaces
    sourceFile.getInterfaces().forEach((iface) => {
      if (!iface.isExported()) return;
      result.total++;
      if (iface.getJsDocs().length > 0) {
        result.documented++;
      } else {
        result.undocumented.push({
          name: iface.getName(),
          location: `${sourceFile.getFilePath()}:${iface.getStartLineNumber()}`,
        });
      }
    });
  });

  const coverage = (result.documented / result.total) * 100;
  
  console.log(`TypeScript Coverage: ${coverage.toFixed(1)}%`);
  console.log(`Documented: ${result.documented} / ${result.total}`);
  
  if (result.undocumented.length > 0) {
    console.log("\nMissing documentation:");
    result.undocumented.forEach((item) => console.log(`  - ${item.name} (${item.location})`));
  }

  if (coverage < 80) {
    console.error(`❌ Coverage ${coverage.toFixed(1)}% below threshold 80%`);
    process.exit(1);
  }
  
  console.log(`✅ Coverage ${coverage.toFixed(1)}% meets threshold`);
}

analyzeTypeScriptCoverage("./app");
```

## Step 2: Python Documentation Coverage Analysis

```python
# scripts/analyze_py_coverage.py
import ast
from pathlib import Path
from typing import List, Dict

class DocstringAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.total = 0
        self.documented = 0
        self.undocumented: List[Dict] = []
        self.current_file = ""
    
    def visit_FunctionDef(self, node: ast.FunctionDef):
        if node.name.startswith("_"):  # Skip private functions
            return
        
        self.total += 1
        docstring = ast.get_docstring(node)
        
        if docstring and len(docstring.strip()) > 10:
            self.documented += 1
        else:
            self.undocumented.append({
                "name": node.name,
                "type": "function",
                "location": f"{self.current_file}:{node.lineno}"
            })
        self.generic_visit(node)
    
    def visit_ClassDef(self, node: ast.ClassDef):
        self.total += 1
        docstring = ast.get_docstring(node)
        
        if docstring and len(docstring.strip()) > 10:
            self.documented += 1
        else:
            self.undocumented.append({
                "name": node.name,
                "type": "class",
                "location": f"{self.current_file}:{node.lineno}"
            })
        self.generic_visit(node)

def analyze_python_coverage(project_path: str):
    analyzer = DocstringAnalyzer()
    
    for py_file in Path(project_path).rglob("*.py"):
        if "__pycache__" in str(py_file):
            continue
        
        analyzer.current_file = str(py_file)
        with open(py_file, "r") as f:
            try:
                tree = ast.parse(f.read())
                analyzer.visit(tree)
            except SyntaxError:
                print(f"⚠️  Syntax error in {py_file}")
    
    coverage = (analyzer.documented / analyzer.total * 100) if analyzer.total > 0 else 0
    
    print(f"Python Coverage: {coverage:.1f}%")
    print(f"Documented: {analyzer.documented} / {analyzer.total}")
    
    if analyzer.undocumented:
        print("\nMissing documentation:")
        for item in analyzer.undocumented:
            print(f"  - {item['type']} {item['name']} ({item['location']})")
    
    if coverage < 80:
        print(f"❌ Coverage {coverage:.1f}% below threshold 80%")
        exit(1)
    
    print(f"✅ Coverage {coverage:.1f}% meets threshold")

analyze_python_coverage("./app")
```

## Step 3: API Endpoint Documentation Coverage

```python
# scripts/analyze_api_coverage.py
from fastapi import FastAPI

def analyze_api_documentation(app: FastAPI):
    result = {"total_endpoints": 0, "documented": 0, "undocumented": []}
    
    openapi = app.openapi()
    
    for path, methods in openapi["paths"].items():
        for method, details in methods.items():
            result["total_endpoints"] += 1
            
            has_summary = bool(details.get("summary"))
            has_description = bool(details.get("description"))
            
            if has_summary and has_description:
                result["documented"] += 1
            else:
                missing = []
                if not has_summary: missing.append("summary")
                if not has_description: missing.append("description")
                
                result["undocumented"].append({
                    "method": method.upper(),
                    "path": path,
                    "missing": missing
                })
    
    coverage = (result["documented"] / result["total_endpoints"] * 100)
    
    print(f"API Coverage: {coverage:.1f}%")
    print(f"Documented: {result['documented']} / {result['total_endpoints']}")
    
    if result["undocumented"]:
        print("\nMissing documentation:")
        for endpoint in result["undocumented"]:
            missing = ", ".join(endpoint["missing"])
            print(f"  - {endpoint['method']} {endpoint['path']} (missing: {missing})")
    
    if coverage < 80:
        print(f"❌ Coverage {coverage:.1f}% below threshold 80%")
        exit(1)
    
    print(f"✅ Coverage {coverage:.1f}% meets threshold")

from app.main import app
analyze_api_documentation(app)
```

## Step 4: Comprehensive HTML Coverage Report

```python
# scripts/generate_coverage_report.py
from jinja2 import Template
from datetime import datetime

def generate_coverage_report(ts_coverage, py_coverage, api_coverage):
    template = Template('''
<!DOCTYPE html>
<html>
<head>
    <title>Documentation Coverage Report</title>
    <style>
        body { font-family: Arial; margin: 40px; }
        .summary { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
        .card { border: 1px solid #ddd; padding: 20px; border-radius: 8px; }
        .card.pass { border-left: 4px solid #28a745; }
        .card.fail { border-left: 4px solid #dc3545; }
        .coverage { font-size: 48px; font-weight: bold; margin: 10px 0; }
        .undocumented { margin-top: 40px; }
        .undocumented li { padding: 8px; background: #f8f9fa; margin: 4px 0; }
    </style>
</head>
<body>
    <h1>Documentation Coverage Report</h1>
    <p>Generated: {{ timestamp }}</p>
    
    <div class="summary">
        <div class="card {{ 'pass' if ts_coverage.coverage >= 80 else 'fail' }}">
            <h3>TypeScript</h3>
            <div class="coverage">{{ "%.1f"|format(ts_coverage.coverage) }}%</div>
            <p>{{ ts_coverage.documented }} / {{ ts_coverage.total }}</p>
        </div>
        <div class="card {{ 'pass' if py_coverage.coverage >= 80 else 'fail' }}">
            <h3>Python</h3>
            <div class="coverage">{{ "%.1f"|format(py_coverage.coverage) }}%</div>
            <p>{{ py_coverage.documented }} / {{ py_coverage.total }}</p>
        </div>
        <div class="card {{ 'pass' if api_coverage.coverage >= 80 else 'fail' }}">
            <h3>API</h3>
            <div class="coverage">{{ "%.1f"|format(api_coverage.coverage) }}%</div>
            <p>{{ api_coverage.documented }} / {{ api_coverage.total_endpoints }}</p>
        </div>
    </div>
    
    {% for section in [ts_coverage, py_coverage] %}
    {% if section.undocumented %}
    <div class="undocumented">
        <h2>{{ section.name }} - Missing Documentation</h2>
        <ul>
        {% for item in section.undocumented %}
            <li><strong>{{ item.name }}</strong> - {{ item.location }}</li>
        {% endfor %}
        </ul>
    </div>
    {% endif %}
    {% endfor %}
</body>
</html>
    ''')
    
    html = template.render(
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ts_coverage=ts_coverage,
        py_coverage=py_coverage,
        api_coverage=api_coverage
    )
    
    with open("docs/coverage-report.html", "w") as f:
        f.write(html)
    
    print("📊 Coverage report generated: docs/coverage-report.html")
```

## Step 5: CI/CD Integration

```yaml
# .github/workflows/documentation-coverage.yml
name: Documentation Coverage

on:
  pull_request:
  push:
    branches: [main]

jobs:
  documentation-coverage:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      
      - name: Install dependencies
        run: |
          npm install
          pip install -r requirements.txt jinja2
      
      - name: Check TypeScript coverage
        run: npx ts-node scripts/analyze-ts-coverage.ts
      
      - name: Check Python coverage
        run: python scripts/analyze_py_coverage.py
      
      - name: Check API coverage
        run: python scripts/analyze_api_coverage.py
      
      - name: Generate report
        if: always()
        run: python scripts/generate_coverage_report.py
      
      - name: Upload report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: docs/coverage-report.html
      
      - name: Comment on PR
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: '📊 Documentation coverage report generated. Check artifacts.'
            });
```

## Results

### Before

- Documentation coverage: unknown
- No visibility into gaps
- 147 undocumented functions
- 23 undocumented API endpoints
- New code merged without docs
- Partners complained about missing docs

### After

- TypeScript coverage: 42% → 87%
- Python coverage: 38% → 91%
- API endpoint coverage: 51% → 95%
- CI/CD enforcement (fails build if <80%)
- Automated HTML reports

### Improvements

- Undocumented functions: 147 → 18 (88% reduction)
- Undocumented endpoints: 23 → 1 (96% reduction)
- Time to find function docs: 15 min → instant
- Partner onboarding: 2 weeks → 3 days
- Documentation debt: eliminated weekly

### Developer Feedback

- "Coverage reports made it clear what needed docs"
- "CI/CD enforcement prevented new undocumented code"
- "HTML report showed exactly what was missing"
- "80% threshold is challenging but achievable"

## Key Lessons

1. **Automated Analysis**: Manual tracking doesn't scale
2. **CI/CD Enforcement**: Prevents documentation regression
3. **Visibility**: Reports show exactly what's missing
4. **Threshold-Based**: 80% coverage is achievable and meaningful
5. **Multi-Language**: Each language needs appropriate tooling (ts-morph, AST, OpenAPI)
6. **HTML Reports**: Visual representation drives action

## Prevention Measures

**Implemented**:
- [x] TypeScript coverage analysis (ts-morph)
- [x] Python coverage analysis (AST)
- [x] API endpoint documentation check
- [x] HTML coverage reports
- [x] CI/CD integration (fails below 80%)
- [x] PR comments with coverage status

**Ongoing**:
- [ ] Pre-commit hooks (warn if adding undocumented code)
- [ ] Dashboard showing coverage trends over time
- [ ] Team documentation KPIs (quarterly review)
- [ ] Automated "most undocumented files" weekly report

---

Related: [openapi-generation.md](openapi-generation.md) | [architecture-docs.md](architecture-docs.md) | [Return to INDEX](INDEX.md)
