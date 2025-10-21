#!/usr/bin/env python3
"""
Rollback Grey Haven Cloudflare Workers deployment to previous version.

This script handles emergency rollbacks when a deployment fails or causes
production issues. It can rollback both the Workers deployment and database
migrations.

Usage:
    # Rollback to previous Workers deployment
    python scripts/rollback.py --env production

    # Rollback Workers and database migration
    python scripts/rollback.py --env production --with-migration

    # Rollback to specific deployment ID
    python scripts/rollback.py --env production --deployment-id abc123

    # Rollback database only
    python scripts/rollback.py --env production --migration-only

    # Dry run (show what would happen)
    python scripts/rollback.py --env production --dry-run

Always run with --help first to see all options.
"""

import argparse
import subprocess
import sys
from typing import Optional


def run_command(cmd: str, description: str, dry_run: bool = False, capture: bool = False) -> tuple[bool, Optional[str]]:
    """Run a shell command and return success status and output."""
    print(f"\n{'[DRY RUN] ' if dry_run else ''}→ {description}")
    print(f"  Command: {cmd}")

    if dry_run:
        return True, None

    result = subprocess.run(cmd, shell=True, capture_output=capture, text=True)
    return result.returncode == 0, result.stdout if capture else None


def confirm_production_rollback() -> bool:
    """Ask for confirmation before production rollback."""
    print("\n⚠️  WARNING: You are about to ROLLBACK PRODUCTION deployment")
    print("This will affect live users immediately.")
    response = input("Type 'rollback production' to confirm: ")
    return response.strip().lower() == "rollback production"


def get_wrangler_config(env: str) -> str:
    """Get the appropriate wrangler config file for environment."""
    if env == "production":
        return "wrangler.production.toml"
    elif env == "staging":
        return "wrangler.staging.toml"
    else:
        return "wrangler.toml"


def list_recent_deployments(wrangler_config: str, dry_run: bool = False) -> None:
    """List recent deployments for reference."""
    if dry_run:
        print("\n[DRY RUN] → Would list recent deployments")
        return

    print("\n→ Fetching recent deployments...")
    subprocess.run(
        f"npx wrangler deployments list --config {wrangler_config}",
        shell=True
    )


def main():
    parser = argparse.ArgumentParser(
        description="Rollback Grey Haven Cloudflare Workers deployment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Emergency rollback of production Workers deployment
  python scripts/rollback.py --env production

  # Rollback Workers and database migration
  python scripts/rollback.py --env production --with-migration

  # Rollback to specific deployment
  python scripts/rollback.py --env production --deployment-id abc123

  # Rollback database migration only
  python scripts/rollback.py --env production --migration-only --backend drizzle

Environments:
  dev        - Development
  staging    - Staging
  production - Production (requires confirmation)

Emergency Rollback Procedure:
  1. Identify the issue (check Sentry, Axiom, Cloudflare logs)
  2. Run rollback script with appropriate flags
  3. Verify rollback with smoke tests
  4. Notify team and update Linear issue
  5. Create postmortem for root cause analysis
        """
    )

    parser.add_argument(
        "--env",
        required=True,
        choices=["dev", "staging", "production"],
        help="Environment to rollback"
    )
    parser.add_argument(
        "--deployment-id",
        type=str,
        help="Specific deployment ID to rollback to (optional)"
    )
    parser.add_argument(
        "--with-migration",
        action="store_true",
        help="Also rollback database migration"
    )
    parser.add_argument(
        "--migration-only",
        action="store_true",
        help="Rollback database migration only (not Workers)"
    )
    parser.add_argument(
        "--backend",
        default="drizzle",
        choices=["drizzle", "alembic"],
        help="Migration backend (default: drizzle)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would happen without executing"
    )

    args = parser.parse_args()

    # Production confirmation
    if args.env == "production" and not args.dry_run:
        if not confirm_production_rollback():
            print("\n❌ Production rollback cancelled")
            sys.exit(1)

    env = args.env
    wrangler_config = get_wrangler_config(env)

    print(f"\n{'=' * 70}")
    print(f"  Emergency Rollback - {env.upper()}")
    print(f"{'=' * 70}")

    # Rollback Workers deployment (unless migration-only)
    if not args.migration_only:
        # List recent deployments first
        if not args.deployment_id:
            list_recent_deployments(wrangler_config, args.dry_run)

        # Construct rollback command
        if args.deployment_id:
            cmd = f"npx wrangler rollback --deployment-id {args.deployment_id} --config {wrangler_config}"
            description = f"Rolling back to deployment {args.deployment_id}"
        else:
            cmd = f"npx wrangler rollback --config {wrangler_config}"
            description = "Rolling back to previous deployment"

        success, _ = run_command(cmd, description, args.dry_run)

        if not success:
            print(f"\n❌ Workers rollback failed for {env}")
            sys.exit(1)

        print(f"\n✅ Workers deployment rolled back successfully")

    # Rollback database migration (if requested)
    if args.with_migration or args.migration_only:
        backend = args.backend

        print(f"\n→ Rolling back {backend} migration for {env}")

        if backend == "drizzle":
            cmd = f"doppler run --config {env} -- drizzle-kit migrate:rollback"
        elif backend == "alembic":
            cmd = f"doppler run --config {env} -- alembic downgrade -1"

        success, _ = run_command(cmd, f"Rolling back {backend} migration", args.dry_run)

        if not success:
            print(f"\n❌ Database migration rollback failed for {env}")
            sys.exit(1)

        print(f"\n✅ Database migration rolled back successfully")

    # Success!
    print(f"\n{'=' * 70}")
    print(f"  ✅ Rollback complete for {env.upper()}")
    print(f"{'=' * 70}")

    # Run smoke tests
    print("\n→ Running smoke tests to verify rollback...")
    success, _ = run_command(
        f"doppler run --config {env} -- npm run test:e2e:smoke",
        "Verifying rollback with smoke tests",
        args.dry_run
    )

    if not success:
        print("\n⚠️  Warning: Smoke tests failed after rollback")
        print("  Manual verification required!")
    else:
        print("\n✅ Smoke tests passed - rollback verified")

    # Post-rollback checklist
    print("\n📋 Post-Rollback Checklist:")
    print("  ✓ Deployment rolled back")
    if args.with_migration or args.migration_only:
        print("  ✓ Database migration rolled back")
    print("\n  ⚠️  Action Items:")
    print("  • Check Sentry for errors")
    print("  • Verify Axiom logs")
    print("  • Monitor Cloudflare Workers analytics")
    print("  • Update Linear issue with rollback status")
    print("  • Create postmortem for root cause analysis")
    print("  • Fix the issue before re-deploying")

    if env == "production":
        print(f"\n🌐 Production URL: https://app.greyhaven.studio")
    elif env == "staging":
        print(f"\n🌐 Staging URL: https://staging.greyhaven.studio")
    else:
        print(f"\n🌐 Dev URL: https://dev.greyhaven.studio")


if __name__ == "__main__":
    main()
