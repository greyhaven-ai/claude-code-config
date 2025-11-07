#!/bin/bash
# Cloudflare Worker API Scaffold Template
# Usage: ./cloudflare-worker-template.sh my-api

PROJECT_NAME="${1:-my-worker-api}"

echo "Scaffolding Cloudflare Worker: $PROJECT_NAME"

# Create directory structure
mkdir -p "$PROJECT_NAME"/{src/{routes,middleware,services,types,utils},tests,.github/workflows}

cd "$PROJECT_NAME" || exit

# package.json
cat > package.json << 'EOF'
{
  "name": "PROJECT_NAME",
  "scripts": {
    "dev": "wrangler dev",
    "deploy": "wrangler deploy",
    "test": "vitest"
  },
  "dependencies": {
    "hono": "^4.0.0"
  },
  "devDependencies": {
    "@cloudflare/workers-types": "^4.20240117.0",
    "typescript": "^5.3.3",
    "vitest": "^1.2.0",
    "wrangler": "^3.25.0"
  }
}
EOF

sed -i '' "s/PROJECT_NAME/$PROJECT_NAME/g" package.json

# wrangler.toml
cat > wrangler.toml << 'EOF'
name = "PROJECT_NAME"
main = "src/index.ts"
compatibility_date = "2024-01-15"

[[d1_databases]]
binding = "DB"
database_name = "PROJECT_NAME-db"
database_id = ""
EOF

sed -i '' "s/PROJECT_NAME/$PROJECT_NAME/g" wrangler.toml

# tsconfig.json
cat > tsconfig.json << 'EOF'
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ES2022",
    "lib": ["ES2022"],
    "moduleResolution": "bundler",
    "strict": true,
    "types": ["@cloudflare/workers-types"]
  }
}
EOF

# src/index.ts
cat > src/index.ts << 'EOF'
import { Hono } from 'hono';
import { cors } from 'hono/cors';

const app = new Hono();

app.use('*', cors());

app.get('/health', (c) => c.json({ status: 'healthy' }));

export default app;
EOF

# .gitignore
cat > .gitignore << 'EOF'
node_modules/
dist/
.wrangler/
.env
.DS_Store
EOF

# README.md
cat > README.md << 'EOF'
# PROJECT_NAME

Cloudflare Workers API

## Setup

\`\`\`bash
npm install
npm run dev
\`\`\`

## Deploy

\`\`\`bash
npm run deploy
\`\`\`
EOF

sed -i '' "s/PROJECT_NAME/$PROJECT_NAME/g" README.md

echo "✅ Scaffold complete! Run: cd $PROJECT_NAME && npm install && npm run dev"
