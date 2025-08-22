#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = []
# ///
"""
Migration Assistant Hook
========================
Type: SessionStart
Description: Detects outdated patterns in opened files and suggests modern alternatives

This hook identifies deprecated code patterns, outdated libraries, and
suggests modern best practices when starting a coding session.
"""

import json
import sys
import re
from pathlib import Path
from typing import List, Dict
from datetime import datetime

# Define deprecated patterns and their modern alternatives
DEPRECATION_PATTERNS = {
    "python": {
        "patterns": [
            {
                "old": r'print\s+["\']',
                "new": "print()",
                "description": "Python 2 print statement → Python 3 print function",
                "severity": "high",
            },
            {
                "old": r"xrange\(",
                "new": "range()",
                "description": "xrange (Python 2) → range (Python 3)",
                "severity": "high",
            },
            {
                "old": r"\.has_key\(",
                "new": "in",
                "description": "dict.has_key() → in operator",
                "severity": "medium",
            },
            {
                "old": r"os\.path\.join",
                "new": "pathlib.Path",
                "description": "os.path → pathlib for modern path handling",
                "severity": "low",
            },
            {
                "old": r"threading\.Thread",
                "new": "asyncio",
                "description": "Consider asyncio for concurrent operations",
                "severity": "info",
            },
            {
                "old": r"%\s*\(",
                "new": "f-strings",
                "description": "% formatting → f-strings (Python 3.6+)",
                "severity": "low",
            },
            {
                "old": r"\.format\(",
                "new": "f-strings",
                "description": ".format() → f-strings for better readability",
                "severity": "low",
            },
            {
                "old": r"unittest\.TestCase",
                "new": "pytest",
                "description": "Consider pytest for more powerful testing",
                "severity": "info",
            },
        ],
        "libraries": {
            "urllib2": "requests or urllib3",
            "ConfigParser": "configparser",
            "Queue": "queue",
            "mock": "unittest.mock",
            "pip": "pip>=21.0 with new resolver",
        },
    },
    "javascript": {
        "patterns": [
            {
                "old": r"var\s+\w+\s*=",
                "new": "const/let",
                "description": "var → const/let for block scoping",
                "severity": "medium",
            },
            {
                "old": r"function\s*\(",
                "new": "arrow functions",
                "description": "Consider arrow functions for cleaner syntax",
                "severity": "info",
            },
            {
                "old": r"Promise\s*\(",
                "new": "async/await",
                "description": "Promises → async/await for better readability",
                "severity": "low",
            },
            {
                "old": r"require\(",
                "new": "import",
                "description": "CommonJS → ES modules",
                "severity": "medium",
            },
            {
                "old": r"React\.Component",
                "new": "function components + hooks",
                "description": "Class components → Function components with hooks",
                "severity": "low",
            },
            {
                "old": r"componentDidMount",
                "new": "useEffect",
                "description": "Lifecycle methods → useEffect hook",
                "severity": "low",
            },
            {
                "old": r"jQuery|\$\(",
                "new": "vanilla JS or modern framework",
                "description": "jQuery → modern JavaScript",
                "severity": "medium",
            },
        ],
        "libraries": {
            "moment": "date-fns or native Temporal API",
            "lodash": "native ES6+ methods",
            "gulp": "webpack or vite",
            "bower": "npm or yarn",
            "request": "fetch or axios",
        },
    },
    "typescript": {
        "patterns": [
            {
                "old": r"<any>",
                "new": "proper typing",
                "description": "Avoid any type - use specific types",
                "severity": "medium",
            },
            {
                "old": r"interface\s+I[A-Z]",
                "new": "interface without I prefix",
                "description": "Remove Hungarian notation from interfaces",
                "severity": "info",
            },
            {
                "old": r"enum\s+",
                "new": "const assertion or union types",
                "description": "Consider const assertions over enums",
                "severity": "info",
            },
            {
                "old": r"namespace\s+",
                "new": "ES modules",
                "description": "Namespaces → ES modules",
                "severity": "medium",
            },
        ],
        "libraries": {},
    },
}


