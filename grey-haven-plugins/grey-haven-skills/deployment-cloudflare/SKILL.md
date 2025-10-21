---
name: grey-haven-deployment-cloudflare
description: Deploy TanStack Start applications to Cloudflare Workers/Pages with GitHub Actions, Doppler, Wrangler, database migrations, and rollback procedures. Use when deploying Grey Haven applications.
---

# Grey Haven Cloudflare Deployment

Deploy TanStack Start applications to **Cloudflare Workers** and **Cloudflare Pages** using GitHub Actions, Doppler for secrets, and Wrangler CLI.

## Deployment Architecture

### TanStack Start on Cloudflare Workers
- **SSR**: Server-side rendering with TanStack Start server functions
- **Edge Runtime**: Global deployment on Cloudflare's edge network
- **Database**: PostgreSQL (Neon/Supabase) with connection pooling
- **Cache**: Cloudflare KV for session storage, R2 for file uploads
- **Secrets**: Managed via Doppler, injected in GitHub Actions

### Backend on Cloudflare Workers (Python)
- **FastAPI**: Deployed as Python Workers using `workers-python`
- **Database**: PostgreSQL with SQLModel and async drivers
- **Background Jobs**: Cloudflare Queues for async processing

## Wrangler Configuration

### `wrangler.toml` (TanStack Start)
```toml
name = "grey-haven-app"
main = "dist/server/index.js"
compatibility_date = "2025-01-15"
node_compat = true

[vars]
ENVIRONMENT = "production"
DATABASE_POOL_MIN = "2"
DATABASE_POOL_MAX = "10"

# KV namespace for session storage
[[kv_namespaces]]
binding = "SESSIONS"
id = "your-kv-namespace-id"
preview_id = "your-preview-kv-namespace-id"

# R2 bucket for file uploads
[[r2_buckets]]
binding = "UPLOADS"
bucket_name = "grey-haven-uploads"
preview_bucket_name = "grey-haven-uploads-preview"

# D1 database (optional - for edge data)
[[d1_databases]]
binding = "DB"
database_name = "grey-haven-db"
database_id = "your-d1-database-id"

# Analytics Engine (optional)
[[analytics_engine_datasets]]
binding = "ANALYTICS"

# Durable Objects (optional - for real-time features)
[[durable_objects.bindings]]
name = "COUNTER"
class_name = "Counter"
script_name = "grey-haven-app"

# Routes
routes = [
  { pattern = "app.greyhaven.studio", zone_name = "greyhaven.studio" }
]

# Custom domains
[custom_domains]
enabled = true
custom_domain = "app.greyhaven.studio"
```

### Environment-Specific Configurations

**Development** (`wrangler.toml`):
```toml
name = "grey-haven-app-dev"
[vars]
ENVIRONMENT = "development"
```

**Staging** (`wrangler.staging.toml`):
```toml
name = "grey-haven-app-staging"
[vars]
ENVIRONMENT = "staging"
routes = [
  { pattern = "staging.greyhaven.studio", zone_name = "greyhaven.studio" }
]
```

**Production** (`wrangler.production.toml`):
```toml
name = "grey-haven-app"
[vars]
ENVIRONMENT = "production"
routes = [
  { pattern = "app.greyhaven.studio", zone_name = "greyhaven.studio" }
]
```

## Doppler Integration

### GitHub Actions Secrets
Store in GitHub repository secrets:
- `DOPPLER_TOKEN`: Doppler service token for CI/CD
- `CLOUDFLARE_API_TOKEN`: Wrangler deployment token

### Doppler Environments
- `dev`: Local development
- `test`: CI/CD testing
- `staging`: Staging deployment
- `production`: Production deployment

### Required Doppler Secrets (Production)
```bash
# Application
BETTER_AUTH_SECRET=<random-secret>
BETTER_AUTH_URL=https://app.greyhaven.studio
JWT_SECRET_KEY=<random-secret>

# Database (Neon/Supabase)
DATABASE_URL=postgresql://user:pass@host/db
DATABASE_URL_ADMIN=postgresql://admin:pass@host/db

# Redis (Upstash)
REDIS_URL=redis://user:pass@host:port

# Email (Resend)
RESEND_API_KEY=re_...

# OAuth Providers
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
GITHUB_CLIENT_ID=...
GITHUB_CLIENT_SECRET=...

# Cloudflare (for KV/R2)
CLOUDFLARE_ACCOUNT_ID=...
CLOUDFLARE_API_TOKEN=...

# Monitoring (optional)
SENTRY_DSN=https://...@sentry.io/...
AXIOM_TOKEN=xaat-...
```

