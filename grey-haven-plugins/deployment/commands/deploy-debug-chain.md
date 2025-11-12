---
allowed-tools: Task, TodoWrite, Read, Write, MultiEdit, Bash, WebSearch
description: Deploy to Cloudflare Workers/Pages and debug issues with agent chain
argument-hint: [project name or directory to deploy]
---

Deploy and debug Cloudflare Workers/Pages: $ARGUMENTS

<ultrathink>
Deploy, monitor, debug, fix. Cloudflare's edge needs special attention. Chain deployment with debugging agents for production-ready code.
</ultrathink>

<megaexpertise type="cloudflare-deployment-orchestrator">
The assistant should deploy to Cloudflare, monitor build logs, debug issues, and chain appropriate agents for fixes.
</megaexpertise>

<context>
Deploying project: $ARGUMENTS
Target: Cloudflare Workers/Pages
Will chain debugging and optimization agents as needed
</context>

<requirements>
- Deploy to Cloudflare Workers/Pages
- Monitor build and deployment logs
- Debug deployment failures
- Optimize for edge runtime
- Set up monitoring and analytics
</requirements>

<actions>
1. **Project Detection and Setup**:
   ```bash
   # Detect project type
   if [ -f "wrangler.toml" ]; then
     PROJECT_TYPE="worker"
   elif [ -f "package.json" ] && grep -q '"@cloudflare/next-on-pages"' package.json; then
     PROJECT_TYPE="nextjs-pages"
   elif [ -d "src" ] && [ -f "package.json" ]; then
     PROJECT_TYPE="pages"
   else
     PROJECT_TYPE="unknown"
   fi
   
   echo "Detected project type: $PROJECT_TYPE"
   ```

2. **List and Analyze Existing Deployments**:
   ```javascript
   // List all Workers
   const workers = await mcp__cloudflare_workers_builds__workers_list();
   
   // Find our worker
   const targetWorker = workers.find(w => 
     w.name.includes("$ARGUMENTS") || 
     w.script_name.includes("$ARGUMENTS")
   );
   
   if (targetWorker) {
     // Get worker details
     const workerDetails = await mcp__cloudflare_workers_builds__workers_get_worker({
       scriptName: targetWorker.script_name
     });
     
     // Get worker code for analysis
     const workerCode = await mcp__cloudflare_workers_builds__workers_get_worker_code({
       scriptName: targetWorker.script_name
     });
     
     // Set as active for subsequent calls
     await mcp__cloudflare_workers_builds__workers_builds_set_active_worker({
       workerId: targetWorker.id
     });
   }
   ```

3. **Check Recent Builds**:
   ```javascript
   // List recent builds
   const builds = await mcp__cloudflare_workers_builds__workers_builds_list_builds({
       workerId: targetWorker.id,
     page: 1,
     perPage: 10
   });
   
   // Analyze failed builds
   const failedBuilds = builds.filter(b => b.status === 'failed');
   
   for (const build of failedBuilds.slice(0, 3)) {
     // Get build details
     const buildDetails = await mcp__cloudflare_workers_builds__workers_builds_get_build({
       buildUUID: build.uuid
     });
     
     // Get build logs
     const buildLogs = await mcp__cloudflare_workers_builds__workers_builds_get_build_logs({
       buildUUID: build.uuid
     });
     
     console.log(`Failed build ${build.uuid}:`, buildLogs);
   }
   ```

4. **Search Cloudflare Documentation**:
   ```javascript
   // Search for relevant documentation based on errors
   if (failedBuilds.length > 0) {
     const errorKeywords = extractErrorKeywords(buildLogs);
     
     for (const keyword of errorKeywords) {
       const docs = await mcp__cloudflare_docs__search_cloudflare_documentation({
         query: keyword
       });
       
       // Store relevant documentation
       relevantDocs.push(docs);
     }
   }
   
   // Get migration guide if needed
   if (PROJECT_TYPE === "pages") {
     const migrationGuide = await mcp__cloudflare_docs__migrate_pages_to_workers_guide();
   }
   ```

5. **Deploy with Wrangler**:
   ```bash
   # Install dependencies if needed
   if ! command -v wrangler &> /dev/null; then
     npm install -g wrangler
   fi
   
   # Build project
   if [ "$PROJECT_TYPE" = "nextjs-pages" ]; then
     npx @cloudflare/next-on-pages
   else
     npm run build
   fi
   
   # Deploy based on project type
   if [ "$PROJECT_TYPE" = "worker" ]; then
     wrangler deploy --name "$ARGUMENTS"
   elif [ "$PROJECT_TYPE" = "pages" ]; then
     wrangler pages deploy ./dist --project-name "$ARGUMENTS"
   fi
   ```

6. **Monitor Deployment**:
   ```javascript
   // Wait for deployment to complete
   await sleep(5000);
   
   // Get latest build
   const latestBuilds = await mcp__cloudflare_workers_builds__workers_builds_list_builds({
     workerId: targetWorker.id,
     page: 1,
     perPage: 1
   });
   
   const latestBuild = latestBuilds[0];
   
   // Get build logs
   const logs = await mcp__cloudflare_workers_builds__workers_builds_get_build_logs({
     buildUUID: latestBuild.uuid
   });
   ```

