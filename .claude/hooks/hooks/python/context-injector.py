#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = []
# ///
"""
Context Injector Hook
===========================
Type: UserPromptSubmit
Description: Analyzes user prompts and automatically loads relevant code context

This hook intercepts user prompts, analyzes them for keywords and intent,
then searches the codebase for relevant files and recent changes to inject
as additional context for Claude.
"""

import json
import sys
import subprocess
import re
from typing import List, Dict


def extract_keywords(prompt: str) -> List[str]:
    """Extract meaningful keywords from user prompt"""
    # Remove common words and extract technical terms
    stop_words = {
        "the",
        "a",
        "an",
        "and",
        "or",
        "but",
        "in",
        "on",
        "at",
        "to",
        "for",
        "of",
        "with",
        "by",
        "from",
        "up",
        "about",
        "into",
        "through",
        "during",
        "how",
        "when",
        "where",
        "what",
        "which",
        "who",
        "why",
        "can",
        "could",
        "should",
        "would",
        "may",
        "might",
        "must",
        "shall",
        "will",
        "fix",
        "update",
        "change",
        "modify",
        "add",
        "remove",
        "delete",
        "create",
        "make",
        "need",
        "want",
        "please",
        "help",
        "me",
        "i",
        "my",
        "this",
        "that",
        "these",
        "those",
    }

    # Extract potential file names, function names, and technical terms
    words = re.findall(r"\b[a-zA-Z_][a-zA-Z0-9_]*\b", prompt.lower())
    keywords = [w for w in words if w not in stop_words and len(w) > 2]

    # Look for file extensions mentioned
    extensions = re.findall(r"\.\w+", prompt)
    keywords.extend(extensions)

    # Look for quoted strings (often file names or specific terms)
    quoted = re.findall(r'["\']([^"\']+)["\']', prompt)
    keywords.extend(quoted)

    # Deduplicate while preserving order
    seen = set()
    unique_keywords = []
    for k in keywords:
        if k not in seen:
            seen.add(k)
            unique_keywords.append(k)

    return unique_keywords[:10]  # Limit to top 10 keywords


def search_codebase(keywords: List[str], project_dir: str) -> Dict[str, List[str]]:
    """Search for files containing keywords using ripgrep"""
    relevant_files = {}

    for keyword in keywords:
        try:
            # Use ripgrep for fast searching
            result = subprocess.run(
                [
                    "rg",
                    "-l",
                    "--type-add",
                    "code:*.{py,js,ts,jsx,tsx,go,rs,java,cpp,c,h}",
                    "-t",
                    "code",
                    "-i",
                    keyword,
                    "--max-count",
                    "5",
                ],
                cwd=project_dir,
                capture_output=True,
                text=True,
                timeout=2,
            )

            if result.returncode == 0 and result.stdout:
                files = result.stdout.strip().split("\n")
                for file in files[:3]:  # Limit files per keyword
                    if file not in relevant_files:
                        relevant_files[file] = []
                    relevant_files[file].append(keyword)

        except (subprocess.TimeoutExpired, FileNotFoundError):
            # Fallback to find if rg not available
            try:
                result = subprocess.run(
                    ["find", ".", "-type", "f", "-name", f"*{keyword}*"],
                    cwd=project_dir,
                    capture_output=True,
                    text=True,
                    timeout=2,
                )
                if result.returncode == 0 and result.stdout:
                    files = result.stdout.strip().split("\n")
                    for file in files[:2]:
                        if file.startswith("./"):
                            file = file[2:]
                        if file not in relevant_files:
                            relevant_files[file] = []
                        relevant_files[file].append(keyword)
            except Exception:
                pass

    return relevant_files


