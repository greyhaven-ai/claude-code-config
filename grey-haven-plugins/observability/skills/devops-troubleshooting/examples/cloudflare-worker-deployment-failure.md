# Cloudflare Worker Deployment Failure Investigation

Complete troubleshooting workflow for "Script exceeds size limit" deployment failure, resolved through bundle optimization and code splitting.

## Overview

**Incident**: Worker deployment failing with size limit error
**Impact**: Production deployment blocked for 2 hours
**Root Cause**: Bundle size grew from 1.2MB to 5.2MB after adding dependencies
**Resolution**: Bundle optimization (code splitting, tree shaking) reduced size to 1.8MB
**Status**: Resolved

## Incident Timeline

| Time | Event | Action |
|------|-------|--------|
| 14:00 | Deployment initiated via CI/CD | `wrangler deploy` triggered |
| 14:02 | Deployment failed | Error: "Script exceeds 1MB size limit" |
| 14:05 | Investigation started | Check recent code changes |
| 14:15 | Root cause identified | New dependencies increased bundle size |
| 14:30 | Fix implemented | Bundle optimization applied |
| 14:45 | Fix deployed | Successful deployment to production |
| 16:00 | Monitoring complete | Confirmed stable deployment |

---

## Symptoms and Detection

### Initial Error

**Deployment Command**:
```bash
$ wrangler deploy
✘ [ERROR] Script exceeds the size limit (5.2MB > 1MB after compression)
```

**CI/CD Pipeline Failure**:
```yaml
# GitHub Actions output
Step: Deploy to Cloudflare Workers
  ✓ Build completed (5.2MB bundle)
  ✗ Deployment failed: Script size exceeds limit
  Error: Workers Free plan limit is 1MB compressed
```

**Impact**:
- Production deployment blocked
- New features stuck in staging
- Team unable to deploy hotfixes

---

## Diagnosis

### Step 1: Check Bundle Size

**Before Investigation**:
```bash
# Build the worker locally
npm run build

# Check output size
ls -lh dist/
-rw-r--r--  1 user  staff   5.2M Dec  5 14:10 worker.js
```

**Analyze Bundle Composition**:
```bash
# Use webpack-bundle-analyzer
npm install --save-dev webpack-bundle-analyzer

# Add to webpack.config.js
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;

module.exports = {
  plugins: [
    new BundleAnalyzerPlugin()
  ]
};

# Build and open analyzer
npm run build
# Opens http://127.0.0.1:8888 with visual bundle breakdown
```

**Bundle Analyzer Findings**:
```
Total Size: 5.2MB

Breakdown:
- @anthropic-ai/sdk: 2.1MB (40%)
- aws-sdk: 1.8MB (35%)
- lodash: 800KB (15%)
- moment: 300KB (6%)
- application code: 200KB (4%)
```

**Red Flags**:
1. Full `aws-sdk` imported (only needed S3)
2. Entire `lodash` library (only using 3 functions)
3. `moment` included (native Date API would suffice)
4. Large AI SDK (only using text generation)

---

### Step 2: Identify Recent Changes

**Git Diff**:
```bash
# Check what changed in last deploy
git diff HEAD~1 HEAD -- src/

# Key changes:
+ import { Anthropic } from '@anthropic-ai/sdk';
+ import AWS from 'aws-sdk';
+ import _ from 'lodash';
+ import moment from 'moment';
```

**PR Analysis**:
```
PR #234: Add AI content generation feature
- Added @anthropic-ai/sdk (full SDK)
- Added AWS S3 integration (full aws-sdk)
- Used lodash for data manipulation
- Used moment for date formatting

Result: Bundle size increased by 4MB
```

---

### Step 3: Cloudflare Worker Size Limits

**Plan Limits**:
```
Workers Free: 1MB compressed
Workers Paid: 10MB compressed

Current plan: Workers Free
Current size: 5.2MB (over limit)

Options:
1. Upgrade to Workers Paid ($5/month)
2. Reduce bundle size to <1MB
3. Split into multiple workers
```

