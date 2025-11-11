#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = []
# ///
"""
Dependency Impact Analyzer Hook
===============================
Type: PreToolUse (Edit)
Description: Shows what depends on code before editing to prevent breaking changes

This hook analyzes the impact of changes by finding all files and functions
that depend on the code being modified.
"""

import json
import sys
import subprocess
import re
from pathlib import Path
from typing import List, Dict, Tuple


def get_file_language(file_path: str) -> str:
    """Determine the programming language from file extension"""
    ext_map = {
        ".py": "python",
        ".js": "javascript",
        ".jsx": "javascript",
        ".ts": "typescript",
        ".tsx": "typescript",
        ".java": "java",
        ".go": "go",
        ".rs": "rust",
        ".rb": "ruby",
        ".php": "php",
        ".cs": "csharp",
        ".cpp": "cpp",
        ".cc": "cpp",
        ".hpp": "cpp",
        ".h": "cpp",
        ".c": "c",
    }

    ext = Path(file_path).suffix.lower()
    return ext_map.get(ext, "unknown")


def extract_exported_symbols(file_path: str, language: str) -> List[str]:
    """Extract exported functions, classes, and variables from a file"""
    symbols = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return symbols

    if language == "python":
        # Functions and classes
        symbols.extend(re.findall(r"^(?:def|class)\s+(\w+)", content, re.MULTILINE))
        # Global variables (UPPERCASE)
        symbols.extend(re.findall(r"^([A-Z_][A-Z0-9_]*)\s*=", content, re.MULTILINE))

    elif language in ["javascript", "typescript"]:
        # ES6 exports
        symbols.extend(
            re.findall(r"export\s+(?:const|let|var|function|class)\s+(\w+)", content)
        )
        symbols.extend(re.findall(r"export\s+{\s*([^}]+)\s*}", content))
        # CommonJS exports
        symbols.extend(re.findall(r"module\.exports\.(\w+)", content))
        symbols.extend(re.findall(r"exports\.(\w+)", content))

    elif language == "go":
        # Exported functions and types (capitalized)
        symbols.extend(
            re.findall(r"^(?:func|type|var|const)\s+([A-Z]\w*)", content, re.MULTILINE)
        )

    elif language == "java":
        # Public methods and classes
        symbols.extend(
            re.findall(r"public\s+(?:class|interface|enum)\s+(\w+)", content)
        )
        symbols.extend(
            re.findall(r"public\s+(?:static\s+)?(?:\w+\s+)?(\w+)\s*\(", content)
        )

    return list(set(symbols))


def find_imports_of_file(
    file_path: str, project_dir: str, language: str
) -> List[Tuple[str, List[str]]]:
    """Find all files that import from the given file"""
    importers = []
    file_name = Path(file_path).stem

    if language == "python":
        # Search for Python imports
        patterns = [
            f"from {file_name} import",
            f"from .{file_name} import",
            f"from ..{file_name} import",
            f"import {file_name}",
        ]

    elif language in ["javascript", "typescript"]:
        # Search for JS/TS imports
        patterns = [
            f"from ['\"].*/{{0,1}}{file_name}['\"]",
            f"require\\(['\"].*/{{0,1}}{file_name}['\"]\\)",
            f"import.*from ['\"].*/{{0,1}}{file_name}['\"]",
        ]

    elif language == "go":
        # Search for Go imports
        package_name = Path(file_path).parent.name
        patterns = [f'import.*"{package_name}"', f"import.*{package_name}"]

    else:
        patterns = [file_name]

    for pattern in patterns:
        try:
            result = subprocess.run(
                [
                    "rg",
                    "-l",
                    pattern,
                    "--type",
                    language if language != "unknown" else "all",
                ],
                cwd=project_dir,
                capture_output=True,
                text=True,
                timeout=3,
            )

            if result.returncode == 0 and result.stdout:
                files = result.stdout.strip().split("\n")
                for f in files:
                    if f and f != file_path:
                        # Find what symbols are imported
                        imported_symbols = find_imported_symbols(f, file_name, language)
                        if imported_symbols:
                            importers.append((f, imported_symbols))

        except Exception:
            pass

    return importers


