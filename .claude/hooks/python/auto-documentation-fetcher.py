#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = ["requests", "beautifulsoup4", "lxml"]
# ///
"""
Auto-Documentation Fetcher Hook
===============================
Type: PreToolUse
Description: Detects when new libraries are being used and fetches relevant documentation

This hook monitors for import statements and library usage, then automatically
fetches and caches documentation for quick reference.
"""

import json
import sys
import re
from pathlib import Path
from typing import Dict, Optional, List
import hashlib
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# Documentation source mappings
DOC_SOURCES = {
    # Python packages
    "requests": "https://docs.python-requests.org/en/latest/",
    "fastapi": "https://fastapi.tiangolo.com/",
    "django": "https://docs.djangoproject.com/",
    "flask": "https://flask.palletsprojects.com/",
    "pandas": "https://pandas.pydata.org/docs/",
    "numpy": "https://numpy.org/doc/stable/",
    "pytest": "https://docs.pytest.org/",
    "sqlalchemy": "https://docs.sqlalchemy.org/",
    # JavaScript/TypeScript
    "react": "https://react.dev/",
    "vue": "https://vuejs.org/guide/",
    "express": "https://expressjs.com/",
    "next": "https://nextjs.org/docs",
    "svelte": "https://svelte.dev/docs",
    "remix": "https://remix.run/docs",
    # Other
    "stripe": "https://stripe.com/docs/api",
    "openai": "https://platform.openai.com/docs/",
    "aws": "https://docs.aws.amazon.com/",
    "docker": "https://docs.docker.com/",
}


def create_cache_dir() -> Path:
    """Create cache directory for documentation"""
    cache_dir = Path.home() / ".claude" / "doc_cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir


def get_cache_key(library: str) -> str:
    """Generate cache key for library documentation"""
    return hashlib.md5(library.encode()).hexdigest()


def is_cache_valid(cache_file: Path, hours: int = 24) -> bool:
    """Check if cached documentation is still valid"""
    if not cache_file.exists():
        return False

    # Check file age
    file_age = datetime.now() - datetime.fromtimestamp(cache_file.stat().st_mtime)
    return file_age < timedelta(hours=hours)


def fetch_documentation(library: str, url: str) -> Optional[str]:
    """Fetch documentation from URL"""
    try:
        response = requests.get(
            url,
            timeout=5,
            headers={"User-Agent": "Claude-Code-Documentation-Fetcher/1.0"},
        )
        response.raise_for_status()

        # Parse HTML and extract meaningful content
        soup = BeautifulSoup(response.text, "lxml")

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        # Try to find main content areas
        content_areas = soup.find_all(
            ["main", "article", "div"], class_=re.compile("content|documentation|main")
        )

        if content_areas:
            text = "\n".join(
                [
                    area.get_text(separator="\n", strip=True)
                    for area in content_areas[:2]
                ]
            )
        else:
            text = soup.get_text(separator="\n", strip=True)

        # Limit to first 5000 characters for context
        return text[:5000]

    except Exception as e:
        return f"Error fetching documentation: {str(e)}"


def detect_new_imports(tool_input: Dict) -> List[str]:
    """Detect import statements in code being written/edited"""
    libraries = []

    # Get the content being written/edited
    content = tool_input.get("content", "") or tool_input.get("new_string", "")

    if not content:
        return libraries

    # Python imports
    python_imports = re.findall(r"^\s*(?:from|import)\s+(\w+)", content, re.MULTILINE)
    libraries.extend(python_imports)

    # JavaScript/TypeScript imports
    js_imports = re.findall(r'(?:import|require)\s*\(?[\'"]([^\'"\s]+)[\'"]', content)
    libraries.extend(js_imports)

    # Package.json dependencies
    if "package.json" in tool_input.get("file_path", ""):
        deps = re.findall(r'"([^"]+)":\s*"[^"]+"', content)
        libraries.extend(deps)

    # Requirements.txt or pyproject.toml
    if "requirements.txt" in tool_input.get("file_path", ""):
        reqs = re.findall(r"^([a-zA-Z0-9\-_]+)", content, re.MULTILINE)
        libraries.extend(reqs)

    return list(set(libraries))


def get_cached_or_fetch_docs(library: str) -> Optional[str]:
    """Get documentation from cache or fetch if needed"""
    cache_dir = create_cache_dir()
    cache_key = get_cache_key(library)
    cache_file = cache_dir / f"{cache_key}.txt"

    # Check if we have valid cached documentation
    if is_cache_valid(cache_file):
        try:
            return cache_file.read_text()
        except Exception:
            pass

    # Check if we have a documentation source for this library
    doc_url = None
    for known_lib, url in DOC_SOURCES.items():
        if known_lib in library.lower() or library.lower() in known_lib:
            doc_url = url
            break

    if not doc_url:
        # Try to construct documentation URL for unknown libraries
        # This is a best-effort attempt
        doc_url = f"https://pypi.org/project/{library}/"

    # Fetch documentation
    docs = fetch_documentation(library, doc_url)

    if docs and not docs.startswith("Error"):
        # Cache the documentation
        try:
            cache_file.write_text(docs)
        except Exception:
            pass

    return docs


def main():
    try:
        # Read hook data from stdin
        data = json.load(sys.stdin)
        tool_name = data.get("tool_name", "")
        tool_input = data.get("tool_input", {})

        # Only process for Edit/Write tools
        if tool_name not in ["Edit", "Write", "MultiEdit"]:
            sys.exit(0)

        # Detect new imports
        libraries = detect_new_imports(tool_input)

        if not libraries:
            sys.exit(0)

        # Filter to only libraries we haven't seen recently
        # (This could be enhanced with a session-based cache)
        relevant_libs = [lib for lib in libraries if lib.lower() in DOC_SOURCES]

        if relevant_libs:
            # Provide feedback about detected libraries
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "documentationDetected": True,
                    "libraries": relevant_libs[:3],  # Limit to 3 libraries
                }
            }

            # Fetch documentation for the first library
            # (We don't want to slow down the tool too much)
            first_lib = relevant_libs[0]
            docs = get_cached_or_fetch_docs(first_lib)

            if docs:
                print(f"📚 Documentation tip for '{first_lib}':")
                print("-" * 40)
                print(docs[:500])  # Show first 500 chars
                print("-" * 40)
                print(
                    f"Full docs: {DOC_SOURCES.get(first_lib.lower(), 'See package repository')}"
                )

        sys.exit(0)

    except Exception as e:
        # Don't block operations on error
        print(f"Documentation fetcher error: {str(e)}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