**Decision**: Reduce bundle size (no budget for upgrade)

---

## Resolution

### Fix 1: Tree Shaking with Named Imports

**Before** (imports entire libraries):
```typescript
// ❌ BAD: Imports full library
import _ from 'lodash';
import moment from 'moment';
import AWS from 'aws-sdk';

// Usage:
const unique = _.uniq(array);
const date = moment().format('YYYY-MM-DD');
const s3 = new AWS.S3();
```

**After** (imports only needed functions):
```typescript
// ✅ GOOD: Named imports enable tree shaking
import { uniq, map, filter } from 'lodash-es';
import { S3Client, PutObjectCommand } from '@aws-sdk/client-s3';

// ✅ BETTER: Native alternatives
const unique = [...new Set(array)];
const date = new Date().toISOString().split('T')[0];

// S3 client (v3 - modular)
const s3 = new S3Client({ region: 'us-east-1' });
```

**Size Reduction**:
```
Before:
- lodash: 800KB → lodash-es tree-shaken: 50KB (94% reduction)
- moment: 300KB → native Date: 0KB (100% reduction)
- aws-sdk: 1.8MB → @aws-sdk/client-s3: 200KB (89% reduction)
```

---

### Fix 2: External Dependencies (Don't Bundle Large SDKs)

**Before**:
```typescript
// worker.ts - bundled @anthropic-ai/sdk (2.1MB)
import { Anthropic } from '@anthropic-ai/sdk';

const client = new Anthropic({
  apiKey: env.ANTHROPIC_API_KEY
});
```

**After** (use fetch directly):
```typescript
// worker.ts - use native fetch (0KB)
async function callAnthropic(prompt: string, env: Env) {
  const response = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': env.ANTHROPIC_API_KEY,
      'anthropic-version': '2023-06-01'
    },
    body: JSON.stringify({
      model: 'claude-3-sonnet-20240229',
      max_tokens: 1024,
      messages: [
        { role: 'user', content: prompt }
      ]
    })
  });

  return response.json();
}
```

**Size Reduction**:
```
Before: @anthropic-ai/sdk: 2.1MB
After: Native fetch: 0KB
Savings: 2.1MB (100% reduction)
```

---

### Fix 3: Code Splitting (Async Imports)

**Before** (everything bundled):
```typescript
// worker.ts
import { expensiveFunction } from './expensive-module';

export default {
  async fetch(request: Request, env: Env) {
    // Even if not used, expensive-module is in bundle
    if (request.url.includes('/special')) {
      return expensiveFunction(request);
    }
    return new Response('OK');
  }
};
```

**After** (lazy load):
```typescript
// worker.ts
export default {
  async fetch(request: Request, env: Env) {
    if (request.url.includes('/special')) {
      // Only load when needed (separate chunk)
      const { expensiveFunction } = await import('./expensive-module');
      return expensiveFunction(request);
    }
    return new Response('OK');
  }
};
```

**Size Reduction**:
```
Main bundle: 1.8MB → 500KB (72% reduction)
expensive-module chunk: Loaded on-demand (lazy)
```

---

### Fix 4: Webpack Configuration Optimization

**Updated webpack.config.js**:
```javascript
const webpack = require('webpack');
const path = require('path');

module.exports = {
  entry: './src/worker.ts',
  target: 'webworker',
  mode: 'production',
  optimization: {
    minimize: true,
    usedExports: true,  // Tree shaking
    sideEffects: false,
  },
  resolve: {
    extensions: ['.ts', '.js'],
    alias: {
      // Replace heavy libraries with lighter alternatives
      'moment': 'date-fns',
      'lodash': 'lodash-es'
    }
  },
  module: {
    rules: [
      {
        test: /\.ts$/,
        use: {
          loader: 'ts-loader',
          options: {
            transpileOnly: true,
            compilerOptions: {
              module: 'esnext',  // Enable tree shaking
              moduleResolution: 'node'
            }
          }
        },
        exclude: /node_modules/
      }
    ]
  },
  plugins: [
    new webpack.DefinePlugin({
      'process.env.NODE_ENV': JSON.stringify('production')
    })
  ],
  output: {
    filename: 'worker.js',
    path: path.resolve(__dirname, 'dist'),
    libraryTarget: 'commonjs2'
  }
};
```

