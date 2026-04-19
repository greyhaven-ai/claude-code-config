#!/usr/bin/env python3
"""Cross-reference linter for the Grey Haven plugin suite.

Scans every SKILL.md, agent .md, and workflow/reference .md under
`grey-haven-plugins/` and verifies that every skill or agent reference
resolves to something that actually exists in the repo.

Catches:
  - `skills:` frontmatter entries that point to missing skills
  - "Related Agents" entries that point to missing agents
  - Legacy `grey-haven-<name>` references left over after renames
  - Inline backtick-quoted skill names that don't resolve

Exit codes:
  0 = clean
  1 = issues found
  2 = invocation error (bad path, etc.)

Usage:
  python3 cross_ref_lint.py [PLUGINS_DIR]
  python3 cross_ref_lint.py --format=github   # GitHub Actions annotations
  python3 cross_ref_lint.py --strict          # fail on legacy refs too

Runs with the Python standard library only — no PyYAML dependency.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Finding:
    path: Path
    line: int
    kind: str
    message: str


@dataclass
class Report:
    findings: list[Finding] = field(default_factory=list)
    skills_seen: set[str] = field(default_factory=set)
    agents_seen: set[str] = field(default_factory=set)

    def add(self, path: Path, line: int, kind: str, message: str) -> None:
        self.findings.append(Finding(path, line, kind, message))

    def by_kind(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for f in self.findings:
            counts[f.kind] = counts.get(f.kind, 0) + 1
        return counts


FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n?(.*)", re.DOTALL)


def parse_frontmatter(text: str) -> tuple[dict[str, object], str, int]:
    """Return (frontmatter_dict, body, body_start_line) — minimal YAML subset."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}, text, 1
    fm_text, body = m.group(1), m.group(2)
    fm_lines = fm_text.count("\n") + 3  # 2 for `---` fences, 1 for the line after
    fm = _parse_minimal_yaml(fm_text)
    return fm, body, fm_lines


def _parse_minimal_yaml(text: str) -> dict[str, object]:
    """Parse just the subset we need: scalars, simple lists.

    Handles:
      key: value
      key: "quoted value"
      key:
        - item
        - item
    """
    out: dict[str, object] = {}
    current_list_key: str | None = None
    for raw in text.split("\n"):
        line = raw.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        # List item continuation
        m = re.match(r"^\s+-\s*(.+?)\s*$", line)
        if m and current_list_key is not None:
            val = m.group(1).strip().strip('"').strip("'")
            lst = out.setdefault(current_list_key, [])
            if isinstance(lst, list):
                lst.append(val)
            continue
        # Key: value or Key: (start of list/block)
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*)\s*:\s*(.*)$", line)
        if m:
            key, val = m.group(1), m.group(2).strip()
            if val == "":
                current_list_key = key
                out.setdefault(key, [])
            else:
                current_list_key = None
                out[key] = val.strip('"').strip("'")
            continue
        current_list_key = None
    return out


def collect_inventory(plugins_dir: Path) -> tuple[dict[str, Path], dict[str, Path]]:
    """Map skill and agent names → source paths."""
    skills: dict[str, Path] = {}
    agents: dict[str, Path] = {}

    for skill_md in plugins_dir.glob("*/skills/*/SKILL.md"):
        fm, _, _ = parse_frontmatter(skill_md.read_text())
        name = str(fm.get("name") or skill_md.parent.name)
        skills[name] = skill_md

    for agent_md in plugins_dir.glob("*/agents/*.md"):
        fm, _, _ = parse_frontmatter(agent_md.read_text())
        name = str(fm.get("name") or agent_md.stem)
        agents[name] = agent_md

    return skills, agents


LEGACY_REF_RE = re.compile(r"grey-haven-[a-z][a-z0-9-]*")
BACKTICK_NAME_RE = re.compile(r"`([a-z][a-z0-9-]{2,})`")
RELATED_AGENTS_HDR = re.compile(r"^##+\s+Related Agents\s*$", re.MULTILINE)

