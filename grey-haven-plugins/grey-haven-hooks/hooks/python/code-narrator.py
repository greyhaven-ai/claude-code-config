#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = []
# ///
"""
Code Narrator Hook
==================
Type: PostToolUse
Description: Generates plain English explanations of code changes

This hook creates human-readable narratives of technical changes,
useful for non-technical stakeholders and documentation.
"""

import json
import sys
import re
from pathlib import Path
from typing import List, Dict


def detect_change_type(old_content: str, new_content: str) -> str:
    """Detect the type of change made"""
    if not old_content and new_content:
        return "created"
    elif old_content and not new_content:
        return "deleted"
    elif len(new_content) > len(old_content) * 1.5:
        return "expanded"
    elif len(new_content) < len(old_content) * 0.7:
        return "reduced"
    else:
        return "modified"


def extract_key_changes(old_content: str, new_content: str, language: str) -> List[str]:
    """Extract the key changes between old and new content"""
    changes = []

    # Extract functions/methods
    if language in ["python", "javascript", "typescript", "java", "go"]:
        old_functions = extract_functions(old_content, language)
        new_functions = extract_functions(new_content, language)

        added_functions = new_functions - old_functions
        removed_functions = old_functions - new_functions

        for func in added_functions:
            changes.append(f"Added function '{func}'")
        for func in removed_functions:
            changes.append(f"Removed function '{func}'")

    # Extract imports/dependencies
    old_imports = extract_imports(old_content, language)
    new_imports = extract_imports(new_content, language)

    added_imports = new_imports - old_imports
    removed_imports = old_imports - new_imports

    if added_imports:
        changes.append(f"Added dependencies: {', '.join(added_imports)}")
    if removed_imports:
        changes.append(f"Removed dependencies: {', '.join(removed_imports)}")

    # Detect error handling changes
    old_error_handling = count_error_handling(old_content, language)
    new_error_handling = count_error_handling(new_content, language)

    if new_error_handling > old_error_handling:
        changes.append("Improved error handling")
    elif new_error_handling < old_error_handling:
        changes.append("Simplified error handling")

    # Detect documentation changes
    old_comments = count_comments(old_content, language)
    new_comments = count_comments(new_content, language)

    if new_comments > old_comments * 1.2:
        changes.append("Added documentation")
    elif new_comments < old_comments * 0.8:
        changes.append("Reduced documentation")

    return changes


def extract_functions(content: str, language: str) -> set:
    """Extract function names from code"""
    functions = set()

    if language == "python":
        functions.update(re.findall(r"def\s+(\w+)\s*\(", content))
        functions.update(re.findall(r"class\s+(\w+)", content))
    elif language in ["javascript", "typescript"]:
        functions.update(re.findall(r"function\s+(\w+)\s*\(", content))
        functions.update(
            re.findall(
                r"(?:const|let|var)\s+(\w+)\s*=\s*(?:\([^)]*\)|[^=])\s*=>", content
            )
        )
        functions.update(re.findall(r"class\s+(\w+)", content))
    elif language == "java":
        functions.update(
            re.findall(r"(?:public|private|protected)\s+\w+\s+(\w+)\s*\(", content)
        )
    elif language == "go":
        functions.update(
            re.findall(r"func\s+(?:\(\w+\s+\*?\w+\)\s+)?(\w+)\s*\(", content)
        )

    return functions


def extract_imports(content: str, language: str) -> set:
    """Extract imported modules/packages"""
    imports = set()

    if language == "python":
        imports.update(re.findall(r"import\s+(\w+)", content))
        imports.update(re.findall(r"from\s+(\w+)", content))
    elif language in ["javascript", "typescript"]:
        imports.update(re.findall(r'import.*from\s+[\'"]([^\'"\s]+)[\'"]', content))
        imports.update(re.findall(r'require\([\'"]([^\'"\s]+)[\'"]\)', content))
    elif language == "java":
        imports.update(re.findall(r"import\s+[\w.]+\.(\w+);", content))
    elif language == "go":
        imports.update(re.findall(r'import\s+"([^"]+)"', content))

    return imports


