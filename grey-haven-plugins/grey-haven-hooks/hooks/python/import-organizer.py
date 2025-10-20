#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = ["isort", "autoflake"]
# ///
"""
Import Organizer Hook
===========================
Type: PostToolUse
Description: Organizes and cleans imports automatically after code edits

This hook sorts imports by category (stdlib → external → internal),
removes unused imports, and maintains consistent import style.
"""

import json
import sys
import subprocess
import re
from pathlib import Path
from typing import List, Tuple


def organize_python_imports(file_path: str) -> Tuple[bool, str]:
    """Organize Python imports using isort and autoflake"""
    try:
        # First, remove unused imports with autoflake
        subprocess.run(
            ["autoflake", "--remove-all-unused-imports", "--in-place", file_path],
            capture_output=True,
            timeout=5,
        )

        # Then sort imports with isort
        result = subprocess.run(
            ["isort", file_path, "--profile", "black", "--line-length", "100"],
            capture_output=True,
            text=True,
            timeout=5,
        )

        if result.returncode == 0:
            return True, "Python imports organized successfully"
        else:
            return False, f"isort error: {result.stderr}"

    except FileNotFoundError:
        # Fallback to manual organization if tools not available
        return organize_python_imports_manual(file_path)
    except Exception as e:
        return False, str(e)


def organize_python_imports_manual(file_path: str) -> Tuple[bool, str]:
    """Manually organize Python imports without external tools"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Separate imports from rest of code
        import_lines = []
        code_lines = []
        in_imports = True

        for line in lines:
            if in_imports:
                if line.strip().startswith(("import ", "from ")):
                    import_lines.append(line)
                elif line.strip() and not line.strip().startswith("#"):
                    in_imports = False
                    code_lines.append(line)
                elif not line.strip():
                    continue  # Skip empty lines in import section
                else:
                    code_lines.append(line)
            else:
                code_lines.append(line)

        if not import_lines:
            return True, "No imports to organize"

        # Categorize imports
        stdlib_imports = []
        external_imports = []
        local_imports = []

        stdlib_modules = {
            "os",
            "sys",
            "json",
            "re",
            "time",
            "datetime",
            "pathlib",
            "typing",
            "collections",
            "itertools",
            "functools",
            "subprocess",
            "tempfile",
            "hashlib",
            "ast",
            "math",
            "random",
            "string",
            "copy",
            "pickle",
        }

        for line in import_lines:
            # Extract module name
            if line.strip().startswith("import "):
                module = line.strip().split()[1].split(".")[0]
            elif line.strip().startswith("from "):
                module = line.strip().split()[1].split(".")[0]
            else:
                continue

            # Categorize
            if module in stdlib_modules:
                stdlib_imports.append(line)
            elif module.startswith("."):
                local_imports.append(line)
            else:
                external_imports.append(line)

        # Sort each category
        stdlib_imports.sort()
        external_imports.sort()
        local_imports.sort()

        # Reconstruct file
        organized_lines = []

        # Add sorted imports
        if stdlib_imports:
            organized_lines.extend(stdlib_imports)
            organized_lines.append("\n")

        if external_imports:
            organized_lines.extend(external_imports)
            organized_lines.append("\n")

        if local_imports:
            organized_lines.extend(local_imports)
            organized_lines.append("\n")

        # Add rest of code
        organized_lines.extend(code_lines)

        # Write back
        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(organized_lines)

        return True, "Python imports organized manually"

    except Exception as e:
        return False, str(e)


def organize_javascript_imports(file_path: str) -> Tuple[bool, str]:
    """Organize JavaScript/TypeScript imports"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        lines = content.split("\n")

        # Separate imports from rest of code
        import_lines = []
        code_lines = []
        in_imports = True

        for line in lines:
            if in_imports:
                if line.strip().startswith(("import ", "const ", "let ", "var ")) and (
                    "require(" in line or "from " in line
                ):
                    import_lines.append(line)
                elif line.strip().startswith("import "):
                    import_lines.append(line)
                elif line.strip() and not line.strip().startswith("//"):
                    in_imports = False
                    code_lines.append(line)
                elif not line.strip():
                    continue
                else:
                    code_lines.append(line)
            else:
                code_lines.append(line)

        if not import_lines:
            return True, "No imports to organize"

        # Categorize imports
        node_imports = []
        external_imports = []
        local_imports = []
        type_imports = []

        for line in import_lines:
            if "type " in line or line.strip().startswith("import type"):
                type_imports.append(line)
            elif re.search(r'from [\'"]\.', line):
                local_imports.append(line)
            elif re.search(r'from [\'"](@|[a-z])', line):
                # Check if it's a node built-in
                if any(
                    module in line
                    for module in [
                        "fs",
                        "path",
                        "http",
                        "https",
                        "crypto",
                        "util",
                        "stream",
                    ]
                ):
                    node_imports.append(line)
                else:
                    external_imports.append(line)
            else:
                external_imports.append(line)

        # Sort each category
        node_imports.sort()
        external_imports.sort()
        local_imports.sort()
        type_imports.sort()

        # Reconstruct file
        organized_lines = []

        # Add sorted imports
        if node_imports:
            organized_lines.extend(node_imports)
            organized_lines.append("")

        if external_imports:
            organized_lines.extend(external_imports)
            organized_lines.append("")

        if local_imports:
            organized_lines.extend(local_imports)
            organized_lines.append("")

        if type_imports:
            organized_lines.extend(type_imports)
            organized_lines.append("")

        # Add rest of code
        organized_lines.extend(code_lines)

        # Write back
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(organized_lines))

        return True, "JavaScript imports organized"

    except Exception as e:
        return False, str(e)