def get_recent_changes(files: List[str], project_dir: str) -> Dict[str, str]:
    """Get recent git changes for relevant files"""
    changes = {}

    for file in files[:5]:  # Limit to top 5 files
        try:
            # Get last commit message for this file
            result = subprocess.run(
                ["git", "log", "--oneline", "-1", "--", file],
                cwd=project_dir,
                capture_output=True,
                text=True,
                timeout=1,
            )

            if result.returncode == 0 and result.stdout:
                changes[file] = result.stdout.strip()

        except Exception:
            pass

    return changes


def analyze_intent(prompt: str) -> str:
    """Analyze the intent of the prompt to provide better context"""
    prompt_lower = prompt.lower()

    intents = []

    # Detect different types of requests
    if any(
        word in prompt_lower
        for word in ["bug", "error", "fix", "broken", "issue", "problem"]
    ):
        intents.append("debugging")

    if any(
        word in prompt_lower
        for word in ["test", "spec", "coverage", "unit", "integration"]
    ):
        intents.append("testing")

    if any(
        word in prompt_lower
        for word in ["refactor", "clean", "optimize", "improve", "performance"]
    ):
        intents.append("refactoring")

    if any(
        word in prompt_lower
        for word in ["implement", "add", "feature", "create", "new"]
    ):
        intents.append("feature_development")

    if any(
        word in prompt_lower
        for word in ["document", "docs", "readme", "comment", "explain"]
    ):
        intents.append("documentation")

    if any(
        word in prompt_lower
        for word in ["security", "vulnerability", "auth", "permission", "access"]
    ):
        intents.append("security")

    return ", ".join(intents) if intents else "general"


def generate_context(prompt: str, project_dir: str) -> str:
    """Generate additional context based on prompt analysis"""
    keywords = extract_keywords(prompt)
    intent = analyze_intent(prompt)

    context_parts = []

    # Add intent-based context
    if intent != "general":
        context_parts.append(f"🎯 Detected intent: {intent}")

    # Search for relevant files
    if keywords:
        context_parts.append(f"🔍 Key terms identified: {', '.join(keywords[:5])}")

        relevant_files = search_codebase(keywords, project_dir)

        if relevant_files:
            # Sort by relevance (number of keyword matches)
            sorted_files = sorted(
                relevant_files.items(), key=lambda x: len(x[1]), reverse=True
            )

            context_parts.append("\n📁 Relevant files found:")
            for file, matched_keywords in sorted_files[:5]:
                context_parts.append(
                    f"  • {file} (matches: {', '.join(set(matched_keywords))})"
                )

            # Get recent changes for top files
            top_files = [f for f, _ in sorted_files[:3]]
            recent_changes = get_recent_changes(top_files, project_dir)

            if recent_changes:
                context_parts.append("\n📝 Recent changes to relevant files:")
                for file, commit in recent_changes.items():
                    context_parts.append(f"  • {file}: {commit}")

    # Add intent-specific suggestions
    if "debugging" in intent:
        context_parts.append(
            "\n🐛 Debugging context: Consider checking error logs, test failures, and recent commits"
        )
    elif "testing" in intent:
        context_parts.append(
            "\n🧪 Testing context: Look for existing test patterns and coverage reports"
        )
    elif "security" in intent:
        context_parts.append(
            "\n🔒 Security context: Review authentication, authorization, and input validation"
        )

    return "\n".join(context_parts) if context_parts else ""


def main():
    try:
        # Read hook data from stdin
        data = json.load(sys.stdin)
        prompt = data.get("prompt", "")

        # Get project directory from environment
        project_dir = data.get("cwd") or data.get("project_dir") or "."

        if not prompt:
            sys.exit(0)

        # Generate additional context
        additional_context = generate_context(prompt, project_dir)

        if additional_context:
            # Output the context - it will be added to Claude's context
            print("=" * 60)
            print("🤖 Smart Context Injection")
            print("=" * 60)
            print(additional_context)
            print("=" * 60)

        sys.exit(0)

    except Exception as e:
        # Log error but don't block the prompt
        print(f"Context injection error: {str(e)}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