## GitHub Actions Deployment

### `.github/workflows/deploy-production.yml`
```yaml
name: Deploy to Production

on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      deployments: write

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '22'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Install Doppler CLI
        uses: dopplerhq/cli-action@v3

      - name: Run tests
        env:
          DOPPLER_TOKEN: ${{ secrets.DOPPLER_TOKEN }}
        run: doppler run --config test -- npm run test

      - name: Build application
        env:
          DOPPLER_TOKEN: ${{ secrets.DOPPLER_TOKEN }}
        run: doppler run --config production -- npm run build

      - name: Run database migrations
        env:
          DOPPLER_TOKEN: ${{ secrets.DOPPLER_TOKEN }}
        run: |
          doppler run --config production -- npm run db:migrate
          doppler run --config production -- npm run db:seed:production

      - name: Deploy to Cloudflare Workers
        env:
          DOPPLER_TOKEN: ${{ secrets.DOPPLER_TOKEN }}
          CLOUDFLARE_API_TOKEN: ${{ secrets.CLOUDFLARE_API_TOKEN }}
        run: |
          # Inject Doppler secrets as Wrangler secrets
          doppler secrets download --config production --format json > secrets.json

          # Deploy with secrets
          npx wrangler deploy --config wrangler.production.toml

          # Set secrets in Cloudflare Workers
          cat secrets.json | jq -r 'to_entries | .[] | "\(.key)=\(.value)"' | while read -r line; do
            key=$(echo "$line" | cut -d= -f1)
            value=$(echo "$line" | cut -d= -f2-)
            echo "$value" | npx wrangler secret put "$key" --config wrangler.production.toml
          done

          # Clean up secrets file
          rm secrets.json

      - name: Run smoke tests
        env:
          DOPPLER_TOKEN: ${{ secrets.DOPPLER_TOKEN }}
        run: doppler run --config production -- npm run test:e2e:smoke

      - name: Notify deployment
        if: success()
        run: |
          echo "✅ Deployment successful to https://app.greyhaven.studio"

      - name: Rollback on failure
        if: failure()
        env:
          CLOUDFLARE_API_TOKEN: ${{ secrets.CLOUDFLARE_API_TOKEN }}
        run: |
          echo "❌ Deployment failed - rolling back"
          npx wrangler rollback --config wrangler.production.toml
```

### `.github/workflows/deploy-staging.yml`
```yaml
name: Deploy to Staging

on:
  push:
    branches: [develop]
  pull_request:
    types: [opened, synchronize]

jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      deployments: write
      pull-requests: write

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '22'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Install Doppler CLI
        uses: dopplerhq/cli-action@v3

      - name: Run tests
        env:
          DOPPLER_TOKEN: ${{ secrets.DOPPLER_TOKEN }}
        run: doppler run --config test -- npm run test

      - name: Build application
        env:
          DOPPLER_TOKEN: ${{ secrets.DOPPLER_TOKEN }}
        run: doppler run --config staging -- npm run build

      - name: Deploy to Cloudflare Workers (Staging)
        env:
          DOPPLER_TOKEN: ${{ secrets.DOPPLER_TOKEN }}
          CLOUDFLARE_API_TOKEN: ${{ secrets.CLOUDFLARE_API_TOKEN }}
        run: |
          doppler secrets download --config staging --format json > secrets.json
          npx wrangler deploy --config wrangler.staging.toml

          cat secrets.json | jq -r 'to_entries | .[] | "\(.key)=\(.value)"' | while read -r line; do
            key=$(echo "$line" | cut -d= -f1)
            value=$(echo "$line" | cut -d= -f2-)
            echo "$value" | npx wrangler secret put "$key" --name grey-haven-app-staging
          done

          rm secrets.json

      - name: Comment PR with preview URL
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: '✅ Preview deployed to https://staging.greyhaven.studio'
            })
```

## Database Migrations in Deployment

