---
allowed-tools: Task, TodoWrite, Read, Write, MultiEdit, Bash
description: Develop E2E tests by recording user interactions in Chrome and generating test code
argument-hint: [URL or localhost:port to test]
---

Develop E2E tests using Chrome browser recording: $ARGUMENTS

<ultrathink>
Watch, learn, codify. Chrome MCP records real user flows with existing auth. Transform interactions into reliable E2E tests.
</ultrathink>

<megaexpertise type="e2e-test-generator">
The assistant should use Chrome MCP to record user interactions with preserved session state, then generate comprehensive E2E tests using appropriate testing frameworks.
</megaexpertise>

<context>
Creating E2E tests for: $ARGUMENTS
Recording real browser interactions
Generating tests with proper assertions
</context>

<requirements>
- Record user interaction flows
- Capture network requests for mocking
- Generate test code with assertions
- Handle authentication states
- Create visual regression tests
</requirements>

<actions>
1. **Initialize Test Recording Session**:
   ```javascript
   // Navigate to application
   await mcp__chrome__chrome_navigate({
     url: "$ARGUMENTS",
     viewport: { width: 1920, height: 1080 }
   });
   
   // Start recording interactions
   const recordedActions = [];
   const recordedNetwork = [];
   ```

2. **Inject Recording Script**:
   ```javascript
   await mcp__chrome__chrome_inject_script({
     type: "ISOLATED",
     jsScript: `
       // Track all user interactions
       const events = ['click', 'input', 'change', 'submit', 'keydown'];
       const recordedEvents = [];
       
       events.forEach(eventType => {
         document.addEventListener(eventType, (e) => {
           const selector = e.target.closest('[data-testid]')?.getAttribute('data-testid') ||
                          e.target.id ? '#' + e.target.id :
                          e.target.className ? '.' + e.target.className.split(' ')[0] :
                          e.target.tagName.toLowerCase();
           
           recordedEvents.push({
             type: eventType,
             selector: selector,
             value: e.target.value,
             key: e.key,
             timestamp: Date.now(),
             text: e.target.textContent,
             position: { x: e.clientX, y: e.clientY }
           });
           
           console.log('[RECORDED]', JSON.stringify(recordedEvents[recordedEvents.length - 1]));
         }, true);
       });
       
       // Track navigation
       const observer = new MutationObserver((mutations) => {
         console.log('[DOM_CHANGE]', {
           timestamp: Date.now(),
           mutations: mutations.length
         });
       });
       
       observer.observe(document.body, {
         childList: true,
         subtree: true
       });
     `
   });
   ```

3. **Start Network Recording**:
   ```javascript
   // Use debugger API for full request/response capture
   await mcp__chrome__chrome_network_debugger_start({});
   ```

4. **Guide User Through Test Flows**:
   ```javascript
   // Inject visual guide
   await mcp__chrome__chrome_inject_script({
     type: "MAIN",
     jsScript: `
       // Create test flow guide
       const guide = document.createElement('div');
       guide.style.cssText = 'position:fixed;top:10px;right:10px;background:#4CAF50;color:white;padding:10px;z-index:10000;border-radius:5px;';
       guide.innerHTML = '<h3>Recording E2E Test</h3><p>Please perform the following actions:</p><ol id="test-steps"></ol>';
       document.body.appendChild(guide);
       
       const steps = [
         'Login to the application',
         'Navigate to main feature',
         'Create a new item',
         'Edit the item',
         'Delete the item',
         'Logout'
       ];
       
       const stepsList = document.getElementById('test-steps');
       steps.forEach(step => {
         const li = document.createElement('li');
         li.textContent = step;
         stepsList.appendChild(li);
       });
     `
   });
   ```

5. **Capture Key Interactions**:
   ```javascript
   // Wait for user to perform actions
   console.log("Please perform the test flow in the browser...");
   
   // Monitor console for recorded events
   let recording = true;
   while (recording) {
     const consoleOutput = await mcp__chrome__chrome_console();
     
     // Extract recorded events
     const newEvents = consoleOutput
       .filter(log => log.message.includes('[RECORDED]'))
       .map(log => JSON.parse(log.message.replace('[RECORDED]', '').trim()));
     
     recordedActions.push(...newEvents);
     
     // Check for completion signal
     if (recordedActions.some(a => a.selector.includes('logout'))) {
       recording = false;
     }
     
     await sleep(1000);
   }
   ```

6. **Capture Visual States**:
   ```javascript
   // Take screenshots at key points
   const screenshots = [];
   
   for (const action of recordedActions) {
     if (action.type === 'click' || action.type === 'submit') {
       // Wait for any transitions
       await sleep(500);
       
       const screenshot = await mcp__chrome__chrome_screenshot({
         fullPage: false,
         storeBase64: true
       });
       
       screenshots.push({
         action: action,
         screenshot: screenshot,
         timestamp: Date.now()
       });
     }
   }
   ```

7. **Stop Network Recording**:
   ```javascript
   const networkData = await mcp__chrome__chrome_network_debugger_stop({});
   
   // Filter relevant API calls
   const apiCalls = networkData.filter(req => 
     req.url.includes('/api/') || 
     req.url.includes('graphql')
   );
   ```

