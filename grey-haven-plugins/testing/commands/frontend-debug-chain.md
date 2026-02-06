---
allowed-tools: Task, TodoWrite, Read, Write, MultiEdit, Bash, Grep, Glob, Teammate, SendMessage, TaskCreate, TaskUpdate, TaskList, TaskGet
description: Debug frontend issues using Chrome MCP with real browser context and agent analysis
argument-hint: [URL or localhost:port to debug]
---
Debug frontend application using Chrome browser: $ARGUMENTS
<ultrathink>
Real browser, real debugging. Chrome MCP preserves login states, catches runtime errors, monitors network. Chain with React/TanStack specialists for comprehensive debugging.
</ultrathink>
<megaexpertise type="frontend-debugging-orchestrator">
The assistant should use Chrome MCP for live debugging with preserved browser state, then chain specialized agents to fix issues found.
</megaexpertise>
<context>
Debugging frontend at: $ARGUMENTS
Using Chrome with existing session/cookies
Will chain appropriate frontend framework agents
</context>
<requirements>
- Console error monitoring
- Network request debugging
- Performance profiling
- Interactive element testing
- React/TanStack specific debugging
- Fix implementation with TDD
</requirements>
<actions>
1. **Navigate to Application**:
 ```javascript
 // Open the application in Chrome
 await mcp__chrome__chrome_navigate({
 url: "$ARGUMENTS",
 viewport: { width: 1920, height: 1080 }
 });
 // Wait for initial load
 await sleep(2000);
 ```
2. **Start Monitoring Tools**:
 ```javascript
 // Start network debugger for API calls
 await mcp__chrome__chrome_network_debugger_start({});
 // Clear console to start fresh
 await mcp__chrome__chrome_console();
 ```
3. **Inject Debug Helper Scripts**:
 ```javascript
 // Inject React DevTools helper
 await mcp__chrome__chrome_inject_script({
 type: "MAIN",
 jsScript: `
 // Expose React internals
 if (window.React) {
 window.__REACT_VERSION__ = React.version;
 }
 // Find React Fiber
 function findReactFiber(element) {
 const key = Object.keys(element).find(key => key.startsWith('__reactFiber'));
 return element[key];
 }
 // Log component renders
 if (window.__REACT_DEVTOOLS_GLOBAL_HOOK__) {
 const hook = window.__REACT_DEVTOOLS_GLOBAL_HOOK__;
 const original = hook.onCommitFiberRoot;
 hook.onCommitFiberRoot = function(...args) {
 console.log('[RENDER]', args);
 return original?.apply(this, args);
 };
 }
 // Monitor TanStack Query
 if (window.__TANSTACK_QUERY_DEVTOOLS__) {
 console.log('[TanStack Query] Devtools available');
 }
 // Error boundary helper
 window.addEventListener('error', (e) => {
 console.error('[RUNTIME ERROR]', {
 message: e.message,
 source: e.filename,
 line: e.lineno,
 column: e.colno,
 stack: e.error?.stack
 });
 });
 // Promise rejection handler
 window.addEventListener('unhandledrejection', (e) => {
 console.error('[PROMISE REJECTION]', e.reason);
 });
 `
 });
 ```
4. **Performance Profiling**:
 ```javascript
 // Inject performance monitoring
 await mcp__chrome__chrome_inject_script({
 type: "MAIN",
 jsScript: `
 // Measure React render performance
 const observer = new PerformanceObserver((list) => {
 for (const entry of list.getEntries()) {
 if (entry.entryType === 'measure') {
 console.log('[PERFORMANCE]', {
 name: entry.name,
 duration: entry.duration,
 startTime: entry.startTime
 });
 }
 }
 });
 observer.observe({ entryTypes: ['measure'] });
 // Monitor long tasks
 const taskObserver = new PerformanceObserver((list) => {
 for (const entry of list.getEntries()) {
 console.warn('[LONG TASK]', {
 duration: entry.duration,
 startTime: entry.startTime
 });
 }
 });
 taskObserver.observe({ entryTypes: ['longtask'] });
 `
 });
 ```