### Drizzle Migrations (TanStack Start)
```typescript
// scripts/migrate.ts
import { drizzle } from "drizzle-orm/node-postgres";
import { migrate } from "drizzle-orm/node-postgres/migrator";
import { Pool } from "pg";

// Doppler provides DATABASE_URL_ADMIN at runtime
const pool = new Pool({
  connectionString: process.env.DATABASE_URL_ADMIN,
});

const db = drizzle(pool);

async function main() {
  console.log("Running migrations...");
  await migrate(db, { migrationsFolder: "./drizzle/migrations" });
  console.log("Migrations complete!");
  await pool.end();
}

main().catch((err) => {
  console.error("Migration failed:", err);
  process.exit(1);
});
```

**package.json**:
```json
{
  "scripts": {
    "db:migrate": "tsx scripts/migrate.ts",
    "db:migrate:dev": "doppler run --config dev -- tsx scripts/migrate.ts",
    "db:migrate:staging": "doppler run --config staging -- tsx scripts/migrate.ts",
    "db:migrate:production": "doppler run --config production -- tsx scripts/migrate.ts"
  }
}
```

### Alembic Migrations (FastAPI)
```python
# alembic/env.py
import os
from alembic import context
from sqlmodel import create_engine

# Doppler provides DATABASE_URL_ADMIN
DATABASE_URL = os.getenv("DATABASE_URL_ADMIN")

def run_migrations():
    engine = create_engine(DATABASE_URL, echo=True)
    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=metadata)
        with context.begin_transaction():
            context.run_migrations()

run_migrations()
```

**Run in CI**:
```bash
doppler run --config production -- alembic upgrade head
```

## Rollback Procedures

### Wrangler Rollback
```bash
# List recent deployments
npx wrangler deployments list --config wrangler.production.toml

# Rollback to previous deployment
npx wrangler rollback --config wrangler.production.toml

# Rollback to specific deployment ID
npx wrangler rollback --deployment-id abc123 --config wrangler.production.toml
```

### Database Rollback (Drizzle)
```bash
# Rollback last migration
doppler run --config production -- drizzle-kit migrate:rollback

# Rollback to specific migration
doppler run --config production -- drizzle-kit migrate:rollback --to 20250115_initial
```

### Database Rollback (Alembic)
```bash
# Rollback one migration
doppler run --config production -- alembic downgrade -1

# Rollback to specific revision
doppler run --config production -- alembic downgrade abc123
```

### Emergency Rollback Playbook
1. **Identify issue**: Check Cloudflare Workers logs, Sentry, Axiom
2. **Rollback Workers deployment**: `npx wrangler rollback`
3. **Rollback database** (if migration caused issue): `alembic downgrade -1`
4. **Verify rollback**: Run smoke tests against production URL
5. **Notify team**: Update Linear issue with rollback status
6. **Root cause analysis**: Create postmortem in Linear

## Cloudflare Workers Configuration

### Environment Variables
Set via Wrangler CLI (injected from Doppler in CI):

```bash
# Local development (uses Doppler)
doppler run --config dev -- npm run dev

# Set secret in Cloudflare Workers (production)
echo "$SECRET_VALUE" | npx wrangler secret put SECRET_NAME --config wrangler.production.toml
```

### KV Namespace Setup
```bash
# Create KV namespace for sessions
npx wrangler kv:namespace create "SESSIONS" --config wrangler.production.toml
npx wrangler kv:namespace create "SESSIONS" --preview --config wrangler.production.toml

# List KV namespaces
npx wrangler kv:namespace list
```

### R2 Bucket Setup
```bash
# Create R2 bucket for file uploads
npx wrangler r2 bucket create grey-haven-uploads
npx wrangler r2 bucket create grey-haven-uploads-preview

# List R2 buckets
npx wrangler r2 bucket list
```

## Custom Domain Setup

### Cloudflare DNS Configuration
1. Add DNS records in Cloudflare dashboard:
   - `app.greyhaven.studio` → CNAME to Workers route
   - `staging.greyhaven.studio` → CNAME to Workers route

2. Enable **Proxy** (orange cloud) for DDoS protection and caching

3. Configure SSL/TLS:
   - Mode: **Full (strict)**
   - Edge Certificates: **Universal SSL** enabled