def count_error_handling(content: str, language: str) -> int:
    """Count error handling constructs"""
    count = 0

    if language == "python":
        count += len(re.findall(r"\btry\b", content))
        count += len(re.findall(r"\bexcept\b", content))
    elif language in ["javascript", "typescript", "java"]:
        count += len(re.findall(r"\btry\b", content))
        count += len(re.findall(r"\bcatch\b", content))
    elif language == "go":
        count += len(re.findall(r"if\s+err\s*!=\s*nil", content))

    return count


def count_comments(content: str, language: str) -> int:
    """Count comment lines"""
    count = 0

    if language in ["python"]:
        count += len(re.findall(r"^\s*#", content, re.MULTILINE))
        count += len(re.findall(r'"""', content))
    elif language in ["javascript", "typescript", "java", "go"]:
        count += len(re.findall(r"^\s*//", content, re.MULTILINE))
        count += len(re.findall(r"/\*", content))

    return count


def generate_narrative(
    file_path: str, change_type: str, key_changes: List[str], language: str
) -> str:
    """Generate a plain English narrative of the changes"""
    file_name = Path(file_path).name
    file_type = get_file_type_description(file_path, language)

    # Start with the main action
    if change_type == "created":
        narrative = f"Created a new {file_type} called '{file_name}'"
    elif change_type == "deleted":
        narrative = f"Removed the {file_type} '{file_name}'"
    elif change_type == "expanded":
        narrative = f"Significantly expanded the {file_type} '{file_name}'"
    elif change_type == "reduced":
        narrative = f"Simplified and reduced the {file_type} '{file_name}'"
    else:
        narrative = f"Updated the {file_type} '{file_name}'"

    # Add key changes if any
    if key_changes:
        if len(key_changes) == 1:
            narrative += f" to {key_changes[0].lower()}"
        elif len(key_changes) == 2:
            narrative += f" to {key_changes[0].lower()} and {key_changes[1].lower()}"
        else:
            changes_text = ", ".join(key_changes[:2]).lower()
            narrative += f" with multiple changes including {changes_text}"

    # Add purpose based on patterns
    purpose = infer_purpose(file_path, key_changes)
    if purpose:
        narrative += f". This {purpose}"

    return narrative + "."


def get_file_type_description(file_path: str, language: str) -> str:
    """Get a human-readable description of the file type"""
    file_name = Path(file_path).name.lower()

    # Check for specific file types
    if "test" in file_name or "spec" in file_name:
        return "test file"
    elif "config" in file_name or "settings" in file_name:
        return "configuration file"
    elif "util" in file_name or "helper" in file_name:
        return "utility module"
    elif "model" in file_name:
        return "data model"
    elif "controller" in file_name:
        return "controller"
    elif "service" in file_name:
        return "service module"
    elif "component" in file_name:
        return "component"
    elif "api" in file_name:
        return "API module"
    elif "schema" in file_name:
        return "schema definition"

    # Default based on language
    language_defaults = {
        "python": "Python module",
        "javascript": "JavaScript file",
        "typescript": "TypeScript module",
        "java": "Java class",
        "go": "Go package",
        "rust": "Rust module",
        "ruby": "Ruby file",
        "php": "PHP script",
    }

    return language_defaults.get(language, "source file")


def infer_purpose(file_path: str, key_changes: List[str]) -> str:
    """Infer the purpose of the changes"""
    purposes = []

    # Check for common purposes based on changes
    if any("error handling" in change.lower() for change in key_changes):
        purposes.append("improves reliability by handling edge cases better")

    if any("added function" in change.lower() for change in key_changes):
        purposes.append("adds new functionality")

    if any("removed function" in change.lower() for change in key_changes):
        purposes.append("removes deprecated or unused code")

    if any("documentation" in change.lower() for change in key_changes):
        purposes.append("improves code maintainability")

    if any("dependencies" in change.lower() for change in key_changes):
        if any("added" in change.lower() for change in key_changes):
            purposes.append("introduces new capabilities")
        else:
            purposes.append("reduces external dependencies")

    # Check file path for context
    file_name = Path(file_path).name.lower()
    if "security" in file_name or "auth" in file_name:
        purposes.append("enhances security")
    elif "performance" in file_name or "optimize" in file_name:
        purposes.append("improves performance")
    elif "fix" in file_name or "patch" in file_name:
        purposes.append("fixes a known issue")

    return purposes[0] if purposes else ""


