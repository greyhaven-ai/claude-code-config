#!/usr/bin/env python3
"""
Run database migrations for Grey Haven applications with Doppler.

Supports both Drizzle (TypeScript) and Alembic (Python) migrations
across multiple environments.

Usage:
# Run migrations for development
python scripts/migrate.py --env dev

# Run migrations for staging
python scripts/migrate.py --env staging

# Run migrations for production (with confirmation)
python scripts/migrate.py --env production

# Rollback last migration
python scripts/migrate.py --env dev --rollback

# Rollback to specific migration
python scripts/migrate.py --env dev --rollback --to 20250115_add_users

# Dry run (show what would happen)
python scripts/migrate.py --env production --dry-run

# Use Alembic instead of Drizzle
python scripts/migrate.py --env dev --backend alembic

Always run with --help first to see all options.
"""

import argparse
import subprocess
import sys
from typing import Optional


def run_command(cmd: str, description: str, dry_run: bool = False) -> bool:
"""Run a shell command and return success status."""
print(f"\n{'[DRY RUN] ' if dry_run else ''}→ {description}")
print(f" Command: {cmd}")

if dry_run:
return True

result = subprocess.run(cmd, shell=True, capture_output=False)
return result.returncode == 0


def confirm_production_migration() -> bool:
"""Ask for confirmation before production migration."""
print("\nWARNING: WARNING: You are about to run migrations on PRODUCTION database")
print("This operation is IRREVERSIBLE and will affect live data.")
response = input("Type 'run production migrations' to confirm: ")
return response.strip().lower() == "run production migrations"


def main():
parser = argparse.ArgumentParser(
description="Run database migrations with Doppler environment variables",
formatter_class=argparse.RawDescriptionHelpFormatter,
epilog="""
Examples:
# Run Drizzle migrations for development
python scripts/migrate.py --env dev

# Rollback last Drizzle migration
python scripts/migrate.py --env dev --rollback

# Run Alembic migrations for staging
python scripts/migrate.py --env staging --backend alembic

# Rollback to specific Alembic migration
python scripts/migrate.py --env staging --backend alembic --rollback --to abc123

Environments:
dev - Local development database
test - CI/CD test database
staging - Staging database
production - Production database (requires confirmation)

Backends:
drizzle - Drizzle Kit (TypeScript/TanStack Start)
alembic - Alembic (Python/FastAPI)

Doppler Configuration:
Requires doppler CLI configured with appropriate access.
Uses DATABASE_URL_ADMIN from Doppler config.
"""
)

parser.add_argument(
"--env",
required=True,
choices=["dev", "test", "staging", "production"],
help="Environment to run migrations against"
)
parser.add_argument(
"--backend",
default="drizzle",
choices=["drizzle", "alembic"],
help="Migration backend to use (default: drizzle)"
)
parser.add_argument(
"--rollback",
action="store_true",
help="Rollback migrations instead of applying"
)
parser.add_argument(
"--to",
type=str,
help="Rollback to specific migration (use with --rollback)"
)
parser.add_argument(
"--dry-run",
action="store_true",
help="Show what would happen without executing"
)

args = parser.parse_args()

# Production confirmation
if args.env == "production" and not args.dry_run and not args.rollback:
if not confirm_production_migration():
print("\nERROR: Production migration cancelled")
sys.exit(1)

env = args.env
backend = args.backend

print(f"\n{'=' * 70}")
print(f" Database Migration - {env.upper()} ({backend.upper()})")
print(f"{'=' * 70}")

# Check Doppler configuration
if not args.dry_run:
result = subprocess.run(
f"doppler secrets get DATABASE_URL_ADMIN --config {env}",
shell=True,
capture_output=True
)
if result.returncode != 0:
print(f"\nERROR: Failed to get DATABASE_URL_ADMIN from Doppler config '{env}'")
print(" Make sure Doppler is configured: doppler setup")
sys.exit(1)

# Construct migration command
if backend == "drizzle":
if args.rollback:
if args.to:
cmd = f"doppler run --config {env} -- drizzle-kit migrate:rollback --to {args.to}"
else:
cmd = f"doppler run --config {env} -- drizzle-kit migrate:rollback"
description = "Rolling back Drizzle migration"
else:
cmd = f"doppler run --config {env} -- drizzle-kit push:pg"
description = "Applying Drizzle migrations"

elif backend == "alembic":
if args.rollback:
if args.to:
cmd = f"doppler run --config {env} -- alembic downgrade {args.to}"
else:
cmd = f"doppler run --config {env} -- alembic downgrade -1"
description = "Rolling back Alembic migration"
else:
cmd = f"doppler run --config {env} -- alembic upgrade head"
description = "Applying Alembic migrations"

# Run migration
success = run_command(cmd, description, args.dry_run)

if not success:
print(f"\nERROR: Migration failed for {env}")
sys.exit(1)

# Success!
print(f"\n{'=' * 70}")
if args.rollback:
print(f" SUCCESS: Rollback successful for {env.upper()}")
else:
print(f" SUCCESS: Migration successful for {env.upper()}")
print(f"{'=' * 70}")

if not args.rollback:
print("\nNext steps:")
print(" • Verify schema changes in database")
print(" • Run tests: doppler run --config test -- npm run test")
print(" • Deploy application if migrations succeeded")
else:
print("\nNext steps:")
print(" • Verify rollback was successful")
print(" • Re-deploy previous application version if needed")


if __name__ == "__main__":
main()