### Wrangler Custom Domain
```bash
# Add custom domain to Workers
npx wrangler deploy --config wrangler.production.toml

# Verify custom domain
curl -I https://app.greyhaven.studio
```

## Monitoring and Alerting

### Cloudflare Workers Analytics
- **Dashboard**: https://dash.cloudflare.com
- **Metrics**: Requests/second, CPU time, errors, success rate
- **Logs**: Real-time logs in Cloudflare dashboard

### Wrangler Tail (Real-time Logs)
```bash
# Stream production logs
npx wrangler tail --config wrangler.production.toml

# Filter by status code
npx wrangler tail --status error --config wrangler.production.toml

# Filter by IP
npx wrangler tail --ip 1.2.3.4 --config wrangler.production.toml
```

### Sentry Integration (Error Tracking)
```typescript
// app/utils/sentry.ts
import * as Sentry from "@sentry/browser";

// Doppler provides SENTRY_DSN
Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.ENVIRONMENT,
  tracesSampleRate: 1.0,
});
```

### Axiom Integration (Structured Logging)
```typescript
// app/utils/logger.ts
import { Axiom } from "@axiomhq/js";

// Doppler provides AXIOM_TOKEN
const axiom = new Axiom({
  token: process.env.AXIOM_TOKEN!,
});

export async function logEvent(event: string, data: Record<string, unknown>) {
  await axiom.ingest("grey-haven-events", [
    {
      event,
      timestamp: new Date().toISOString(),
      environment: process.env.ENVIRONMENT,
      ...data,
    },
  ]);
}
```

## Performance Optimization

### Cloudflare Cache API
```typescript
// app/routes/api/users.ts
export const GET = async ({ request }: { request: Request }) => {
  const cache = caches.default;
  const cacheKey = new Request(request.url, request);

  // Check cache
  let response = await cache.match(cacheKey);
  if (response) {
    return response;
  }

  // Fetch from database
  const users = await db.select().from(usersTable);
  response = new Response(JSON.stringify(users), {
    headers: {
      "Content-Type": "application/json",
      "Cache-Control": "public, max-age=300", // 5 minutes
    },
  });

  // Store in cache
  await cache.put(cacheKey, response.clone());
  return response;
};
```

### Connection Pooling (PostgreSQL)
```typescript
// app/utils/db.server.ts
import { Pool } from "pg";
import { drizzle } from "drizzle-orm/node-postgres";

// Doppler provides DATABASE_URL with connection pooling
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 10, // Match wrangler.toml DATABASE_POOL_MAX
  min: 2,  // Match wrangler.toml DATABASE_POOL_MIN
  idleTimeoutMillis: 30000,
});

export const db = drizzle(pool);
```

## Security Best Practices

### Rate Limiting (Cloudflare Workers)
```typescript
// middleware/rate-limit.ts
import { Ratelimit } from "@upstash/ratelimit";
import { Redis } from "@upstash/redis/cloudflare";

// Doppler provides REDIS_URL
const redis = Redis.fromEnv();
const ratelimit = new Ratelimit({
  redis,
  limiter: Ratelimit.slidingWindow(10, "10 s"), // 10 requests per 10 seconds
});

export async function rateLimit(identifier: string) {
  const { success, limit, remaining, reset } = await ratelimit.limit(identifier);
  if (!success) {
    throw new Error("Rate limit exceeded");
  }
}
```

### CORS Configuration
```typescript
// app/entry.server.tsx
export function handleFetch(request: Request) {
  const response = await getLoadContext(request);

  // Set CORS headers
  response.headers.set("Access-Control-Allow-Origin", "https://app.greyhaven.studio");
  response.headers.set("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE");
  response.headers.set("Access-Control-Allow-Headers", "Content-Type, Authorization");

  return response;
}
```

## Local Development

### Wrangler Dev (Local Workers)
```bash
# Run Workers locally with Doppler
doppler run --config dev -- npx wrangler dev

# Run with specific port
doppler run --config dev -- npx wrangler dev --port 8787

# Run with remote mode (uses production KV/R2)
doppler run --config dev -- npx wrangler dev --remote
```

### Local Database Setup
```bash
# Start PostgreSQL locally
docker run -d \
  --name postgres \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  postgres:16

# Run migrations
doppler run --config dev -- npm run db:migrate

# Seed database
doppler run --config dev -- npm run db:seed
```