def scan_file_for_patterns(file_path: str, language: str) -> List[Dict]:
    """Scan a file for deprecated patterns"""
    findings = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            lines = content.split("\n")

        patterns = DEPRECATION_PATTERNS.get(language, {}).get("patterns", [])

        for pattern_info in patterns:
            pattern = pattern_info["old"]
            matches = []

            for i, line in enumerate(lines, 1):
                if re.search(pattern, line):
                    matches.append(i)

            if matches:
                findings.append(
                    {
                        "file": file_path,
                        "pattern": pattern_info["description"],
                        "suggestion": pattern_info["new"],
                        "severity": pattern_info["severity"],
                        "lines": matches[:5],  # Limit to first 5 occurrences
                    }
                )

        # Check for deprecated libraries
        libraries = DEPRECATION_PATTERNS.get(language, {}).get("libraries", {})
        for old_lib, new_lib in libraries.items():
            if old_lib in content:
                findings.append(
                    {
                        "file": file_path,
                        "pattern": f"Deprecated library: {old_lib}",
                        "suggestion": new_lib,
                        "severity": "medium",
                        "lines": [],
                    }
                )

    except Exception:
        pass

    return findings


def check_package_versions(project_dir: str) -> List[Dict]:
    """Check for outdated package versions"""
    findings = []

    # Check Python requirements
    requirements_files = ["requirements.txt", "setup.py", "pyproject.toml"]
    for req_file in requirements_files:
        req_path = Path(project_dir) / req_file
        if req_path.exists():
            try:
                with open(req_path, "r") as f:
                    content = f.read()

                # Check for packages without version pinning
                if req_file == "requirements.txt":
                    unpinned = re.findall(
                        r"^([a-zA-Z0-9\-_]+)\s*$", content, re.MULTILINE
                    )
                    if unpinned:
                        findings.append(
                            {
                                "file": str(req_path),
                                "pattern": f"Unpinned dependencies: {', '.join(unpinned[:3])}",
                                "suggestion": "Pin versions for reproducible builds",
                                "severity": "medium",
                                "lines": [],
                            }
                        )

            except Exception:
                pass

    # Check JavaScript package.json
    package_json = Path(project_dir) / "package.json"
    if package_json.exists():
        try:
            with open(package_json, "r") as f:
                content = f.read()

            # Check for old Node version
            if '"node":' in content:
                node_version_match = re.search(r'"node":\s*"([^"]+)"', content)
                if node_version_match:
                    version = node_version_match.group(1)
                    # Simple check - Node < 16 is outdated
                    if re.match(r"[\^~]?(\d+)", version):
                        major = int(re.match(r"[\^~]?(\d+)", version).group(1))
                        if major < 16:
                            findings.append(
                                {
                                    "file": str(package_json),
                                    "pattern": f"Outdated Node version: {version}",
                                    "suggestion": "Update to Node 18+ LTS",
                                    "severity": "high",
                                    "lines": [],
                                }
                            )

        except Exception:
            pass

    return findings


def suggest_modern_frameworks(project_dir: str) -> List[str]:
    """Suggest modern framework alternatives based on project structure"""
    suggestions = []

    # Check for React class components
    if any(Path(project_dir).rglob("*.jsx")) or any(Path(project_dir).rglob("*.tsx")):
        suggestions.append(
            "Consider migrating to React 18+ with Suspense and Server Components"
        )

    # Check for old build tools
    if (Path(project_dir) / "webpack.config.js").exists():
        webpack_config = (Path(project_dir) / "webpack.config.js").read_text()
        if "webpack 4" in webpack_config or "webpack 5" not in webpack_config:
            suggestions.append(
                "Consider migrating to Webpack 5 or Vite for faster builds"
            )

    if (Path(project_dir) / "gulpfile.js").exists():
        suggestions.append(
            "Consider replacing Gulp with modern build tools like Vite or esbuild"
        )

    # Check for Python 2 indicators
    if (Path(project_dir) / "setup.py").exists():
        try:
            setup_content = (Path(project_dir) / "setup.py").read_text()
            if "python_requires" not in setup_content:
                suggestions.append("Add python_requires='>=3.8' to setup.py")
        except Exception:
            pass

    return suggestions