def generate_technical_summary(
    old_content: str, new_content: str, language: str
) -> Dict:
    """Generate a technical summary with metrics"""
    old_lines = len(old_content.splitlines()) if old_content else 0
    new_lines = len(new_content.splitlines())

    summary = {
        "lines_added": max(0, new_lines - old_lines),
        "lines_removed": max(0, old_lines - new_lines),
        "total_lines": new_lines,
        "complexity_indicator": "low",
    }

    # Estimate complexity
    if new_lines > 500:
        summary["complexity_indicator"] = "high"
    elif new_lines > 200:
        summary["complexity_indicator"] = "medium"

    # Count key constructs
    summary["functions"] = len(extract_functions(new_content, language))
    summary["imports"] = len(extract_imports(new_content, language))

    return summary


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
        old_content = tool_input.get("old_string", "")
        new_content = tool_input.get("new_string", "") or tool_input.get("content", "")

        if not file_path or not new_content:
            sys.exit(0)

        # Detect language
        ext = Path(file_path).suffix.lower()
        language_map = {
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
        }

        language = language_map.get(ext, "unknown")

        # Detect change type
        change_type = detect_change_type(old_content, new_content)

        # Extract key changes
        key_changes = extract_key_changes(old_content, new_content, language)

        # Generate narrative
        narrative = generate_narrative(file_path, change_type, key_changes, language)

        # Generate technical summary
        summary = generate_technical_summary(old_content, new_content, language)

        # Format output
        output = []
        output.append("=" * 50)
        output.append("📝 Code Change Narrative")
        output.append("=" * 50)
        output.append("")
        output.append("📖 Plain English Summary:")
        output.append(f"   {narrative}")
        output.append("")

        if key_changes:
            output.append("🔍 Key Changes:")
            for change in key_changes[:5]:
                output.append(f"   • {change}")

        output.append("")
        output.append("📊 Technical Metrics:")
        output.append(
            f"   • Lines changed: +{summary['lines_added']}/-{summary['lines_removed']}"
        )
        output.append(f"   • Total lines: {summary['total_lines']}")
        output.append(f"   • Functions/Classes: {summary['functions']}")
        output.append(f"   • Dependencies: {summary['imports']}")
        output.append(f"   • Complexity: {summary['complexity_indicator']}")

        # Add stakeholder-specific summaries
        output.append("")
        output.append("👥 For Stakeholders:")

        # For project managers
        if change_type == "created":
            output.append("   PM: New functionality has been added to the system")
        elif key_changes and any("error" in c.lower() for c in key_changes):
            output.append("   PM: Stability improvements have been implemented")
        elif summary["lines_removed"] > summary["lines_added"]:
            output.append("   PM: Code has been optimized and simplified")
        else:
            output.append("   PM: Existing functionality has been enhanced")

        # For QA
        if "test" in file_path.lower():
            output.append("   QA: Test coverage has been updated")
        elif key_changes and any("error" in c.lower() for c in key_changes):
            output.append("   QA: Error scenarios may need retesting")
        elif summary["functions"] > 3:
            output.append(
                "   QA: Multiple functions added - regression testing recommended"
            )

        # For documentation team
        if summary["functions"] > 0 or change_type == "created":
            output.append("   Docs: API documentation may need updating")

        output.append("=" * 50)

        # Print the narrative
        print("\n".join(output))

        sys.exit(0)

    except Exception as e:
        # Don't block operations on error
        print(f"Code narrator error: {str(e)}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