## CI/CD Pipeline Summary

### Development Workflow
1. **Local development**: `doppler run --config dev -- npm run dev`
2. **Run tests**: `doppler run --config test -- npm run test`
3. **Commit changes**: Follow Grey Haven commit format (100 char header, lowercase)
4. **Push to feature branch**: `git push origin GREY-123-feat-description`
5. **Open PR**: Links to Linear issue GREY-123

### Staging Deployment (Automatic)
1. **PR merged to `develop`**: Triggers `deploy-staging.yml`
2. **Run tests**: `doppler run --config test -- npm run test`
3. **Build**: `doppler run --config staging -- npm run build`
4. **Deploy to staging**: `npx wrangler deploy --config wrangler.staging.toml`
5. **Inject secrets**: From Doppler staging environment
6. **Preview URL**: https://staging.greyhaven.studio

### Production Deployment (Automatic)
1. **PR merged to `main`**: Triggers `deploy-production.yml`
2. **Run tests**: `doppler run --config test -- npm run test`
3. **Build**: `doppler run --config production -- npm run build`
4. **Database migrations**: `doppler run --config production -- npm run db:migrate`
5. **Deploy to production**: `npx wrangler deploy --config wrangler.production.toml`
6. **Inject secrets**: From Doppler production environment
7. **Smoke tests**: `doppler run --config production -- npm run test:e2e:smoke`
8. **Rollback on failure**: `npx wrangler rollback`
9. **Production URL**: https://app.greyhaven.studio

## Troubleshooting

### Deployment Fails with "Secret not found"
**Cause**: Doppler secret not set in production environment

**Fix**:
```bash
# Check Doppler secrets
doppler secrets --config production

# Add missing secret
doppler secrets set SECRET_NAME --config production
```

### Wrangler Deployment Timeout
**Cause**: Large bundle size or slow build

**Fix**:
```bash
# Analyze bundle size
npm run build -- --analyze

# Optimize imports (use tree-shaking)
# Remove unused dependencies
```

### Database Connection Errors
**Cause**: Invalid DATABASE_URL or connection pool exhausted

**Fix**:
```bash
# Verify DATABASE_URL in Doppler
doppler secrets get DATABASE_URL --config production

# Increase connection pool in wrangler.toml
[vars]
DATABASE_POOL_MAX = "20"
```

### KV/R2 Binding Errors
**Cause**: KV namespace or R2 bucket not configured in wrangler.toml

**Fix**:
```bash
# List KV namespaces
npx wrangler kv:namespace list

# Update wrangler.toml with correct IDs
[[kv_namespaces]]
binding = "SESSIONS"
id = "your-actual-kv-id"
```

## When to Apply This Skill

Use this deployment skill when:
- Deploying TanStack Start applications to Cloudflare Workers
- Setting up CI/CD pipelines with GitHub Actions
- Configuring Doppler for multi-environment secrets
- Running database migrations in production
- Rolling back failed deployments
- Setting up custom domains on Cloudflare
- Configuring KV namespaces or R2 buckets
- Troubleshooting deployment failures
- Optimizing Workers performance
- Setting up monitoring and alerting

## Template References

These deployment patterns come from Grey Haven's actual templates:
- **Frontend**: `cvi-template` (TanStack Start + Cloudflare Workers)
- **Backend**: `cvi-backend-template` (FastAPI + Python Workers)
- **GitHub Actions**: `.github/workflows/deploy-*.yml`
- **Wrangler**: `wrangler.*.toml` configuration files

## Critical Reminders

1. **Doppler for ALL secrets** - Never commit secrets to git
2. **Database migrations BEFORE deployment** - Prevents runtime errors
3. **Smoke tests AFTER deployment** - Catch issues early
4. **Rollback on failure** - Automated rollback in GitHub Actions
5. **Connection pooling** - Match wrangler.toml pool settings
6. **Custom domains** - Use Cloudflare Proxy for DDoS protection
7. **Rate limiting** - Protect API endpoints with Upstash Redis
8. **CORS configuration** - Whitelist production domain only
9. **Environment-specific configs** - Separate wrangler.*.toml files
10. **Monitor deployments** - Use Wrangler tail, Sentry, Axiom