5. **Interactive Element Testing**:
 ```javascript
 // Get all interactive elements
 const elements = await mcp__chrome__chrome_get_interactive_elements();
 // Group by type
 const buttons = elements.filter(e => e.type === 'button');
 const inputs = elements.filter(e => e.type === 'input');
 const links = elements.filter(e => e.type === 'link');
 // Test form validation
 for (const input of inputs) {
 if (input.selector.includes('email')) {
 await mcp__chrome__chrome_fill_or_select({
 selector: input.selector,
 value: "invalid-email"
 });
 // Trigger validation
 await mcp__chrome__chrome_keyboard({
 key: "Tab"
 });
 }
 }
 // Test button clicks
 for (const button of buttons.slice(0, 3)) { // Test first 3 buttons
 await mcp__chrome__chrome_click_element({
 selector: button.selector
 });
 // Check for errors after click
 const consoleErrors = await mcp__chrome__chrome_console();
 }
 ```
6. **Network Analysis**:
 ```javascript
 // Let the app run for a bit
 await sleep(5000);
 // Stop and analyze network
 const networkData = await mcp__chrome__chrome_network_debugger_stop({});
 // Find failed requests
 const failedRequests = networkData.filter(req =>
 req.status >= 400 || req.status === 0
 );
 // Find slow requests
 const slowRequests = networkData.filter(req =>
 req.responseTime > 1000
 );
 // Analyze API patterns
 const apiCalls = networkData.filter(req =>
 req.url.includes('/api/') ||
 req.url.includes('graphql')
 );
 ```
7. **Console Error Collection**:
 ```javascript
 // Get all console output
 const consoleOutput = await mcp__chrome__chrome_console();
 // Categorize errors
 const errors = consoleOutput.filter(log => log.type === 'error');
 const warnings = consoleOutput.filter(log => log.type === 'warning');
 const performance = consoleOutput.filter(log =>
 log.message.includes('[PERFORMANCE]')
 );
 ```
8. **Screenshot Problem Areas**:
 ```javascript
 // Capture full page
 await mcp__chrome__chrome_screenshot({
 fullPage: true,
 storeBase64: true
 });
 // Capture specific error elements
 for (const error of errors) {
 if (error.selector) {
 await mcp__chrome__chrome_screenshot({
 selector: error.selector,
 storeBase64: true
 });
 }
 }
 ```
9. **Mode Detection**:
   - Check if `Teammate` tool is available
   - If available: use **Team Mode** for the agent chain phase (parallel analysis + fixing)
   - Otherwise: use **Subagent Mode** (existing sequential agent chain)
   - Announce: "Using **Team Mode** — parallel agent analysis and fixing." or "Using **Subagent Mode** — sequential agent chain."

10. **Team Mode — Parallel Agent Chain** (replaces sequential steps 9-11 when in Team Mode):

    a. **Create Team**:
       ```
       Teammate(spawnTeam) with name: frontend-debug-{url-slug}
       ```

    b. **Create Task Board**:
       ```
       Layer 0 (parallel analysis + fixing):
         - react-fixer: Analyze and fix React/TanStack issues
         - quality-rev: Review code quality for frontend patterns
         - tdd-fixer: Implement fixes with TDD methodology

       Layer 1 (synthesis — blocked by all Layer 0):
         - Orchestrator merges findings and generates report
       ```

    c. **Spawn Teammates**:
       | Teammate | Agent Type | File Ownership | Plan Required |
       |----------|-----------|----------------|---------------|
       | react-fixer | `testing:react-tanstack-tester` | Component files (`src/components/**`, `src/pages/**`) | No |
       | quality-rev | `core:code-quality-analyzer` | None (read-only analysis) | No |
       | tdd-fixer | `core:tdd-typescript-implementer` | Test files (`tests/**`, `*.test.*`, `*.spec.*`) | No |

       Spawn prompt template:
       ```
       You are {role} on the frontend-debug-{url-slug} team.

       FILE OWNERSHIP: You may ONLY create/modify files matching: {patterns}
       Do NOT touch files outside your ownership boundary.

       Browser debugging data collected:
       - Console errors: {error summary}
       - Failed network requests: {request summary}
       - Performance issues: {performance summary}

       Report findings via SendMessage to the orchestrator when complete.
       Your current task: see TaskList for your assigned tasks.
       ```

    d. **Monitor & Synthesize**:
       - Track task completion via `TaskList`
       - Collect findings from all teammates
       - Merge into unified debug report

    e. **Cleanup**:
       - Send `shutdown_request` to all teammates
       - Call `Teammate(cleanup)`