8. **Chain to Test Generator Agent**:
   - Invoke test-generator agent:
     ```
     Task: "Generate E2E tests from recorded interactions:
           
           Recorded Actions:
           ${JSON.stringify(recordedActions, null, 2)}
           
           API Calls to Mock:
           ${JSON.stringify(apiCalls, null, 2)}
           
           Generate tests for:
           1. Playwright
           2. Cypress
           3. Testing Library
           
           Include:
           - Proper selectors (prefer data-testid)
           - Assertions for each step
           - Network mocking
           - Error handling"
     ```

9. **Generate Playwright Test**:
   ```typescript
   // Generated test file: e2e/recorded-flow.spec.ts
   import { test, expect } from '@playwright/test';
   
   test.describe('User Flow: $ARGUMENTS', () => {
     test.beforeEach(async ({ page }) => {
       // Navigate to application
       await page.goto('$ARGUMENTS');
       
       // Mock API responses
       ${apiCalls.map(call => `
       await page.route('${call.url}', async route => {
         await route.fulfill({
           status: ${call.status},
           body: JSON.stringify(${JSON.stringify(call.responseBody)})
         });
       });`).join('\n')}
     });
     
     test('Complete user flow', async ({ page }) => {
       ${recordedActions.map(action => {
         switch(action.type) {
           case 'click':
             return `
       // Click ${action.text || action.selector}
       await page.click('${action.selector}');
       await expect(page).toHaveURL(/.*/); // Update with expected URL`;
           
           case 'input':
             return `
       // Fill input ${action.selector}
       await page.fill('${action.selector}', '${action.value}');`;
           
           case 'submit':
             return `
       // Submit form
       await page.press('${action.selector}', 'Enter');
       await page.waitForLoadState('networkidle');`;
           
           default:
             return `// ${action.type} on ${action.selector}`;
         }
       }).join('\n')}
       
       // Visual regression test
       await expect(page).toHaveScreenshot('final-state.png');
     });
     
     test('Error handling', async ({ page }) => {
       // Test error scenarios
       await page.route('**/api/*', route => route.abort());
       
       await page.click('[data-testid="submit-button"]');
       await expect(page.locator('.error-message')).toBeVisible();
     });
   });
   ```

10. **Generate Cypress Test**:
    ```javascript
    // Generated test file: cypress/e2e/recorded-flow.cy.js
    describe('User Flow: $ARGUMENTS', () => {
      beforeEach(() => {
        // Mock API responses
        ${apiCalls.map(call => `
        cy.intercept('${call.method}', '${call.url}', {
          statusCode: ${call.status},
          body: ${JSON.stringify(call.responseBody)}
        }).as('${call.url.split('/').pop()}');`).join('\n')}
        
        cy.visit('$ARGUMENTS');
      });
      
      it('Complete user flow', () => {
        ${recordedActions.map(action => {
          switch(action.type) {
            case 'click':
              return `
        // Click ${action.text || action.selector}
        cy.get('${action.selector}').click();`;
            
            case 'input':
              return `
        // Fill input
        cy.get('${action.selector}').type('${action.value}');`;
            
            case 'submit':
              return `
        // Submit form
        cy.get('${action.selector}').submit();
        cy.wait('@apiCall');`;
            
            default:
              return `// ${action.type}`;
          }
        }).join('\n')}
        
        // Assertions
        cy.url().should('include', '/success');
        cy.get('[data-testid="success-message"]').should('be.visible');
      });
    });
    ```

11. **Generate Visual Regression Tests**:
    ```javascript
    // visual-regression.spec.js
    import { test, expect } from '@playwright/test';
    
    test('Visual regression tests', async ({ page }) => {
      const screenshots = ${JSON.stringify(screenshots.map(s => s.action))};
      
      for (const step of screenshots) {
        await page.goto('$ARGUMENTS');
        
        // Recreate state up to this point
        // ... recorded actions ...
        
        await expect(page).toHaveScreenshot(\`step-\${step.type}-\${step.selector}.png\`);
      }
    });
    ```

12. **Generate Test Data Fixtures**:
    ```javascript
    // fixtures/recorded-data.json
    {
      "apiMocks": ${JSON.stringify(apiCalls, null, 2)},
      "userActions": ${JSON.stringify(recordedActions, null, 2)},
      "testData": {
        "validUser": {
          "email": "test@example.com",
          "password": "TestPass123!"
        },
        "invalidUser": {
          "email": "invalid",
          "password": "wrong"
        }
      }
    }
    ```

13. **Generate Test Report**:
    ```markdown
    # E2E Test Generation Report
    
    ## Test Coverage
    - User flows recorded: ${recordedActions.length} actions
    - API calls mocked: ${apiCalls.length} endpoints
    - Screenshots captured: ${screenshots.length}
    
    ## Generated Tests
    - [OK] Playwright test suite
    - [OK] Cypress test suite
    - [OK] Visual regression tests
    - [OK] Test data fixtures
    
    ## Key Test Scenarios
    1. Happy path user flow
    2. Error handling
    3. Network failure scenarios
    4. Visual regression checks
    
    ## Selectors Used
    ${[...new Set(recordedActions.map(a => a.selector))].map(s => `- ${s}`).join('\n')}
    
    ## API Endpoints Mocked
    ${apiCalls.map(c => `- ${c.method} ${c.url}`).join('\n')}
    
    ## Next Steps
    1. Review and refine selectors (prefer data-testid)
    2. Add additional assertions
    3. Parameterize test data
    4. Set up CI/CD integration
    5. Configure visual regression baselines
    ```
</actions>

The assistant should leverage Chrome MCP's ability to work with real browser sessions and existing authentication to record authentic user flows, then transform them into comprehensive, maintainable E2E tests.