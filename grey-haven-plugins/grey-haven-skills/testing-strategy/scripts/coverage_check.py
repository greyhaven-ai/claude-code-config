#!/usr/bin/env python3
"""
Check test coverage and enforce 80% minimum threshold for Grey Haven projects.

Analyzes coverage reports from Vitest or pytest and provides detailed
breakdown of coverage by file, function, and line.

Usage:
    # Check Vitest coverage
    python scripts/coverage_check.py

    # Check pytest coverage
    python scripts/coverage_check.py --backend pytest

    # Show detailed file-by-file breakdown
    python scripts/coverage_check.py --detailed

    # Check coverage and fail if below threshold
    python scripts/coverage_check.py --strict

    # Generate coverage report if missing
    python scripts/coverage_check.py --generate

Always run with --help first to see all options.
"""

import argparse
import subprocess
import sys
import json
import os
from pathlib import Path


def run_command(cmd: str, capture: bool = True) -> tuple[bool, str]:
    """Run a shell command and return success status and output."""
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=capture,
        text=True
    )
    return result.returncode == 0, result.stdout if capture else ""


def check_vitest_coverage(detailed: bool = False) -> dict:
    """Check Vitest coverage from coverage/coverage-summary.json."""
    coverage_file = Path("coverage/coverage-summary.json")

    if not coverage_file.exists():
        print("❌ Coverage report not found: coverage/coverage-summary.json")
        print("  Run tests with coverage first:")
        print("  doppler run --config test -- vitest run --coverage")
        sys.exit(1)

    with open(coverage_file) as f:
        coverage_data = json.load(f)

    # Total coverage
    total = coverage_data["total"]

    results = {
        "lines": total["lines"]["pct"],
        "statements": total["statements"]["pct"],
        "functions": total["functions"]["pct"],
        "branches": total["branches"]["pct"],
    }

    # Detailed breakdown by file
    if detailed:
        print("\n📊 Coverage by File:")
        print(f"{'File':<50} {'Lines':<10} {'Funcs':<10} {'Branches':<10}")
        print("=" * 80)

        for file_path, file_data in coverage_data.items():
            if file_path == "total":
                continue

            # Shorten file path for display
            short_path = file_path.replace(os.getcwd(), ".")
            if len(short_path) > 47:
                short_path = "..." + short_path[-44:]

            lines_pct = file_data["lines"]["pct"]
            funcs_pct = file_data["functions"]["pct"]
            branches_pct = file_data["branches"]["pct"]

            # Color code based on coverage
            if lines_pct < 80:
                status = "🔴"
            elif lines_pct < 90:
                status = "🟡"
            else:
                status = "🟢"

            print(f"{status} {short_path:<47} {lines_pct:<9.1f}% {funcs_pct:<9.1f}% {branches_pct:<9.1f}%")

    return results


def check_pytest_coverage(detailed: bool = False) -> dict:
    """Check pytest coverage from .coverage file."""
    coverage_file = Path(".coverage")

    if not coverage_file.exists():
        print("❌ Coverage report not found: .coverage")
        print("  Run tests with coverage first:")
        print("  doppler run --config test -- pytest --cov=app")
        sys.exit(1)

    # Use coverage.py to get report
    success, output = run_command("coverage report --format=total")

    if not success:
        print("❌ Failed to generate coverage report")
        sys.exit(1)

    # Parse total coverage percentage
    total_coverage = float(output.strip().rstrip("%"))

    # Get detailed report if requested
    if detailed:
        print("\n📊 Coverage by File:")
        success, detailed_output = run_command("coverage report")
        print(detailed_output)

    # pytest coverage doesn't separate by type, so we use total for all
    results = {
        "lines": total_coverage,
        "statements": total_coverage,
        "functions": total_coverage,
        "branches": total_coverage,
    }

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Check test coverage and enforce thresholds",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Check Vitest coverage
  python scripts/coverage_check.py

  # Check pytest coverage with detailed breakdown
  python scripts/coverage_check.py --backend pytest --detailed

  # Generate coverage and check (strict mode)
  python scripts/coverage_check.py --generate --strict

Coverage Thresholds:
  Minimum 80% coverage required for:
  - Lines
  - Functions
  - Branches
  - Statements

Backends:
  vitest - Vitest (TypeScript/React) - default
  pytest - pytest (Python/FastAPI)
        """
    )

    parser.add_argument(
        "--backend",
        default="vitest",
        choices=["vitest", "pytest"],
        help="Test backend to check coverage for (default: vitest)"
    )
    parser.add_argument(
        "--detailed",
        action="store_true",
        help="Show detailed file-by-file breakdown"
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with error if coverage below 80 percent"
    )
    parser.add_argument(
        "--generate",
        action="store_true",
        help="Generate coverage report before checking"
    )

    args = parser.parse_args()

    print(f"\n{'=' * 70}")
    print(f"  Coverage Check - {args.backend.upper()}")
    print(f"{'=' * 70}")

    # Generate coverage if requested
    if args.generate:
        print("\n→ Generating coverage report...")

        if args.backend == "vitest":
            cmd = "doppler run --config test -- vitest run --coverage"
        else:
            cmd = "doppler run --config test -- pytest --cov=app --cov-report=term --cov-report=html"

        success, _ = run_command(cmd, capture=False)

        if not success:
            print("\n❌ Failed to generate coverage")
            sys.exit(1)

    # Check coverage
    if args.backend == "vitest":
        coverage = check_vitest_coverage(args.detailed)
    else:
        coverage = check_pytest_coverage(args.detailed)

    # Display summary
    print(f"\n{'=' * 70}")
    print("  Coverage Summary")
    print(f"{'=' * 70}")

    threshold = 80.0
    all_pass = True

    for metric, value in coverage.items():
        if value >= threshold:
            status = "✅"
        else:
            status = "❌"
            all_pass = False

        print(f"{status} {metric.capitalize():<15} {value:>6.2f}% (threshold: {threshold}%)")

    # Overall result
    print(f"\n{'=' * 70}")
    if all_pass:
        print("  ✅ All coverage thresholds met!")
    else:
        print("  ❌ Coverage below 80% threshold")

    print(f"{'=' * 70}")

    # Additional info
    if not all_pass:
        print("\n💡 Tips to improve coverage:")
        print("  • Add unit tests for uncovered functions")
        print("  • Add integration tests for API endpoints")
        print("  • Add edge case tests for conditionals")
        print("  • Test error handling paths")

        if args.backend == "vitest":
            print("\n📊 View detailed report: coverage/index.html")
        else:
            print("\n📊 View detailed report: htmlcov/index.html")

    # Exit with error in strict mode if coverage below threshold
    if args.strict and not all_pass:
        sys.exit(1)


if __name__ == "__main__":
    main()
