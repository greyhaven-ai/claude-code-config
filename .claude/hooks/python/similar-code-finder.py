#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = ["ast-grep-py"]
# ///
"""
Similar Code Finder Hook
========================
Type: PostToolUse (Edit)
Description: Finds similar code patterns after edits to suggest refactoring opportunities

This hook analyzes code changes and searches for similar patterns elsewhere
in the codebase that might benefit from the same changes or refactoring.
"""

import json
import sys
import subprocess
import re
from pathlib import Path
from typing import List, Dict
import difflib


def extract_function_signature(content: str, language: str) -> List[str]:
    """Extract function signatures from code"""
    signatures = []

    if language == "python":
        # Python function definitions
        patterns = re.findall(r"def\s+(\w+)\s*\([^)]*\)", content)
        signatures.extend(patterns)
        # Python class definitions
        patterns = re.findall(r"class\s+(\w+)", content)
        signatures.extend(patterns)

    elif language in ["javascript", "typescript"]:
        # Function declarations
        patterns = re.findall(r"function\s+(\w+)\s*\([^)]*\)", content)
        signatures.extend(patterns)
        # Arrow functions
        patterns = re.findall(r"const\s+(\w+)\s*=\s*(?:\([^)]*\)|[^=])\s*=>", content)
        signatures.extend(patterns)
        # Class definitions
        patterns = re.findall(r"class\s+(\w+)", content)
        signatures.extend(patterns)

    elif language in ["java", "csharp"]:
        # Method definitions
        patterns = re.findall(
            r"(?:public|private|protected|static|final|async)\s+\w+\s+(\w+)\s*\([^)]*\)",
            content,
        )
        signatures.extend(patterns)

    return signatures


def detect_language(file_path: str) -> str:
    """Detect programming language from file extension"""
    ext_map = {
        ".py": "python",
        ".js": "javascript",
        ".jsx": "javascript",
        ".ts": "typescript",
        ".tsx": "typescript",
        ".java": "java",
        ".cs": "csharp",
        ".go": "go",
        ".rs": "rust",
        ".cpp": "cpp",
        ".c": "c",
        ".rb": "ruby",
        ".php": "php",
    }

    ext = Path(file_path).suffix.lower()
    return ext_map.get(ext, "unknown")


def extract_code_patterns(content: str, language: str) -> List[Dict]:
    """Extract notable code patterns from content"""
    patterns = []

    # Error handling patterns
    if language == "python":
        try_blocks = re.findall(r"try:.*?except.*?:", content, re.DOTALL)
        for block in try_blocks:
            patterns.append(
                {
                    "type": "error_handling",
                    "pattern": "try-except",
                    "snippet": block[:100],
                }
            )

    elif language in ["javascript", "typescript"]:
        try_blocks = re.findall(r"try\s*{.*?}\s*catch.*?{.*?}", content, re.DOTALL)
        for block in try_blocks:
            patterns.append(
                {
                    "type": "error_handling",
                    "pattern": "try-catch",
                    "snippet": block[:100],
                }
            )

    # Loop patterns
    loop_patterns = re.findall(
        r"for\s*\([^)]+\)|for\s+\w+\s+in\s+\w+|while\s*\([^)]+\)", content
    )
    for loop in loop_patterns[:3]:  # Limit to first 3
        patterns.append({"type": "loop", "pattern": loop.split()[0], "snippet": loop})

    # Conditional patterns
    if_patterns = re.findall(r"if\s*\([^)]+\)|if\s+[^:]+:", content)
    for condition in if_patterns[:3]:
        patterns.append(
            {"type": "conditional", "pattern": "if-statement", "snippet": condition}
        )

    return patterns