# Names that *look* like legacy skill refs but are actually legitimate
# identifiers (directory paths, repo names, external service project names,
# documentation placeholders, template file names).
LEGACY_IGNORE: set[str] = {
    "grey-haven-plugins",            # the plugin directory in this repo
    "grey-haven-claude-code-config", # this repo's own name
    "grey-haven-docs",               # Cloudflare Pages project name
    "grey-haven-skill-name",         # documentation placeholder
    "grey-haven-conventions",        # filename in project-scaffolding/reference
}


def check_skill_frontmatter(
    path: Path, fm: dict[str, object], known_skills: set[str], report: Report
) -> None:
    skills_field = fm.get("skills")
    if not isinstance(skills_field, list):
        return
    for ref in skills_field:
        ref = str(ref)
        if ref not in known_skills:
            report.add(
                path,
                0,
                "frontmatter-skill-missing",
                f"`skills:` entry '{ref}' does not resolve to any known skill",
            )


def check_agent_frontmatter(
    path: Path, fm: dict[str, object], known_skills: set[str], report: Report
) -> None:
    skills_field = fm.get("skills")
    if not isinstance(skills_field, list):
        return
    for ref in skills_field:
        ref = str(ref)
        if ref not in known_skills:
            report.add(
                path,
                0,
                "frontmatter-skill-missing",
                f"agent `skills:` entry '{ref}' does not resolve to any known skill",
            )


def check_related_agents(
    path: Path, body: str, body_offset: int, known_agents: set[str], report: Report
) -> None:
    """Scan a skill body for a Related Agents section and validate the names."""
    m = RELATED_AGENTS_HDR.search(body)
    if not m:
        return
    section_start = m.end()
    # End at the next ## heading or EOF
    next_h = re.search(r"^##+\s+", body[section_start:], re.MULTILINE)
    section_end = section_start + (next_h.start() if next_h else len(body))
    section = body[section_start:section_end]
    for lm in re.finditer(r"^-\s*`([a-zA-Z0-9_-]+)`", section, re.MULTILINE):
        name = lm.group(1)
        line = body_offset + body[: section_start + lm.start()].count("\n")
        if name not in known_agents:
            report.add(
                path,
                line,
                "related-agent-missing",
                f"'Related Agents' entry '{name}' has no matching agent file",
            )


def _is_path_context(body: str, start: int) -> bool:
    """True when the match sits inside a path-like context (`./foo/grey-haven-...`)."""
    prev = body[max(0, start - 3) : start]
    return prev.endswith(("./", "//", ".", "/"))


def _is_counter_example(body: str, start: int) -> bool:
    """True for 'not `grey-haven-X`' patterns used as deliberate counter-examples."""
    window = body[max(0, start - 20) : start]
    return bool(re.search(r"\bnot\s+[`'\"]?$", window))


def _is_markdown_link_target(body: str, start: int) -> bool:
    """True when inside a markdown link like [text](grey-haven-...)."""
    return start > 0 and body[start - 1] == "("


def check_legacy_refs(
    path: Path, body: str, body_offset: int, report: Report, strict: bool
) -> None:
    # CHANGELOG is a historical record; skip entirely.
    if path.name == "CHANGELOG.md":
        return
    for lm in LEGACY_REF_RE.finditer(body):
        ref = lm.group(0)
        if ref in LEGACY_IGNORE:
            continue
        if _is_path_context(body, lm.start()):
            continue
        if _is_counter_example(body, lm.start()):
            continue
        if _is_markdown_link_target(body, lm.start()):
            continue
        line = body_offset + body[: lm.start()].count("\n")
        kind = "legacy-ref" if strict else "legacy-ref-info"
        report.add(
            path,
            line,
            kind,
            f"legacy reference '{ref}' — should be renamed without the grey-haven- prefix",
        )


