#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = ["coverage"]
# ///
"""
Coverage Gap Finder Hook
========================
Type: Stop
Description: Shows uncovered code paths in changed files and suggests test cases

This hook runs after editing to identify untested code paths and
generates test stubs for uncovered branches.
"""

import json
import sys
import subprocess
import re
from pathlib import Path
from typing import List, Dict, Optional
import ast


def find_coverage_files(project_dir: str) -> List[Path]:
    """Find coverage report files in the project"""
    coverage_files = []
    project_path = Path(project_dir)

    # Common coverage file patterns
    patterns = [
        ".coverage",
        "coverage.xml",
        "coverage.json",
        "htmlcov/index.html",
        "coverage/lcov.info",
        "coverage/coverage-final.json",
        "test-results/coverage.xml",
    ]

    for pattern in patterns:
        coverage_path = project_path / pattern
        if coverage_path.exists():
            coverage_files.append(coverage_path)

    # Search for coverage files recursively (limit depth)
    for coverage_file in project_path.glob("**/coverage.*"):
        if coverage_file.is_file():
            coverage_files.append(coverage_file)
            if len(coverage_files) > 5:
                break

    return coverage_files


def run_coverage_analysis(file_path: str, project_dir: str) -> Optional[Dict]:
    """Run coverage analysis for a specific file"""
    try:
        # Try to run coverage for Python files
        if file_path.endswith(".py"):
            # Check if coverage is installed
            result = subprocess.run(
                ["python", "-m", "coverage", "report", "--include", file_path],
                cwd=project_dir,
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode == 0:
                return parse_coverage_output(result.stdout)

        # Try for JavaScript/TypeScript
        elif file_path.endswith((".js", ".jsx", ".ts", ".tsx")):
            # Check for Jest coverage
            result = subprocess.run(
                ["npx", "jest", "--coverage", "--collectCoverageFrom", file_path],
                cwd=project_dir,
                capture_output=True,
                text=True,
                timeout=15,
            )

            if result.returncode == 0:
                return parse_jest_coverage(result.stdout)

    except Exception:
        pass

    return None


def parse_coverage_output(output: str) -> Dict:
    """Parse Python coverage report output"""
    coverage_data = {
        "statements": 0,
        "missing": 0,
        "coverage_percent": 0,
        "uncovered_lines": [],
    }

    # Parse coverage report format
    # Name                      Stmts   Miss  Cover   Missing
    # -------------------------------------------------------
    # module.py                    20      5    75%   12-14, 18, 22

    lines = output.split("\n")
    for line in lines:
        if "%" in line and not line.startswith("-"):
            parts = line.split()
            if len(parts) >= 4:
                try:
                    coverage_data["statements"] = int(parts[-4])
                    coverage_data["missing"] = int(parts[-3])
                    coverage_data["coverage_percent"] = float(parts[-2].rstrip("%"))

                    # Parse missing lines
                    if len(parts) > 4:
                        missing_str = " ".join(parts[4:])
                        coverage_data["uncovered_lines"] = parse_line_numbers(
                            missing_str
                        )
                except Exception:
                    pass

    return coverage_data


def parse_jest_coverage(output: str) -> Dict:
    """Parse Jest coverage output"""
    coverage_data = {
        "statements": 0,
        "branches": 0,
        "functions": 0,
        "lines": 0,
        "uncovered_lines": [],
    }

    # Parse Jest coverage table
    lines = output.split("\n")
    for line in lines:
        if "|" in line and "%" in line:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 5:
                try:
                    # Extract percentages
                    for part in parts:
                        if "%" in part:
                            value = float(part.rstrip("%"))
                            if "Stmts" in line:
                                coverage_data["statements"] = value
                            elif "Branch" in line:
                                coverage_data["branches"] = value
                            elif "Funcs" in line:
                                coverage_data["functions"] = value
                            elif "Lines" in line:
                                coverage_data["lines"] = value
                except Exception:
                    pass

    return coverage_data


def parse_line_numbers(missing_str: str) -> List[int]:
    """Parse line numbers from coverage missing string"""
    lines = []

    # Handle formats like "12-14, 18, 22"
    parts = missing_str.split(",")
    for part in parts:
        part = part.strip()
        if "-" in part:
            # Range of lines
            try:
                start, end = part.split("-")
                lines.extend(range(int(start), int(end) + 1))
            except Exception:
                pass
        else:
            # Single line
            try:
                lines.append(int(part))
            except Exception:
                pass

    return lines


def analyze_uncovered_code(file_path: str, uncovered_lines: List[int]) -> List[Dict]:
    """Analyze what code is uncovered and suggest tests"""
    suggestions = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Analyze uncovered lines
        for line_num in uncovered_lines[:10]:  # Limit to first 10
            if line_num <= len(lines):
                line = lines[line_num - 1].strip()

                # Identify what kind of code is uncovered
                suggestion = {
                    "line": line_num,
                    "code": line[:80],  # Truncate long lines
                    "type": "unknown",
                    "test_suggestion": "",
                }

                # Identify code patterns
                if "if " in line or "elif " in line:
                    suggestion["type"] = "conditional"
                    suggestion["test_suggestion"] = (
                        "Test both true and false conditions"
                    )
                elif "except" in line or "catch" in line:
                    suggestion["type"] = "error_handling"
                    suggestion["test_suggestion"] = "Test error scenarios"
                elif "return" in line:
                    suggestion["type"] = "return_statement"
                    suggestion["test_suggestion"] = "Test this return path"
                elif "for " in line or "while " in line:
                    suggestion["type"] = "loop"
                    suggestion["test_suggestion"] = (
                        "Test with empty and multiple iterations"
                    )
                elif "def " in line or "function " in line:
                    suggestion["type"] = "function"
                    suggestion["test_suggestion"] = "Add test for this function"

                suggestions.append(suggestion)

    except Exception:
        pass

    return suggestions


def generate_test_stub(
    file_path: str, uncovered_functions: List[str], language: str
) -> str:
    """Generate test stub for uncovered functions"""
    file_name = Path(file_path).stem

    if language == "python":
        stub = f"""# Test stub for {file_name}.py

import pytest
from {file_name} import *

class Test{file_name.title()}:
"""
        for func in uncovered_functions[:5]:
            stub += f"""
    def test_{func}_happy_path(self):
        \"\"\"Test {func} with valid input\"\"\"
        # TODO: Implement test
        assert True
    
    def test_{func}_edge_case(self):
        \"\"\"Test {func} with edge cases\"\"\"
        # TODO: Test with None, empty, boundary values
        assert True
    
    def test_{func}_error_case(self):
        \"\"\"Test {func} error handling\"\"\"
        # TODO: Test error scenarios
        with pytest.raises(Exception):
            pass
"""

    elif language in ["javascript", "typescript"]:
        stub = f"""// Test stub for {file_name}

describe('{file_name}', () => {{
"""
        for func in uncovered_functions[:5]:
            stub += f"""
  describe('{func}', () => {{
    it('should handle happy path', () => {{
      // TODO: Implement test
      expect(true).toBe(true);
    }});
    
    it('should handle edge cases', () => {{
      // TODO: Test with null, undefined, empty
      expect(true).toBe(true);
    }});
    
    it('should handle errors', () => {{
      // TODO: Test error scenarios
      expect(() => {{}}).toThrow();
    }});
  }});
"""
        stub += "});"

    else:
        stub = "// TODO: Add tests for uncovered code"

    return stub


def identify_untested_branches(file_path: str, language: str) -> List[str]:
    """Identify untested branches in code"""
    branches = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        if language == "python":
            # Parse Python AST
            try:
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        # Check if function has conditionals
                        has_conditionals = any(
                            isinstance(child, (ast.If, ast.While, ast.For))
                            for child in ast.walk(node)
                        )
                        if has_conditionals:
                            branches.append(f"{node.name} (has conditionals)")
            except Exception:
                pass

        elif language in ["javascript", "typescript"]:
            # Simple regex-based detection
            functions = re.findall(
                r"function\s+(\w+)|(?:const|let|var)\s+(\w+)\s*=.*?=>", content
            )
            for func_tuple in functions:
                func_name = func_tuple[0] or func_tuple[1]
                if func_name:
                    # Check if function has conditionals
                    func_pattern = f"{func_name}.*?{{.*?}}"
                    func_match = re.search(func_pattern, content, re.DOTALL)
                    if func_match and (
                        "if " in func_match.group() or "switch " in func_match.group()
                    ):
                        branches.append(f"{func_name} (has conditionals)")

    except Exception:
        pass

    return branches


def main():
    try:
        # Read hook data from stdin
        data = json.load(sys.stdin)

        # Get changed files from environment
        changed_files = data.get("changed_files", [])
        if not changed_files:
            # Try to get from CLAUDE_FILE_PATHS environment variable
            import os

            file_paths = os.environ.get("CLAUDE_FILE_PATHS", "")
            if file_paths:
                changed_files = file_paths.split()

        if not changed_files:
            sys.exit(0)

        # Get project directory
        project_dir = data.get("project_dir", ".")

        # Find existing coverage files
        coverage_files = find_coverage_files(project_dir)

        output = []
        output.append("=" * 60)
        output.append("📊 Coverage Gap Analysis")
        output.append("=" * 60)

        if coverage_files:
            output.append("\n📁 Found coverage data:")
            for cf in coverage_files[:3]:
                output.append(f"   • {cf.relative_to(Path(project_dir))}")

        # Analyze each changed file
        total_suggestions = []

        for file_path in changed_files:
            if not Path(file_path).exists():
                continue

            # Detect language
            ext = Path(file_path).suffix.lower()
            language_map = {
                ".py": "python",
                ".js": "javascript",
                ".jsx": "javascript",
                ".ts": "typescript",
                ".tsx": "typescript",
            }

            language = language_map.get(ext)
            if not language:
                continue

            output.append(f"\n📄 Analyzing: {Path(file_path).name}")

            # Try to get coverage data
            coverage_data = run_coverage_analysis(file_path, project_dir)

            if coverage_data and coverage_data.get("uncovered_lines"):
                coverage_pct = coverage_data.get("coverage_percent", 0)

                # Coverage status emoji
                if coverage_pct >= 80:
                    emoji = "🟢"
                elif coverage_pct >= 60:
                    emoji = "🟡"
                else:
                    emoji = "🔴"

                output.append(f"   {emoji} Coverage: {coverage_pct}%")

                # Analyze uncovered code
                suggestions = analyze_uncovered_code(
                    file_path, coverage_data["uncovered_lines"]
                )
                total_suggestions.extend(suggestions)

                if suggestions:
                    output.append("   ⚠️  Uncovered code found:")
                    for sugg in suggestions[:3]:
                        output.append(f"      Line {sugg['line']}: {sugg['code']}")
                        if sugg["test_suggestion"]:
                            output.append(f"        → {sugg['test_suggestion']}")

            # Identify untested branches
            branches = identify_untested_branches(file_path, language)
            if branches:
                output.append("   🌿 Functions with untested branches:")
                for branch in branches[:3]:
                    output.append(f"      • {branch}")

        # Generate test stubs
        if total_suggestions:
            output.append("\n" + "=" * 60)
            output.append("🧪 Suggested Test Cases:")
            output.append("=" * 60)

            # Group by type
            by_type = {}
            for sugg in total_suggestions:
                by_type.setdefault(sugg["type"], []).append(sugg)

            for test_type, suggestions in by_type.items():
                if test_type != "unknown":
                    output.append(f"\n{test_type.replace('_', ' ').title()}:")
                    for sugg in suggestions[:3]:
                        output.append(
                            f"   • Line {sugg['line']}: {sugg['test_suggestion']}"
                        )

        # Testing recommendations
        output.append("\n💡 Coverage Improvement Tips:")
        output.append("   • Focus on error handling paths (often missed)")
        output.append("   • Test edge cases and boundary conditions")
        output.append("   • Add tests for new functions before committing")
        output.append("   • Aim for 80% coverage minimum")
        output.append("   • Use mutation testing to verify test quality")

        output.append("\n📚 Commands to check coverage:")
        output.append("   Python: python -m pytest --cov --cov-report=html")
        output.append("   JavaScript: npm test -- --coverage")
        output.append(
            "   TypeScript: npm test -- --coverage --collectCoverageFrom='src/**/*.ts'"
        )

        output.append("=" * 60)

        # Print output
        print("\n".join(output))

        sys.exit(0)

    except Exception as e:
        # Don't block operations on error
        print(f"Coverage gap finder error: {str(e)}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