def find_similar_files(file_path: str, project_dir: str, language: str) -> List[str]:
    """Find files with similar purpose based on naming and location"""
    similar_files = []
    file_name = Path(file_path).stem

    # Look for files with similar names
    try:
        # Use ripgrep to find files with similar names
        result = subprocess.run(
            ["find", project_dir, "-type", "f", "-name", f"*{file_name}*"],
            capture_output=True,
            text=True,
            timeout=2,
        )

        if result.returncode == 0 and result.stdout:
            files = result.stdout.strip().split("\n")
            # Filter to same language
            ext = Path(file_path).suffix
            similar_files = [f for f in files if f.endswith(ext) and f != file_path][:5]

    except Exception:
        pass

    # Look for files in same directory
    try:
        parent_dir = Path(file_path).parent
        for f in parent_dir.glob(f"*{Path(file_path).suffix}"):
            if str(f) != file_path and str(f) not in similar_files:
                similar_files.append(str(f))

    except Exception:
        pass

    return similar_files[:5]  # Limit to 5 files


def calculate_similarity(content1: str, content2: str) -> float:
    """Calculate similarity ratio between two code snippets"""
    # Use difflib to calculate similarity
    return difflib.SequenceMatcher(None, content1, content2).ratio()


def search_for_patterns(
    patterns: List[Dict], project_dir: str, current_file: str
) -> Dict[str, List]:
    """Search for similar patterns in the codebase"""
    findings = {}

    for pattern in patterns[:3]:  # Limit to first 3 patterns to avoid slowdown
        pattern_type = pattern["type"]

        if pattern_type not in findings:
            findings[pattern_type] = []

        # Search for similar patterns using ripgrep
        search_term = pattern["snippet"][:30]  # Use first 30 chars

        try:
            # Escape special regex characters
            search_term = re.escape(search_term)

            result = subprocess.run(
                ["rg", "-l", "--max-count", "3", search_term],
                cwd=project_dir,
                capture_output=True,
                text=True,
                timeout=2,
            )

            if result.returncode == 0 and result.stdout:
                files = result.stdout.strip().split("\n")
                for file in files[:3]:
                    if file != current_file:
                        findings[pattern_type].append(
                            {"file": file, "pattern": pattern["pattern"]}
                        )

        except Exception:
            pass

    return findings


def main():
    try:
        # Read hook data from stdin
        data = json.load(sys.stdin)
        tool_name = data.get("tool_name", "")
        tool_input = data.get("tool_input", {})

        # Only process for Edit tools
        if tool_name not in ["Edit", "MultiEdit"]:
            sys.exit(0)

        file_path = tool_input.get("file_path", "")
        new_content = tool_input.get("new_string", "")
        tool_input.get("old_string", "")

        if not file_path or not new_content:
            sys.exit(0)

        # Detect language
        language = detect_language(file_path)

        if language == "unknown":
            sys.exit(0)

        # Get project directory
        project_dir = data.get("project_dir", ".")

        # Extract patterns from the new content
        patterns = extract_code_patterns(new_content, language)

        # Extract function signatures
        signatures = extract_function_signature(new_content, language)

        # Find similar files
        similar_files = find_similar_files(file_path, project_dir, language)

        # Search for similar patterns
        pattern_findings = search_for_patterns(patterns, project_dir, file_path)

        # Generate output
        output_parts = []

        if signatures:
            output_parts.append(
                f"🔍 Modified functions/classes: {', '.join(signatures[:3])}"
            )

        if similar_files:
            output_parts.append("\n📂 Similar files that might need the same changes:")
            for f in similar_files:
                # Make path relative for readability
                try:
                    rel_path = Path(f).relative_to(project_dir)
                    output_parts.append(f"  • {rel_path}")
                except Exception:
                    output_parts.append(f"  • {Path(f).name}")

        if pattern_findings:
            output_parts.append("\n🔄 Similar patterns found in codebase:")
            for pattern_type, locations in pattern_findings.items():
                if locations:
                    output_parts.append(f"  {pattern_type}:")
                    for loc in locations[:3]:
                        output_parts.append(f"    • {loc['file']}")

        # Check for potential refactoring opportunities
        if len(similar_files) > 2:
            output_parts.append("\n💡 Refactoring suggestion:")
            output_parts.append(
                "  Multiple similar files detected. Consider extracting common functionality."
            )

        if output_parts:
            print("=" * 50)
            print("🔍 Similar Code Analysis")
            print("=" * 50)
            print("\n".join(output_parts))
            print("=" * 50)

        sys.exit(0)

    except Exception as e:
        # Don't block operations on error
        print(f"Similar code finder error: {str(e)}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
