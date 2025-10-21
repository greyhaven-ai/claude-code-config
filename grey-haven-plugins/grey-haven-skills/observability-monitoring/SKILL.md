---
name: grey-haven-observability
description: Implement observability and monitoring for Grey Haven applications - structured logging with Axiom, error tracking with Sentry, Cloudflare Workers analytics, OpenTelemetry tracing, health checks, alerts, and dashboards. Use when setting up monitoring.
---
# Grey Haven Observability and Monitoring
Implement **observability and monitoring** for Grey Haven Studio applications using Axiom (logging), Sentry (errors), Cloudflare Analytics, and OpenTelemetry (tracing).
## Observability Stack
### Grey Haven Monitoring Architecture
- **Structured Logging**: Axiom for searchable, queryable logs
- **Error Tracking**: Sentry for frontend and backend errors
- **Metrics**: Cloudflare Workers Analytics for request/performance metrics
- **Tracing**: OpenTelemetry for distributed tracing (optional)
- **Uptime**: Cloudflare Health Checks for endpoint availability
- **Alerts**: Axiom monitors + Sentry alerts for critical issues
## Structured Logging with Axiom
### Axiom Setup (TanStack Start)
```typescript
// app/utils/logger.ts
import { Axiom } from "@axiomhq/js";
// Doppler provides AXIOM_TOKEN
const axiom = new Axiom({
 token: process.env.AXIOM_TOKEN!,
 orgId: process.env.AXIOM_ORG_ID,
});
// Dataset names by environment
const DATASET = process.env.ENVIRONMENT === "production"
 ? "grey-haven-prod"
 : "grey-haven-dev";
export interface LogEvent {
 level: "debug" | "info" | "warn" | "error";
 message: string;
 context?: Record<string, unknown>;
 userId?: string;
 tenantId?: string;
 requestId?: string;
 duration?: number;
}
export async function log(event: LogEvent) {
 const timestamp = new Date().toISOString();
 await axiom.ingest(DATASET, [
 {
 _time: timestamp,
 level: event.level,
 message: event.message,
 environment: process.env.ENVIRONMENT,
 service: "tanstack-start",
 user_id: event.userId,
 tenant_id: event.tenantId,
 request_id: event.requestId,
 duration_ms: event.duration,
 ...event.context,
 },
 ]);
 // Flush logs (important for serverless)
 await axiom.flush();
}
// Convenience methods
export const logger = {
 debug: (message: string, context?: Record<string, unknown>) =>
 log({ level: "debug", message, context }),
 info: (message: string, context?: Record<string, unknown>) =>
 log({ level: "info", message, context }),
 warn: (message: string, context?: Record<string, unknown>) =>
 log({ level: "warn", message, context }),
 error: (message: string, context?: Record<string, unknown>) =>
 log({ level: "error", message, context }),
};
```
### Axiom Setup (FastAPI)
```python
# app/utils/logger.py
import os
import httpx
from datetime import datetime
from typing import Any, Optional
# Doppler provides AXIOM_TOKEN
AXIOM_TOKEN = os.getenv("AXIOM_TOKEN")
AXIOM_ORG_ID = os.getenv("AXIOM_ORG_ID")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DATASET = "grey-haven-prod" if ENVIRONMENT == "production" else "grey-haven-dev"
async def log_event(
 level: str,
 message: str,
 context: Optional[dict[str, Any]] = None,
 user_id: Optional[str] = None,
 tenant_id: Optional[str] = None,
 request_id: Optional[str] = None,
 duration_ms: Optional[float] = None,
):
 """Send structured log event to Axiom."""
 event = {
 "_time": datetime.utcnow().isoformat(),
 "level": level,
 "message": message,
 "environment": ENVIRONMENT,
 "service": "fastapi",
 "user_id": user_id,
 "tenant_id": tenant_id,
 "request_id": request_id,
 "duration_ms": duration_ms,
 **(context or {}),
 }
 async with httpx.AsyncClient() as client:
 await client.post(
 f"https://api.axiom.co/v1/datasets/{DATASET}/ingest",
 headers={
 "Authorization": f"Bearer {AXIOM_TOKEN}",
 "Content-Type": "application/json",
 },
 json=[event],
 )
class Logger:
 """Structured logger for FastAPI."""
 @staticmethod
 async def debug(message: str, **context):
 await log_event("debug", message, context)
 @staticmethod
 async def info(message: str, **context):
 await log_event("info", message, context)
 @staticmethod
 async def warn(message: str, **context):
 await log_event("warn", message, context)
 @staticmethod
 async def error(message: str, **context):
 await log_event("error", message, context)
logger = Logger()
```
### Log API Requests (Middleware)
```typescript
// app/middleware/logging.ts (TanStack Start)
import { logger } from "~/utils/logger";
import { v4 as uuidv4 } from "uuid";
export async function loggingMiddleware(request: Request, next: () => Promise<Response>) {
 const requestId = uuidv4();
 const startTime = Date.now();
 try {
 // Execute request
 const response = await next();
 const duration = Date.now() - startTime;
 // Log successful request
 await logger.info("API request completed", {
 request_id: requestId,
 method: request.method,
 url: request.url,
 status: response.status,
 duration_ms: duration,
 });
 return response;
 } catch (error) {
 const duration = Date.now() - startTime;
 // Log failed request
 await logger.error("API request failed", {
 request_id: requestId,
 method: request.method,
 url: request.url,
 error: error.message,
 duration_ms: duration,
 });
 throw error;
 }
}
```
```python
# app/middleware/logging.py (FastAPI)
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import time
import uuid
from app.utils.logger import logger
class LoggingMiddleware(BaseHTTPMiddleware):
 """Log all API requests."""
 async def dispatch(self, request: Request, call_next):
 request_id = str(uuid.uuid4())
 start_time = time.time()
 try:
# Execute request
 response = await call_next(request)
 duration_ms = (time.time() - start_time) * 1000
# Log successful request
 await logger.info(
 "API request completed",
 request_id=request_id,
 method=request.method,
 url=str(request.url),
 status=response.status_code,
 duration_ms=duration_ms,
 )
 return response
 except Exception as e:
 duration_ms = (time.time() - start_time) * 1000
# Log failed request
 await logger.error(
 "API request failed",
 request_id=request_id,
 method=request.method,
 url=str(request.url),
 error=str(e),
 duration_ms=duration_ms,
 )
 raise
# Register middleware in main.py
from app.middleware.logging import LoggingMiddleware
app.add_middleware(LoggingMiddleware)
```
### Query Logs in Axiom
```apl
// Axiom Processing Language (APL) queries
// Get all errors in last 24 hours
['grey-haven-prod']
| where level == "error"
| where _time > ago(24h)
| project _time, message, user_id, tenant_id, request_id
// Average request duration by endpoint
['grey-haven-prod']
| where level == "info"
| where message == "API request completed"
| summarize avg_duration = avg(duration_ms) by url
| order by avg_duration desc
// Error rate by tenant
['grey-haven-prod']
| where level == "error"
| where _time > ago(1h)
| summarize error_count = count() by tenant_id
| order by error_count desc
// Slow queries (> 1 second)
['grey-haven-prod']
| where duration_ms > 1000
| project _time, message, url, duration_ms
| order by duration_ms desc
```
## Error Tracking with Sentry
### Sentry Setup (TanStack Start)
```typescript
// app/utils/sentry.ts
import * as Sentry from "@sentry/browser";
import { BrowserTracing } from "@sentry/tracing";
// Doppler provides SENTRY_DSN
Sentry.init({
 dsn: process.env.SENTRY_DSN,
 environment: process.env.ENVIRONMENT,
 tracesSampleRate: 1.0, // 100% of transactions
 integrations: [
 new BrowserTracing(),
 new Sentry.Replay({
 // Session replay for debugging
 maskAllText: true,
 blockAllMedia: true,
 }),
 ],
 replaysSessionSampleRate: 0.1, // 10% of sessions
 replaysOnErrorSampleRate: 1.0, // 100% of sessions with errors
});
// Set user context (after login)
export function setUserContext(user: { id: string; email: string; tenantId: string }) {
 Sentry.setUser({
 id: user.id,
 email: user.email,
 tenantId: user.tenantId,
 });
}
// Clear user context (after logout)
export function clearUserContext() {
 Sentry.setUser(null);
}
// Capture exception with context
export function captureException(error: Error, context?: Record<string, unknown>) {
 Sentry.captureException(error, {
 extra: context,
 });
}
```
### Sentry Setup (FastAPI)
```python
# app/utils/sentry.py
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
import os
# Doppler provides SENTRY_DSN
SENTRY_DSN = os.getenv("SENTRY_DSN")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
sentry_sdk.init(
 dsn=SENTRY_DSN,
 environment=ENVIRONMENT,
 traces_sample_rate=1.0, # 100% of transactions
 integrations=[
 FastApiIntegration(),
 SqlalchemyIntegration(),
 ],
)
def set_user_context(user_id: str, email: str, tenant_id: str):
 """Set user context for Sentry."""
 sentry_sdk.set_user({
 "id": user_id,
 "email": email,
 "tenant_id": tenant_id,
 })
def clear_user_context():
 """Clear user context from Sentry."""
 sentry_sdk.set_user(None)
def capture_exception(error: Exception, context: dict | None = None):
 """Capture exception with additional context."""
 with sentry_sdk.push_scope() as scope:
 if context:
 for key, value in context.items():
 scope.set_extra(key, value)
 sentry_sdk.capture_exception(error)
```
### Error Boundaries (React)
```typescript
// app/components/ErrorBoundary.tsx
import { Component, ReactNode } from "react";
import * as Sentry from "@sentry/browser";
interface Props {
 children: ReactNode;
 fallback?: ReactNode;
}
interface State {
 hasError: boolean;
}
export class ErrorBoundary extends Component<Props, State> {
 constructor(props: Props) {
 super(props);
 this.state = { hasError: false };
 }
 static getDerivedStateFromError(error: Error) {
 return { hasError: true };
 }
 componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
 // Log error to Sentry
 Sentry.captureException(error, {
 extra: {
 componentStack: errorInfo.componentStack,
 },
 });
 }
 render() {
 if (this.state.hasError) {
 return (
 this.props.fallback || (
 <div className="error-boundary">
 <h2>Something went wrong</h2>
 <button onClick={() => this.setState({ hasError: false })}>
 Try again
 </button>
 </div>
 )
 );
 }
 return this.props.children;
 }
}
```
### Catch Errors in Server Functions
```typescript
// app/routes/api/users.ts
import { createServerFn } from "@tanstack/start";
import { captureException } from "~/utils/sentry";
import { logger } from "~/utils/logger";
export const createUser = createServerFn({ method: "POST" })
 .validator(createUserSchema)
 .handler(async ({ data, context }) => {
 try {
 const user = await db.insert(usersTable).values(data).returning();
 return user;
 } catch (error) {
 // Log to Axiom
 await logger.error("Failed to create user", {
 error: error.message,
 data,
 });
 // Send to Sentry
 captureException(error, {
 operation: "createUser",
 data,
 });
 throw error;
 }
 });
```
## Cloudflare Workers Analytics
### Cloudflare Dashboard Metrics
- **Requests**: Total requests per second, requests by status code
- **CPU Time**: Worker execution time (milliseconds)
- **Errors**: Error rate (5xx responses)
- **Subrequests**: External API calls from Workers
- **KV Operations**: KV namespace read/write operations
### Custom Analytics (Analytics Engine)
```typescript
// app/utils/analytics.ts
export async function trackEvent(
 env: Env,
 event: string,
 properties: Record<string, string | number>
) {
 // Write to Analytics Engine (binding in wrangler.toml)
 await env.ANALYTICS.writeDataPoint({
 blobs: [event],
 doubles: [Date.now()],
 indexes: Object.keys(properties).map((key) => String(properties[key])),
 });
}
// Usage in server function
export const loginUser = createServerFn({ method: "POST" }).handler(
 async ({ data, context }) => {
 const user = await authenticateUser(data);
 // Track login event
 await trackEvent(context.env, "user_login", {
 user_id: user.id,
 tenant_id: user.tenantId,
 method: "email",
 });
 return user;
 }
);
```
### Query Analytics (GraphQL API)
```graphql
query GetLoginStats {
 viewer {
 accounts(filter: { accountTag: $accountId }) {
 workersAnalyticsEngineDataset(dataset: "grey_haven_events") {
 query(
 filter: {
 blob1: "user_login"
 datetime_gt: "2025-01-01T00:00:00Z"
 }
 ) {
 count
 dimensions {
 blob1
 index1 # user_id
 index2 # tenant_id
 }
 }
 }
 }
 }
}
```
## OpenTelemetry Tracing (Optional)
### Setup OpenTelemetry (FastAPI)
```python
# app/utils/tracing.py
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
import os
# Doppler provides OTEL_EXPORTER_OTLP_ENDPOINT
OTLP_ENDPOINT = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
# Initialize tracer
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)
# Configure exporter (Axiom, Honeycomb, etc.)
span_processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=OTLP_ENDPOINT))
trace.get_tracer_provider().add_span_processor(span_processor)
# Instrument FastAPI
FastAPIInstrumentor.instrument_app(app)
# Create custom spans
async def process_payment(order_id: str):
 with tracer.start_as_current_span("process_payment") as span:
 span.set_attribute("order_id", order_id)
# Nested span for database query
 with tracer.start_as_current_span("fetch_order"):
 order = await db.get(Order, order_id)
# Nested span for external API call
 with tracer.start_as_current_span("charge_payment"):
 result = await stripe.charge(order.amount)
 return result
```
## Health Checks and Uptime
### Health Check Endpoint
```typescript
// app/routes/api/health.ts (TanStack Start)
import { createServerFn } from "@tanstack/start";
import { db } from "~/utils/db.server";
export const GET = createServerFn({ method: "GET" }).handler(async ({ context }) => {
 const startTime = Date.now();
 // Check database connection
 let dbHealthy = false;
 try {
 await db.execute("SELECT 1");
 dbHealthy = true;
 } catch (error) {
 console.error("Database health check failed:", error);
 }
 // Check Redis connection
 let redisHealthy = false;
 try {
 await context.env.REDIS.ping();
 redisHealthy = true;
 } catch (error) {
 console.error("Redis health check failed:", error);
 }
 const duration = Date.now() - startTime;
 const healthy = dbHealthy && redisHealthy;
 return new Response(
 JSON.stringify({
 status: healthy ? "healthy" : "unhealthy",
 checks: {
 database: dbHealthy ? "ok" : "failed",
 redis: redisHealthy ? "ok" : "failed",
 },
 duration_ms: duration,
 timestamp: new Date().toISOString(),
 }),
 {
 status: healthy ? 200 : 503,
 headers: { "Content-Type": "application/json" },
 }
 );
});
```
```python
# app/api/routes/health.py (FastAPI)
from fastapi import APIRouter, status
from app.core.database import engine
from app.utils.redis import redis
from datetime import datetime
import time
router = APIRouter()
@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
 """Health check endpoint for monitoring."""
 start_time = time.time()
# Check database
 db_healthy = False
 try:
 async with engine.connect() as conn:
 await conn.execute("SELECT 1")
 db_healthy = True
 except Exception as e:
 print(f"Database health check failed: {e}")
# Check Redis
 redis_healthy = False
 try:
 await redis.ping()
 redis_healthy = True
 except Exception as e:
 print(f"Redis health check failed: {e}")
 duration_ms = (time.time() - start_time) * 1000
 healthy = db_healthy and redis_healthy
 return {
 "status": "healthy" if healthy else "unhealthy",
 "checks": {
 "database": "ok" if db_healthy else "failed",
 "redis": "ok" if redis_healthy else "failed",
 },
 "duration_ms": duration_ms,
 "timestamp": datetime.utcnow().isoformat(),
 }
```
### Cloudflare Health Checks
Configure in Cloudflare Dashboard:
1. Navigate to **Traffic** → **Health Checks**
2. Create health check:
 - **Name**: Grey Haven API Health
 - **URL**: `https://api.greyhaven.studio/api/v1/health`
 - **Interval**: 60 seconds
 - **Retries**: 2
 - **Expected Status**: 200
 - **Notification**: Email on failure