7. **Chain to Debug Agent if Failed**:
   if (latestBuild.status === 'failed') {
     - Parse error from logs
     - Invoke code-quality-analyzer agent:
       ```
       Task: "Analyze Cloudflare Worker deployment failure:
             
             Error logs:
             ${logs}
             
             Worker code:
             ${workerCode}
             
             Identify issues with:
             1. Edge runtime compatibility
             2. Module imports
             3. Environment variables
             4. Build configuration"
       ```

8. **Optimize for Edge Runtime**:
   - Invoke performance-optimizer agent:
     ```
     Task: "Optimize code for Cloudflare Workers edge runtime:
           
           Current code:
           ${workerCode}
           
           Optimize for:
           1. Bundle size (1MB limit for free tier)
           2. CPU time limits (10ms free, 50ms paid)
           3. Memory usage
           4. Cold start performance
           
           Specific optimizations:
           - Remove unnecessary dependencies
           - Use Cloudflare native APIs
           - Implement caching strategies"
     ```

9. **Generate Worker Tests**:
   - Invoke test-generator agent:
     ```
     Task: "Generate tests for Cloudflare Worker:
           
           Worker code:
           ${workerCode}
           
           Generate:
           1. Unit tests using Miniflare
           2. Integration tests for API endpoints
           3. Edge case handling
           4. Error response tests"
     ```

10. **Setup Monitoring and Analytics**:
    ```javascript
    // Create monitoring worker
    const monitoringCode = `
    export default {
      async fetch(request, env, ctx) {
        const url = new URL(request.url);
        
        // Log request
        console.log({
          method: request.method,
          url: url.pathname,
          headers: Object.fromEntries(request.headers),
          cf: request.cf,
          timestamp: new Date().toISOString()
        });
        
        // Forward to origin worker
        const response = await fetch(request);
        
        // Log response
        console.log({
          status: response.status,
          headers: Object.fromEntries(response.headers)
        });
        
        // Add analytics headers
        response.headers.set('X-Worker-Version', '${version}');
        response.headers.set('X-Edge-Location', request.cf.colo);
        
        return response;
      }
    };`;
    
    // Deploy monitoring wrapper
    await deployMonitoringWorker(monitoringCode);
    ```

11. **Configure Routes and Bindings**:
    ```toml
    # wrangler.toml configuration
    name = "$ARGUMENTS"
    main = "src/index.js"
    compatibility_date = "2024-01-01"
    
    [env.production]
    vars = { ENVIRONMENT = "production" }
    routes = [
      { pattern = "example.com/*", zone_name = "example.com" }
    ]
    
    [[kv_namespaces]]
    binding = "CACHE"
    id = "xxxxx"
    
    [[r2_buckets]]
    binding = "ASSETS"
    bucket_name = "assets"
    
    [[d1_databases]]
    binding = "DB"
    database_name = "prod-db"
    database_id = "xxxxx"
    ```

12. **Generate Deployment Report**:
    ```markdown
    # Cloudflare Deployment Report: $ARGUMENTS
    
    ## Deployment Status
    - Build ID: ${latestBuild.uuid}
    - Status: ${latestBuild.status}
    - Duration: ${latestBuild.duration}ms
    - Timestamp: ${latestBuild.created_at}
    
    ## Build Configuration
    - Worker Name: ${targetWorker.script_name}
    - Environment: ${targetWorker.environment}
    - Routes: ${targetWorker.routes.join(', ')}
    
    ## Performance Metrics
    - Bundle Size: ${bundleSize} KB
    - Cold Start: ${coldStart}ms
    - Average Response: ${avgResponse}ms
    
    ## Optimizations Applied
    ${optimizations.map(o => `- ${o.description}: ${o.impact}`).join('\n')}
    
    ## Error Summary
    ${errors.length > 0 ? errors.map(e => `- ${e.message}`).join('\n') : 'No errors'}
    
    ## Test Coverage
    - Unit Tests: ${unitTests.passed}/${unitTests.total}
    - Integration Tests: ${integrationTests.passed}/${integrationTests.total}
    
    ## Monitoring Setup
    - Analytics: [OK] Enabled
    - Error Tracking: [OK] Configured
    - Performance Monitoring: [OK] Active
    
    ## Documentation Referenced
    ${relevantDocs.map(d => `- [${d.title}](${d.url})`).join('\n')}
    
    ## Next Steps
    1. Monitor error rates in production
    2. Set up alerting for failures
    3. Configure auto-scaling if needed
    4. Implement cache warming
    ```

13. **Post-Deployment Verification**:
    ```bash
    # Test deployed worker
    WORKER_URL="https://$ARGUMENTS.workers.dev"
    
    # Health check
    curl -I "$WORKER_URL/health"
    
    # Test main endpoints
    curl "$WORKER_URL/api/test"
    
    # Check response headers
    curl -I "$WORKER_URL" | grep -E "cf-ray|cf-cache-status"
    ```
</actions>

The assistant should treat Cloudflare deployment as a critical production step, using build analysis and documentation search to resolve issues, while chaining specialized agents for optimization and testing.