---

## Results

### Bundle Size Comparison

| Category | Before | After | Reduction |
|----------|--------|-------|-----------|
| **@anthropic-ai/sdk** | 2.1MB | 0KB (fetch) | -100% |
| **aws-sdk** | 1.8MB | 200KB (v3) | -89% |
| **lodash** | 800KB | 50KB (tree-shaken) | -94% |
| **moment** | 300KB | 0KB (native Date) | -100% |
| **Application code** | 200KB | 200KB | 0% |
| **TOTAL** | **5.2MB** | **450KB** | **-91%** |

**Compressed Size**:
- Before: 5.2MB → 1.8MB compressed (over 1MB limit)
- After: 450KB → 180KB compressed (under 1MB limit)

---

### Deployment Verification

**Successful Deployment**:
```bash
$ wrangler deploy
✔ Building...
✔ Validating...
Bundle size: 450KB (180KB compressed)
✔ Uploading...
✔ Deployed to production

Production URL: https://api.greyhaven.io
Worker ID: worker-abc123
```

**Load Testing**:
```bash
# Before optimization (would fail deployment)
# Bundle: 5.2MB, deploy: FAIL

# After optimization
$ ab -n 1000 -c 10 https://api.greyhaven.io/
Requests per second: 1250 [#/sec]
Time per request: 8ms [mean]
Successful requests: 1000 (100%)
Bundle size: 450KB ✓
```

---

## Prevention Measures

### 1. CI/CD Bundle Size Check

```yaml
# .github/workflows/deploy.yml - Add size validation
steps:
  - run: npm ci && npm run build
  - name: Check bundle size
    run: |
      SIZE_MB=$(stat -f%z dist/worker.js | awk '{print $1/1048576}')
      if (( $(echo "$SIZE_MB > 1.0" | bc -l) )); then
        echo "❌ Bundle exceeds 1MB"; exit 1
      fi
  - run: npx wrangler deploy
```

### 2. Pre-commit Hook

```bash
# .git/hooks/pre-commit
SIZE_MB=$(stat -f%z dist/worker.js | awk '{print $1/1048576}')
[ "$SIZE_MB" -lt "1.0" ] || { echo "❌ Bundle >1MB"; exit 1; }
```

### 3. PR Template

```markdown
## Bundle Impact
- [ ] Bundle size <800KB
- [ ] Tree shaking verified
Size: [Before → After]
```

### 4. Automated Analysis

```json
{
  "scripts": {
    "analyze": "webpack --profile --json > stats.json && webpack-bundle-analyzer stats.json"
  }
}
```

---

## Lessons Learned

### What Went Well

✅ Identified root cause quickly (bundle analyzer)
✅ Multiple optimization strategies applied
✅ Achieved 91% bundle size reduction
✅ Added automated checks to prevent recurrence

### What Could Be Improved

❌ No bundle size monitoring before incident
❌ Dependencies added without size consideration
❌ No pre-commit checks for bundle size

### Key Takeaways

1. **Always check bundle size** when adding dependencies
2. **Use native APIs** instead of libraries when possible
3. **Tree shaking** requires named imports (not default)
4. **Code splitting** for rarely-used features
5. **External API calls** are lighter than bundling SDKs

---

## Related Documentation

- **PlanetScale Issues**: [planetscale-connection-issues.md](planetscale-connection-issues.md)
- **Network Debugging**: [distributed-system-debugging.md](distributed-system-debugging.md)
- **Performance**: [performance-degradation-analysis.md](performance-degradation-analysis.md)
- **Runbooks**: [../reference/troubleshooting-runbooks.md](../reference/troubleshooting-runbooks.md)

---

Return to [examples index](INDEX.md)