def find_imported_symbols(
    importing_file: str, module_name: str, language: str
) -> List[str]:
    """Find which symbols are imported from a module in a specific file"""
    symbols = []

    try:
        with open(importing_file, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return symbols

    if language == "python":
        # from module import symbol1, symbol2
        pattern = f"from .*{module_name} import ([^\\n]+)"
        matches = re.findall(pattern, content)
        for match in matches:
            # Parse imported symbols
            imports = match.split(",")
            for imp in imports:
                imp = imp.strip()
                if " as " in imp:
                    imp = imp.split(" as ")[0].strip()
                symbols.append(imp)

    elif language in ["javascript", "typescript"]:
        # import { symbol1, symbol2 } from 'module'
        pattern = f"import\\s+{{([^}}]+)}}\\s+from\\s+['\"][^'\"]*{module_name}['\"]"
        matches = re.findall(pattern, content)
        for match in matches:
            imports = match.split(",")
            for imp in imports:
                imp = imp.strip()
                if " as " in imp:
                    imp = imp.split(" as ")[0].strip()
                symbols.append(imp)

    return symbols


def find_function_calls(
    file_path: str, function_names: List[str], project_dir: str
) -> Dict[str, List[str]]:
    """Find all files that call specific functions"""
    callers = {}

    for func_name in function_names[:5]:  # Limit to avoid slowdown
        callers[func_name] = []

        try:
            # Search for function calls
            result = subprocess.run(
                [
                    "rg",
                    "-l",
                    f"{func_name}\\s*\\(",
                    "--type-add",
                    "code:*.{py,js,ts,tsx,jsx,go,java,rs}",
                    "-t",
                    "code",
                ],
                cwd=project_dir,
                capture_output=True,
                text=True,
                timeout=2,
            )

            if result.returncode == 0 and result.stdout:
                files = result.stdout.strip().split("\n")
                for f in files:
                    if f and f != file_path:
                        callers[func_name].append(f)

        except Exception:
            pass

    return callers


def analyze_test_coverage(file_path: str, project_dir: str) -> List[str]:
    """Find test files that test the given file"""
    test_files = []
    file_name = Path(file_path).stem

    # Common test file patterns
    test_patterns = [
        f"test_{file_name}.py",
        f"{file_name}_test.py",
        f"{file_name}.test.js",
        f"{file_name}.test.ts",
        f"{file_name}_test.go",
        f"{file_name}Test.java",
        f"{file_name}.spec.js",
        f"{file_name}.spec.ts",
    ]

    for pattern in test_patterns:
        try:
            result = subprocess.run(
                ["find", project_dir, "-name", pattern],
                capture_output=True,
                text=True,
                timeout=2,
            )

            if result.returncode == 0 and result.stdout:
                files = result.stdout.strip().split("\n")
                test_files.extend([f for f in files if f])

        except Exception:
            pass

    # Also search for files that import this module in test directories
    test_dirs = ["test", "tests", "spec", "__tests__"]
    for test_dir in test_dirs:
        try:
            result = subprocess.run(
                ["rg", "-l", file_name, f"{project_dir}/{test_dir}"],
                capture_output=True,
                text=True,
                timeout=1,
            )

            if result.returncode == 0 and result.stdout:
                files = result.stdout.strip().split("\n")
                test_files.extend([f for f in files if f])

        except Exception:
            pass

    return list(set(test_files))


def calculate_impact_score(importers: int, callers: int, tests: int) -> str:
    """Calculate an impact score for the change"""
    total = importers + callers + tests

    if total == 0:
        return "🟢 Low impact - No direct dependencies found"
    elif total < 5:
        return "🟡 Medium impact - A few dependencies found"
    elif total < 15:
        return "🟠 High impact - Multiple dependencies found"
    else:
        return "🔴 Critical impact - Many dependencies found"


def main():
    try:
        # Read hook data from stdin
        data = json.load(sys.stdin)
        tool_name = data.get("tool_name", "")
        tool_input = data.get("tool_input", {})

        # Only process for Edit/Write tools
        if tool_name not in ["Edit", "Write", "MultiEdit"]:
            sys.exit(0)

        file_path = tool_input.get("file_path", "")
        if not file_path or not Path(file_path).exists():
            sys.exit(0)

        # Get project directory
        project_dir = data.get("project_dir", ".")

        # Detect language
        language = get_file_language(file_path)

        # Extract exported symbols
        exported_symbols = extract_exported_symbols(file_path, language)

        # Find files that import this file
        importers = find_imports_of_file(file_path, project_dir, language)

        # Find function callers
        callers = (
            find_function_calls(file_path, exported_symbols, project_dir)
            if exported_symbols
            else {}
        )

        # Find test files
        test_files = analyze_test_coverage(file_path, project_dir)

        # Calculate impact
        total_importers = len(importers)
        total_callers = sum(len(files) for files in callers.values())
        total_tests = len(test_files)

        impact_score = calculate_impact_score(
            total_importers, total_callers, total_tests
        )

        # Generate output
        output_parts = []

        output_parts.append("=" * 60)
        output_parts.append("⚠️  Dependency Impact Analysis")
        output_parts.append("=" * 60)
        output_parts.append(f"File: {Path(file_path).name}")
        output_parts.append(f"Language: {language}")
        output_parts.append(f"\n{impact_score}")

        if exported_symbols:
            output_parts.append(f"\n📤 Exported symbols ({len(exported_symbols)}):")
            for symbol in exported_symbols[:5]:
                output_parts.append(f"  • {symbol}")
            if len(exported_symbols) > 5:
                output_parts.append(f"  ... and {len(exported_symbols) - 5} more")

        if importers:
            output_parts.append(f"\n📥 Files importing this module ({len(importers)}):")
            for file, symbols in importers[:5]:
                rel_path = (
                    Path(file).relative_to(project_dir)
                    if project_dir != "."
                    else Path(file)
                )
                if symbols:
                    output_parts.append(
                        f"  • {rel_path} (imports: {', '.join(symbols[:3])})"
                    )
                else:
                    output_parts.append(f"  • {rel_path}")
            if len(importers) > 5:
                output_parts.append(f"  ... and {len(importers) - 5} more")

        if callers:
            output_parts.append("\n📞 Function usage:")
            for func_name, files in list(callers.items())[:3]:
                if files:
                    output_parts.append(
                        f"  {func_name}(): called in {len(files)} file(s)"
                    )

        if test_files:
            output_parts.append(f"\n🧪 Test files ({len(test_files)}):")
            for test_file in test_files[:3]:
                rel_path = (
                    Path(test_file).relative_to(project_dir)
                    if project_dir != "."
                    else Path(test_file)
                )
                output_parts.append(f"  • {rel_path}")
            if len(test_files) > 3:
                output_parts.append(f"  ... and {len(test_files) - 3} more")

        # Add warnings for high impact changes
        if total_importers + total_callers > 10:
            output_parts.append("\n⚠️  WARNING: This file has many dependencies!")
            output_parts.append("Consider:")
            output_parts.append("  • Running all tests after changes")
            output_parts.append("  • Updating dependent files if API changes")
            output_parts.append("  • Documenting breaking changes")

        output_parts.append("=" * 60)

        # Print the analysis
        print("\n".join(output_parts))

        sys.exit(0)

    except Exception as e:
        # Don't block operations on error
        print(f"Dependency analyzer error: {str(e)}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