def check_inline_skill_refs(
    path: Path,
    body: str,
    body_offset: int,
    known_skills: set[str],
    known_agents: set[str],
    report: Report,
) -> None:
    """Flag `name-like` backtick references that look like skills/agents but don't resolve.

    Conservative — only flags refs that both look skill-like AND sit near the
    text 'skill' or in a Works-Best-With / Integrates-With section, to avoid
    false positives on arbitrary variable names in code blocks.
    """
    # Skip code blocks
    cleaned = re.sub(r"```.*?```", "", body, flags=re.DOTALL)
    for lm in re.finditer(
        r"(?:(?:Works Best With|Integrates With|Complements|Auto-loads)[^\n]*\n(?:[-*][^\n]*\n){0,20})",
        cleaned,
    ):
        block = lm.group(0)
        line0 = body_offset + cleaned[: lm.start()].count("\n")
        for bt in BACKTICK_NAME_RE.finditer(block):
            name = bt.group(1)
            if name in known_skills or name in known_agents:
                continue
            if name in {"true", "false", "null", "pytest", "vitest"}:
                continue
            line = line0 + block[: bt.start()].count("\n")
            report.add(
                path,
                line,
                "inline-ref-missing",
                f"inline reference `{name}` in integration section resolves to neither a skill nor an agent",
            )


def lint(plugins_dir: Path, strict: bool, report: Report) -> None:
    skills, agents = collect_inventory(plugins_dir)
    known_skills = set(skills.keys())
    known_agents = set(agents.keys())
    report.skills_seen = known_skills
    report.agents_seen = known_agents

    # Walk all relevant markdown files
    for md in plugins_dir.rglob("*.md"):
        # Skip skill supporting docs that aren't SKILL.md, but keep agents and workflows
        text = md.read_text(errors="replace")
        fm, body, body_offset = parse_frontmatter(text)

        if md.name == "SKILL.md":
            check_skill_frontmatter(md, fm, known_skills, report)
            check_related_agents(md, body, body_offset, known_agents, report)
        elif md.parent.name == "agents":
            check_agent_frontmatter(md, fm, known_skills, report)

        check_legacy_refs(md, body, body_offset, report, strict)
        check_inline_skill_refs(md, body, body_offset, known_skills, known_agents, report)


def format_human(report: Report) -> str:
    lines: list[str] = []
    lines.append(
        f"Inventory: {len(report.skills_seen)} skills, {len(report.agents_seen)} agents"
    )
    lines.append("")
    if not report.findings:
        lines.append("No cross-reference issues found.")
        return "\n".join(lines)

    by_kind: dict[str, list[Finding]] = {}
    for f in report.findings:
        by_kind.setdefault(f.kind, []).append(f)

    for kind, findings in sorted(by_kind.items()):
        lines.append(f"[{kind}] ({len(findings)})")
        for f in findings:
            loc = f"{f.path}:{f.line}" if f.line else str(f.path)
            lines.append(f"  {loc}  {f.message}")
        lines.append("")

    lines.append(f"Total: {len(report.findings)} findings across {len(by_kind)} categories")
    return "\n".join(lines)


def format_github(report: Report) -> str:
    out: list[str] = []
    for f in report.findings:
        level = "warning" if f.kind.endswith("-info") else "error"
        loc = f"file={f.path}"
        if f.line:
            loc += f",line={f.line}"
        out.append(f"::{level} {loc}::[{f.kind}] {f.message}")
    return "\n".join(out)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.strip().split("\n")[0])
    ap.add_argument(
        "plugins_dir",
        nargs="?",
        default="grey-haven-plugins",
        help="Path to the plugins directory (default: grey-haven-plugins)",
    )
    ap.add_argument("--format", choices=("human", "github"), default="human")
    ap.add_argument(
        "--strict",
        action="store_true",
        help="Treat legacy grey-haven-* refs as errors (default: informational)",
    )
    args = ap.parse_args(argv)

    plugins_dir = Path(args.plugins_dir)
    if not plugins_dir.is_dir():
        print(f"Not a directory: {plugins_dir}", file=sys.stderr)
        return 2

    report = Report()
    lint(plugins_dir, args.strict, report)

    output = format_github(report) if args.format == "github" else format_human(report)
    print(output)

    hard_errors = [
        f for f in report.findings if not f.kind.endswith("-info")
    ]
    return 1 if hard_errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