11. **Subagent Mode — Sequential Agent Chain** (fallback when Team Mode is unavailable):

    a. **Chain to React/TanStack Testing Agent**:
       - Invoke react-tanstack-tester agent:
       ```
       Task: "Analyze and fix React/TanStack issues found:
       Console Errors:
       ${JSON.stringify(errors, null, 2)}
       Failed API Calls:
       ${JSON.stringify(failedRequests, null, 2)}
       Performance Issues:
       ${JSON.stringify(performance, null, 2)}
       Create fixes and tests for:
       1. Component errors
       2. API integration issues
       3. Performance bottlenecks"
       ```

    b. **Chain to Code Quality Analyzer**:
       - Based on errors found, invoke code-quality-analyzer:
       ```
       Task: "Review frontend code for issues causing:
       ${errors.map(e => e.message).join('\n')}
       Focus on:
       - Event handler errors
       - State management issues
       - Async operation handling
       - Memory leaks"
       ```

    c. **Fix Implementation with TDD**:
       - Invoke tdd-typescript agent:
       ```
       Task: "Implement fixes for frontend issues:
       Issues to fix:
       1. ${errors[0]?.message}
       2. ${failedRequests[0]?.url} - ${failedRequests[0]?.status}
       Write tests first, then fixes for:
       - Error boundaries for runtime errors
       - Retry logic for failed requests
       - Performance optimizations"
       ```

12. **Generate Debug Report**:
 ```markdown
# Frontend Debug Report: $ARGUMENTS

## Orchestration
- Mode: Team Mode / Subagent Mode
- Teammates spawned: X (if team mode)
- File ownership enforced: react-fixer → components, tdd-fixer → tests, quality-rev → read-only

## [CRITICAL] Critical Issues (${errors.length})
 ${errors.map(e => `
### ${e.message}
 - Location: ${e.source}:${e.line}:${e.column}
 - Stack: \`\`\`
 ${e.stack}
 \`\`\`
 - Fix Applied: [Yes/No]
 `).join('\n')}
## WARNING: Warnings (${warnings.length})
 ${warnings.slice(0, 5).map(w => `- ${w.message}`).join('\n')}
## Network Issues
### Failed Requests (${failedRequests.length})
 ${failedRequests.map(r => `
 - ${r.method} ${r.url}
 Status: ${r.status}
 Response: ${r.responseBody?.substring(0, 200)}
 `).join('\n')}
### Slow Requests (${slowRequests.length})
 ${slowRequests.map(r => `
 - ${r.url}: ${r.responseTime}ms
 `).join('\n')}
## Performance Metrics
 - Long Tasks: ${performance.filter(p => p.message.includes('LONG TASK')).length}
 - Slow Renders: ${performance.filter(p => p.duration > 16).length}
 - Average Render Time: ${avgRenderTime}ms
## Interactive Elements Tested
 - Buttons: ${buttons.length} found, ${buttonsTested} tested
 - Forms: ${inputs.length} inputs found
 - Links: ${links.length} found
 - Validation Errors: ${validationErrors.length}
## Visual Documentation
 - Screenshots captured: ${screenshots.length}
 - Error states documented: [Yes/No]
## SUCCESS: Fixes Applied
 1. [Fix description and test coverage]
 2. [Fix description and test coverage]
## Recommendations
 1. Add error boundaries to prevent crashes
 2. Implement retry logic for failed API calls
 3. Optimize render performance with memoization
 4. Add loading states for async operations
## Next Steps
 - [ ] Deploy fixes to staging
 - [ ] Run full test suite
 - [ ] Monitor error rates
 ```
13. **Verify Fixes**:
 ```javascript
 // Reload page with fixes
 await mcp__chrome__chrome_navigate({
 url: "$ARGUMENTS",
 viewport: { width: 1920, height: 1080 }
 });
 // Re-run checks
 await mcp__chrome__chrome_inject_script({
 type: "MAIN",
 jsScript: `
 console.log('[VERIFICATION] Checking fixes...');
 // Previous error checks
 `
 });
 // Verify no new errors
 const newConsole = await mcp__chrome__chrome_console();
 const newErrors = newConsole.filter(log => log.type === 'error');
 if (newErrors.length === 0) {
 console.log("SUCCESS: All fixes verified!");
 }
 ```
</actions>
The assistant should use Chrome MCP as a powerful frontend debugging tool that preserves real browser state and login sessions, then chain specialized React/TanStack agents to implement fixes with proper testing.