def generate_migration_report(findings: List[Dict], suggestions: List[str]) -> str:
    """Generate a migration report"""
    if not findings and not suggestions:
        return ""

    output = []
    output.append("=" * 60)
    output.append("🔄 Migration Assistant Report")
    output.append("=" * 60)
    output.append(f"Scan date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    output.append("")

    # Group findings by severity
    high_severity = [f for f in findings if f["severity"] == "high"]
    medium_severity = [f for f in findings if f["severity"] == "medium"]
    low_severity = [f for f in findings if f["severity"] == "low"]
    [f for f in findings if f["severity"] == "info"]

    if high_severity:
        output.append("🔴 HIGH PRIORITY - Deprecated patterns that should be updated:")
        for finding in high_severity[:5]:
            output.append(f"   • {finding['pattern']}")
            output.append(f"     → Suggestion: {finding['suggestion']}")
            if finding["lines"]:
                output.append(
                    f"     Found on lines: {', '.join(map(str, finding['lines']))}"
                )
        output.append("")

    if medium_severity:
        output.append("🟡 MEDIUM PRIORITY - Consider updating these patterns:")
        for finding in medium_severity[:5]:
            output.append(f"   • {finding['pattern']}")
            output.append(f"     → {finding['suggestion']}")
        output.append("")

    if low_severity:
        output.append("🟢 LOW PRIORITY - Modern alternatives available:")
        for finding in low_severity[:3]:
            output.append(f"   • {finding['pattern']} → {finding['suggestion']}")
        output.append("")

    if suggestions:
        output.append("💡 Framework & Tooling Suggestions:")
        for suggestion in suggestions:
            output.append(f"   • {suggestion}")
        output.append("")

    # Add migration tips
    output.append("📚 Migration Best Practices:")
    output.append("   1. Start with high-priority deprecations")
    output.append("   2. Update one pattern type at a time")
    output.append("   3. Run tests after each change")
    output.append("   4. Use automated tools when available:")
    output.append("      • Python: 2to3, pyupgrade, black")
    output.append("      • JavaScript: jscodeshift, lebab")
    output.append("      • TypeScript: ts-migrate")

    output.append("=" * 60)

    return "\n".join(output)


def main():
    try:
        # Read hook data from stdin
        data = json.load(sys.stdin)

        # Get project directory
        project_dir = data.get("project_dir", ".") or data.get("cwd", ".")

        # Scan common source directories
        source_dirs = ["src", "lib", "app", "."]
        all_findings = []

        for source_dir in source_dirs:
            dir_path = Path(project_dir) / source_dir
            if not dir_path.exists():
                continue

            # Scan Python files
            for py_file in dir_path.rglob("*.py"):
                findings = scan_file_for_patterns(str(py_file), "python")
                all_findings.extend(findings)
                if len(all_findings) > 20:  # Limit total findings
                    break

            # Scan JavaScript/TypeScript files
            for ext in ["*.js", "*.jsx", "*.ts", "*.tsx"]:
                for js_file in dir_path.rglob(ext):
                    language = "typescript" if "ts" in ext else "javascript"
                    findings = scan_file_for_patterns(str(js_file), language)
                    all_findings.extend(findings)
                    if len(all_findings) > 20:
                        break

        # Check package versions
        version_findings = check_package_versions(project_dir)
        all_findings.extend(version_findings)

        # Get framework suggestions
        suggestions = suggest_modern_frameworks(project_dir)

        # Generate and print report
        report = generate_migration_report(all_findings[:15], suggestions)

        if report:
            print(report)

        sys.exit(0)

    except Exception as e:
        # Don't block operations on error
        print(f"Migration assistant error: {str(e)}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
