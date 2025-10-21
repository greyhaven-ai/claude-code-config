#!/usr/bin/env python3
"""
Run tests for Grey Haven applications with Doppler environment variables.

Supports Vitest (TypeScript) and pytest (Python) with markers for different
test types (unit, integration, e2e, benchmark).

Usage:
# Run all tests with test environment
python scripts/run_tests.py

# Run unit tests only
python scripts/run_tests.py --type unit

# Run integration and e2e tests
python scripts/run_tests.py --type integration --type e2e

# Run tests with coverage
python scripts/run_tests.py --coverage

# Run tests in watch mode (for development)
python scripts/run_tests.py --watch

# Run pytest instead of Vitest
python scripts/run_tests.py --backend pytest

# Run with specific Doppler environment
python scripts/run_tests.py --env ci

Always run with --help first to see all options.
"""

import argparse
import subprocess
import sys
from typing import List


def run_command(cmd: str, description: str) -> bool:
"""Run a shell command and return success status."""
print(f"\n→ {description}")
print(f" Command: {cmd}\n")

result = subprocess.run(cmd, shell=True)
return result.returncode == 0


def main():
parser = argparse.ArgumentParser(
description="Run tests with Doppler environment variables",
formatter_class=argparse.RawDescriptionHelpFormatter,
epilog="""
Examples:
# Run all Vitest tests
python scripts/run_tests.py

# Run unit tests only
python scripts/run_tests.py --type unit

# Run integration and e2e tests with coverage
python scripts/run_tests.py --type integration --type e2e --coverage

# Run pytest unit tests
python scripts/run_tests.py --backend pytest --type unit

# Run tests in watch mode
python scripts/run_tests.py --watch

Test Types (Markers):
unit - Unit tests (fast, isolated)
integration - Integration tests (database, external services)
e2e - End-to-end tests (full application flow)
benchmark - Performance benchmark tests

Backends:
vitest - Vitest (TypeScript/React) - default
pytest - pytest (Python/FastAPI)

Doppler Configuration:
Uses 'test' config by default.
Override with --env flag for CI environments.
"""
)

parser.add_argument(
"--backend",
default="vitest",
choices=["vitest", "pytest"],
help="Test backend to use (default: vitest)"
)
parser.add_argument(
"--type",
action="append",
choices=["unit", "integration", "e2e", "benchmark"],
help="Test type(s) to run (can be repeated). If not specified, runs all tests."
)
parser.add_argument(
"--coverage",
action="store_true",
help="Run with coverage reporting"
)
parser.add_argument(
"--watch",
action="store_true",
help="Run in watch mode (for development)"
)
parser.add_argument(
"--env",
default="test",
help="Doppler environment config to use (default: test)"
)
parser.add_argument(
"--verbose",
action="store_true",
help="Verbose output"
)

args = parser.parse_args()

backend = args.backend
env = args.env
test_types = args.type or []

print(f"\n{'=' * 70}")
print(f" Running {backend.upper()} Tests")
print(f" Environment: {env}")
if test_types:
print(f" Types: {', '.join(test_types)}")
print(f"{'=' * 70}")

# Construct test command based on backend
if backend == "vitest":
# Base Vitest command
cmd_parts = ["doppler", "run", "--config", env, "--", "vitest"]

# Add test types as grep patterns
if test_types:
# Vitest uses file patterns or test name patterns
# We'll use test name patterns matching our markers
patterns = "|".join(test_types)
cmd_parts.extend(["-t", f"({patterns})"])

# Add coverage flag
if args.coverage:
cmd_parts.append("--coverage")

# Add watch mode
if args.watch:
cmd_parts.append("--watch")

# Add verbose flag
if args.verbose:
cmd_parts.append("--reporter=verbose")

# Run mode (not watch)
if not args.watch:
cmd_parts.append("run")

elif backend == "pytest":
# Base pytest command
cmd_parts = ["doppler", "run", "--config", env, "--", "pytest"]

# Add test types as markers
if test_types:
markers = " or ".join(test_types)
cmd_parts.extend(["-m", markers])

# Add coverage flag
if args.coverage:
cmd_parts.extend([
"--cov=app",
"--cov-report=term-missing",
"--cov-report=html"
])

# Add verbose flag
if args.verbose:
cmd_parts.append("-vv")

# pytest doesn't have built-in watch mode
if args.watch:
print("\nWARNING: Warning: pytest doesn't support watch mode natively")
print(" Consider using pytest-watch: pip install pytest-watch")

cmd = " ".join(cmd_parts)
success = run_command(cmd, f"Running {backend} tests")

if not success:
print(f"\nERROR: Tests failed")
sys.exit(1)

# Coverage threshold check (if coverage was run)
if args.coverage and backend == "vitest":
print("\n→ Checking coverage thresholds...")
print(" Required: 80% (lines, functions, branches, statements)")

# Vitest coverage is configured in vitest.config.ts
# Thresholds are enforced automatically
print(" ✓ Coverage thresholds enforced by Vitest config")

elif args.coverage and backend == "pytest":
print("\n→ Checking coverage thresholds...")
print(" Required: 80% coverage")

# Check coverage with pytest-cov
coverage_cmd = f"doppler run --config {env} -- pytest --cov=app --cov-fail-under=80 -q"
coverage_success = run_command(coverage_cmd, "Validating coverage threshold")

if not coverage_success:
print("\nERROR: Coverage below 80% threshold")
print(" Add more tests to increase coverage")
sys.exit(1)

# Success!
print(f"\n{'=' * 70}")
print(f" SUCCESS: All tests passed!")
print(f"{'=' * 70}")

if args.coverage:
if backend == "vitest":
print("\n Coverage report: coverage/index.html")
else:
print("\n Coverage report: htmlcov/index.html")

print("\nNext steps:")
if not test_types:
print(" • All tests passed - ready to commit")
else:
print(f" • {', '.join(test_types)} tests passed")
if not args.coverage:
print(" • Run with --coverage to check code coverage")
print(" • Deploy with: python scripts/deploy.py --env staging")


if __name__ == "__main__":
main()