## Alerts and Notifications
### Axiom Monitors
Create monitors in Axiom dashboard:
**High Error Rate Alert**:
```apl
['grey-haven-prod']
| where level == "error"
| where _time > ago(5m)
| summarize error_count = count()
| where error_count > 10
```
- **Threshold**: > 10 errors in 5 minutes
- **Notification**: Email + Slack
**Slow Request Alert**:
```apl
['grey-haven-prod']
| where duration_ms > 5000
| where _time > ago(10m)
| summarize slow_requests = count()
| where slow_requests > 5
```
- **Threshold**: > 5 slow requests (> 5s) in 10 minutes
- **Notification**: Email
### Sentry Alerts
Configure in Sentry dashboard:
1. **Project Settings** → **Alerts**
2. Create alert rule:
 - **Condition**: Error count > 10 in 1 hour
 - **Action**: Email + Slack notification
 - **Filter**: Only production environment
### Slack Notifications (Webhook)
```typescript
// app/utils/slack.ts
export async function sendSlackAlert(message: string, severity: "info" | "warning" | "error") {
 // Doppler provides SLACK_WEBHOOK_URL
 const webhookUrl = process.env.SLACK_WEBHOOK_URL;
 const color = {
 info: "#36a64f",
 warning: "#ff9900",
 error: "#ff0000",
 }[severity];
 await fetch(webhookUrl, {
 method: "POST",
 headers: { "Content-Type": "application/json" },
 body: JSON.stringify({
 attachments: [
 {
 color,
 title: "Grey Haven Alert",
 text: message,
 ts: Math.floor(Date.now() / 1000),
 },
 ],
 }),
 });
}
// Usage in error handler
try {
 await criticalOperation();
} catch (error) {
 await sendSlackAlert(
 ` Critical operation failed: ${error.message}`,
 "error"
 );
 throw error;
}
```
## Performance Dashboards
### Axiom Dashboard Queries
**Request Volume by Endpoint**:
```apl
['grey-haven-prod']
| where message == "API request completed"
| where _time > ago(24h)
| summarize requests = count() by url
| order by requests desc
| limit 10
```
**P95 Response Time**:
```apl
['grey-haven-prod']
| where message == "API request completed"
| where _time > ago(1h)
| summarize p95_duration = percentile(duration_ms, 95) by bin(_time, 5m)
```
**Error Rate Over Time**:
```apl
['grey-haven-prod']
| where _time > ago(24h)
| summarize
 total = count(),
 errors = countif(level == "error")
 by bin(_time, 1h)
| extend error_rate = (errors * 100.0) / total
| project _time, error_rate
```
## Doppler Configuration
### Required Secrets for Observability
```bash
# Axiom (structured logging)
AXIOM_TOKEN=xaat-...
AXIOM_ORG_ID=grey-haven-...
# Sentry (error tracking)
SENTRY_DSN=https://...@sentry.io/...
# Slack (alerts)
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
# OpenTelemetry (optional tracing)
OTEL_EXPORTER_OTLP_ENDPOINT=https://api.axiom.co/v1/traces
# Cloudflare Analytics (auto-configured)
CLOUDFLARE_ACCOUNT_ID=...
```
## When to Apply This Skill
Use this observability skill when:
- Setting up logging for new applications or services
- Implementing error tracking with Sentry
- Creating health check endpoints for monitoring
- Configuring alerts for high error rates or slow requests
- Debugging production issues (query logs in Axiom)
- Analyzing performance bottlenecks (query duration metrics)
- Setting up dashboards for stakeholder visibility
- Implementing distributed tracing with OpenTelemetry
- Configuring Cloudflare Health Checks for uptime monitoring
- Integrating Slack notifications for critical alerts
## Template References
These observability patterns come from Grey Haven's actual templates:
- **Frontend**: `cvi-template` (Sentry + Axiom logging)
- **Backend**: `cvi-backend-template` (Sentry + Axiom + OpenTelemetry)
- **Cloudflare**: Workers Analytics + Health Checks
## Critical Reminders
1. **Structured logging** - Log JSON with consistent fields (level, message, context)
2. **Flush logs in serverless** - Call `axiom.flush()` before function returns
3. **Set user context** - Include user_id and tenant_id in logs and Sentry
4. **Log request duration** - Track duration_ms for performance analysis
5. **Query logs efficiently** - Use APL queries with time filters and aggregations
6. **Set up error boundaries** - Catch React errors and send to Sentry
7. **Health check dependencies** - Check database, Redis, external APIs
8. **Configure alerts** - Set thresholds for error rate, slow requests, downtime
9. **Use Doppler for secrets** - Store AXIOM_TOKEN, SENTRY_DSN in Doppler
10. **Monitor production only** - Separate datasets for dev/staging/production
