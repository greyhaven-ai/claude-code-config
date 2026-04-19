#!/usr/bin/env python3
"""Bump the `version` field across every plugin.json in lockstep.

The Grey Haven plugin suite is versioned in lockstep — every plugin.json
ships with the same version number. This helper keeps them synchronized.

Usage:
  bump_plugin_versions.py --check
  bump_plugin_versions.py --bump {patch,minor,major}
  bump_plugin_versions.py --version X.Y.Z

Exit codes:
  0 = success (or clean lockstep on --check)
  1 = versions out of lockstep (on --check) or logical error
  2 = invocation error (bad args, missing files)

Stdlib only — no PyYAML/semver dependencies.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

DEFAULT_PLUGINS_DIR = Path("grey-haven-plugins")
SEMVER_RE = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")


def find_plugin_jsons(plugins_dir: Path) -> list[Path]:
    return sorted(plugins_dir.glob("*/.claude-plugin/plugin.json"))


def bump_semver(current: str, bump_type: str) -> str:
    m = SEMVER_RE.match(current)
    if not m:
        raise ValueError(f"not a semver: '{current}'")
    major, minor, patch = int(m.group(1)), int(m.group(2)), int(m.group(3))
    if bump_type == "patch":
        patch += 1
    elif bump_type == "minor":
        minor += 1
        patch = 0
    elif bump_type == "major":
        major += 1
        minor = 0
        patch = 0
    else:
        raise ValueError(f"unknown bump type: '{bump_type}'")
    return f"{major}.{minor}.{patch}"


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.strip().split("\n")[0])
    ap.add_argument(
        "--plugins-dir",
        type=Path,
        default=DEFAULT_PLUGINS_DIR,
        help=f"Path to plugins directory (default: {DEFAULT_PLUGINS_DIR})",
    )
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--check",
        action="store_true",
        help="Report current versions; exit 1 if not in lockstep",
    )
    group.add_argument(
        "--bump",
        choices=("patch", "minor", "major"),
        help="Semver bump type (requires all plugins already in lockstep)",
    )
    group.add_argument(
        "--version",
        metavar="X.Y.Z",
        help="Set an explicit version (accepted even if current versions are mixed)",
    )
    args = ap.parse_args(argv)

    if not args.plugins_dir.is_dir():
        print(f"Not a directory: {args.plugins_dir}", file=sys.stderr)
        return 2

    plugin_jsons = find_plugin_jsons(args.plugins_dir)
    if not plugin_jsons:
        print(f"No plugin.json files under {args.plugins_dir}", file=sys.stderr)
        return 2

    current: dict[Path, tuple[str, dict]] = {}
    for p in plugin_jsons:
        try:
            data = json.loads(p.read_text())
        except json.JSONDecodeError as e:
            print(f"Invalid JSON in {p}: {e}", file=sys.stderr)
            return 2
        current[p] = (str(data.get("version", "0.0.0")), data)

    distinct = sorted({v for v, _ in current.values()})

    if args.check:
        width = max(len(v) for v, _ in current.values()) + 2
        for p, (v, _) in current.items():
            print(f"{v:<{width}}{p.parent.parent.name}")
        print()
        if len(distinct) == 1:
            print(f"All {len(current)} plugins at {distinct[0]}")
            return 0
        print(f"Out of lockstep: {len(distinct)} distinct versions — {distinct}")
        return 1

    # Determine the new version
    if args.version:
        if not SEMVER_RE.match(args.version):
            print(f"Not a semver: '{args.version}'", file=sys.stderr)
            return 2
        new_version = args.version
    else:
        if len(distinct) > 1:
            print(
                f"Refusing to --bump: versions are out of lockstep ({distinct}). "
                "Pass --version X.Y.Z to reset, or fix first.",
                file=sys.stderr,
            )
            return 1
        try:
            new_version = bump_semver(distinct[0], args.bump)
        except ValueError as e:
            print(f"Cannot bump: {e}", file=sys.stderr)
            return 2

    # Apply in place
    for p, (_, data) in current.items():
        data["version"] = new_version
        p.write_text(json.dumps(data, indent=4) + "\n")

    print(f"Bumped {len(current)} plugins to {new_version}:")
    for p in current:
        print(f"  {p.parent.parent.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
