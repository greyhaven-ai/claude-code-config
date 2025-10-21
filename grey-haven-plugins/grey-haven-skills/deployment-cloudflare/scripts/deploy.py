#!/usr/bin/env python3
"""
Deploy Grey Haven applications to Cloudflare Workers with Doppler secrets.

This script automates the deployment workflow:
1. Runs tests with Doppler environment
2. Builds the application
3. Runs database migrations
4. Deploys to Cloudflare Workers with Wrangler
5. Injects secrets from Doppler
6. Runs smoke tests
7. Automatically rolls back on failure

Usage:
    # Development deployment
    python scripts/deploy.py --env dev

    # Staging deployment
    python scripts/deploy.py --env staging

    # Production deployment (with confirmation)
    python scripts/deploy.py --env production

    # Skip tests (not recommended)
    python scripts/deploy.py --env staging --skip-tests

    # Dry run (show what would happen)
    python scripts/deploy.py --env production --dry-run

Always run with --help first to see all options.
"""

import argparse
import subprocess
import sys
import json
import os
from typing import Optional


def run_command(cmd: str, description: str, dry_run: bool = False) -> bool:
    """Run a shell command and return success status."""
    print(f"\n{'[DRY RUN] ' if dry_run else ''}→ {description}")
    print(f"  Command: {cmd}")

    if dry_run:
        return True

    result = subprocess.run(cmd, shell=True, capture_output=False)
    return result.returncode == 0


def confirm_production_deploy() -> bool:
    """Ask for confirmation before production deployment."""
    print("\n⚠️  WARNING: You are about to deploy to PRODUCTION")
    print("This will affect live users.")
    response = input("Type 'deploy to production' to confirm: ")
    return response.strip().lower() == "deploy to production"


def get_wrangler_config(env: str) -> str:
    """Get the appropriate wrangler config file for environment."""
    if env == "production":
        return "wrangler.production.toml"
    elif env == "staging":
        return "wrangler.staging.toml"
    else:
        return "wrangler.toml"


def main():
    parser = argparse.ArgumentParser(
        description="Deploy Grey Haven application to Cloudflare Workers",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/deploy.py --env dev
  python scripts/deploy.py --env staging --skip-migrations
  python scripts/deploy.py --env production --dry-run

Environments:
  dev        - Development (wrangler.toml)
  staging    - Staging (wrangler.staging.toml)
  production - Production (wrangler.production.toml)

Doppler Configuration:
  Requires DOPPLER_TOKEN environment variable or doppler CLI configured.
  Secrets are injected from Doppler config matching the environment.
        """
    )

    parser.add_argument(
        "--env",
        required=True,
        choices=["dev", "staging", "production"],
        help="Deployment environment"
    )
    parser.add_argument(
        "--skip-tests",
        action="store_true",
        help="Skip running tests (not recommended)"
    )
    parser.add_argument(
        "--skip-migrations",
        action="store_true",
        help="Skip database migrations"
    )
    parser.add_argument(
        "--skip-smoke-tests",
        action="store_true",
        help="Skip smoke tests after deployment"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would happen without executing"
    )

    args = parser.parse_args()

    # Production confirmation
    if args.env == "production" and not args.dry_run:
        if not confirm_production_deploy():
            print("\n❌ Production deployment cancelled")
            sys.exit(1)

    env = args.env
    wrangler_config = get_wrangler_config(env)

    print(f"\n{'=' * 70}")
    print(f"  Grey Haven Deployment to {env.upper()}")
    print(f"{'=' * 70}")

    # Step 1: Run tests
    if not args.skip_tests:
        success = run_command(
            f"doppler run --config test -- npm run test",
            "Running tests",
            args.dry_run
        )
        if not success:
            print("\n❌ Tests failed. Deployment aborted.")
            sys.exit(1)
    else:
        print("\n⚠️  Skipping tests (--skip-tests)")

    # Step 2: Build application
    success = run_command(
        f"doppler run --config {env} -- npm run build",
        f"Building application for {env}",
        args.dry_run
    )
    if not success:
        print("\n❌ Build failed. Deployment aborted.")
        sys.exit(1)

    # Step 3: Run database migrations
    if not args.skip_migrations:
        success = run_command(
            f"doppler run --config {env} -- npm run db:migrate",
            "Running database migrations",
            args.dry_run
        )
        if not success:
            print("\n❌ Migrations failed. Deployment aborted.")
            sys.exit(1)
    else:
        print("\n⚠️  Skipping migrations (--skip-migrations)")

    # Step 4: Deploy to Cloudflare Workers
    success = run_command(
        f"npx wrangler deploy --config {wrangler_config}",
        f"Deploying to Cloudflare Workers ({wrangler_config})",
        args.dry_run
    )
    if not success:
        print("\n❌ Deployment failed.")
        sys.exit(1)

    # Step 5: Inject Doppler secrets to Cloudflare Workers
    if not args.dry_run:
        print("\n→ Injecting Doppler secrets to Cloudflare Workers")
        print("  This may take a minute...")

        # Download secrets from Doppler
        result = subprocess.run(
            f"doppler secrets download --config {env} --format json",
            shell=True,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print("\n❌ Failed to download Doppler secrets")
            sys.exit(1)

        secrets = json.loads(result.stdout)

        # Inject each secret to Cloudflare Workers
        for key, value in secrets.items():
            # Skip non-secret env vars (like NODE_ENV, ENVIRONMENT)
            if key in ["NODE_ENV", "ENVIRONMENT", "CI"]:
                continue

            cmd = f'echo "{value}" | npx wrangler secret put {key} --config {wrangler_config}'
            subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        print(f"  ✓ Injected {len(secrets)} secrets")
    else:
        print("\n[DRY RUN] → Would inject Doppler secrets to Cloudflare Workers")

    # Step 6: Run smoke tests
    if not args.skip_smoke_tests:
        success = run_command(
            f"doppler run --config {env} -- npm run test:e2e:smoke",
            "Running smoke tests",
            args.dry_run
        )
        if not success:
            print("\n⚠️  Smoke tests failed. Rolling back deployment...")

            if not args.dry_run:
                subprocess.run(
                    f"npx wrangler rollback --config {wrangler_config}",
                    shell=True
                )

            print("\n❌ Deployment rolled back due to smoke test failure")
            sys.exit(1)
    else:
        print("\n⚠️  Skipping smoke tests (--skip-smoke-tests)")

    # Success!
    print(f"\n{'=' * 70}")
    print(f"  ✅ Deployment to {env.upper()} successful!")
    print(f"{'=' * 70}")

    if env == "production":
        print(f"\n🌐 Production URL: https://app.greyhaven.studio")
    elif env == "staging":
        print(f"\n🌐 Staging URL: https://staging.greyhaven.studio")
    else:
        print(f"\n🌐 Dev URL: https://dev.greyhaven.studio")

    print("\nNext steps:")
    print("  • Monitor logs: npx wrangler tail")
    print("  • Check Sentry for errors")
    print("  • Verify Axiom logs")


if __name__ == "__main__":
    main()