def organize_go_imports(file_path: str) -> Tuple[bool, str]:
    """Organize Go imports using goimports or manual organization"""
    try:
        # Try goimports first
        result = subprocess.run(
            ["goimports", "-w", file_path], capture_output=True, text=True, timeout=5
        )

        if result.returncode == 0:
            return True, "Go imports organized with goimports"

    except FileNotFoundError:
        pass

    # Fallback to manual organization
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Find import block
        import_match = re.search(r"import\s*\((.*?)\)", content, re.DOTALL)
        if not import_match:
            # Single import
            return True, "No import block to organize"

        import_block = import_match.group(1)
        imports = [line.strip() for line in import_block.split("\n") if line.strip()]

        # Categorize imports
        stdlib_imports = []
        external_imports = []
        local_imports = []

        for imp in imports:
            imp_clean = imp.strip('"')
            if "/" not in imp_clean:
                stdlib_imports.append(imp)
            elif imp_clean.startswith("github.com/") or imp_clean.startswith(
                "golang.org/"
            ):
                external_imports.append(imp)
            else:
                local_imports.append(imp)

        # Sort and rebuild
        organized_imports = []
        if stdlib_imports:
            organized_imports.extend(sorted(stdlib_imports))
            organized_imports.append("")
        if external_imports:
            organized_imports.extend(sorted(external_imports))
            organized_imports.append("")
        if local_imports:
            organized_imports.extend(sorted(local_imports))

        # Replace import block
        new_import_block = "\n\t".join(organized_imports)
        new_content = content.replace(import_block, f"\n\t{new_import_block}\n")

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)

        return True, "Go imports organized manually"

    except Exception as e:
        return False, str(e)


def detect_unused_imports(file_path: str, language: str) -> List[str]:
    """Detect potentially unused imports"""
    unused = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        if language == "python":
            # Extract imports
            imports = re.findall(r"import\s+(\w+)", content)
            imports.extend(re.findall(r"from\s+\w+\s+import\s+(\w+)", content))

            # Check if used
            for imp in imports:
                # Simple check - not perfect but fast
                # Count occurrences excluding the import line itself
                pattern = r"\b" + imp + r"\b"
                occurrences = len(re.findall(pattern, content))
                if occurrences <= 1:  # Only in import statement
                    unused.append(imp)

        elif language in ["javascript", "typescript"]:
            # Extract imported names
            imports = re.findall(r"import\s+(?:{([^}]+)}|(\w+))", content)
            for imp_tuple in imports:
                names = imp_tuple[0] if imp_tuple[0] else imp_tuple[1]
                for name in names.split(","):
                    name = name.strip()
                    if name:
                        pattern = r"\b" + name + r"\b"
                        occurrences = len(re.findall(pattern, content))
                        if occurrences <= 1:
                            unused.append(name)

    except Exception:
        pass

    return unused


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

        # Detect language
        ext = Path(file_path).suffix.lower()

        # Determine organization strategy
        success = False
        message = ""
        language = ""

        if ext in [".py"]:
            language = "python"
            success, message = organize_python_imports(file_path)
        elif ext in [".js", ".jsx", ".ts", ".tsx"]:
            language = "javascript"
            success, message = organize_javascript_imports(file_path)
        elif ext == ".go":
            language = "go"
            success, message = organize_go_imports(file_path)
        else:
            # Unsupported language - exit silently
            sys.exit(0)

        # Detect unused imports
        unused = detect_unused_imports(file_path, language)

        # Generate output only if there were changes or issues
        if success or unused:
            output = []
            output.append("=" * 50)
            output.append("📦 Import Organization")
            output.append("=" * 50)

            if success:
                output.append(f"✅ {message}")
            else:
                output.append(f"⚠️  {message}")

            if unused:
                output.append("\n⚠️  Potentially unused imports detected:")
                for imp in unused[:5]:
                    output.append(f"   • {imp}")
                if len(unused) > 5:
                    output.append(f"   ... and {len(unused) - 5} more")
                output.append("\n💡 Consider removing unused imports for cleaner code")

            # Add organization tips
            output.append("\n📋 Import Organization Rules Applied:")

            if language == "python":
                output.append("   1. Standard library imports first")
                output.append("   2. Third-party packages second")
                output.append("   3. Local/relative imports last")
                output.append("   4. Alphabetical order within groups")
            elif language == "javascript":
                output.append("   1. Node built-in modules first")
                output.append("   2. External packages second")
                output.append("   3. Local imports last")
                output.append("   4. Type imports separated")
            elif language == "go":
                output.append("   1. Standard library first")
                output.append("   2. External packages second")
                output.append("   3. Internal packages last")

            output.append("=" * 50)

            # Print output
            print("\n".join(output))

        sys.exit(0)

    except Exception as e:
        # Don't block operations on error
        print(f"Import organizer error: {str(e)}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
