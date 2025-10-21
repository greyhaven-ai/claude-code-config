---
allowed-tools: Task, TodoWrite, Read, Write, MultiEdit, Bash
description: Create visual regression tests with Playwright and chain analysis agents
argument-hint: [URL or localhost:port to test]
---

Create visual regression tests with Playwright: $ARGUMENTS

<ultrathink>
Pixels tell stories. Playwright captures visual truth, agents analyze differences. Regression tests protect user experience.
</ultrathink>

<megaexpertise type="visual-testing-orchestrator">
The assistant should use Playwright MCP to create comprehensive visual regression tests, then chain agents to analyze results and generate reports.
</megaexpertise>

<context>
Creating visual tests for: $ARGUMENTS
Using Playwright for cross-browser testing
Chaining agents for result analysis
</context>

<requirements>
- Multi-browser visual testing
- Responsive design validation
- Component isolation testing
- Visual diff analysis
- Accessibility testing
- Performance metrics
</requirements>

<actions>
1. **Initialize Playwright Testing**:
   ```javascript
   // Check if Playwright is installed
   const isInstalled = await mcp__playwright__browser_install();
   
   // Navigate to application
   await mcp__playwright__browser_navigate({
     url: "$ARGUMENTS"
   });
   ```

2. **Capture Browser State**:
   ```javascript
   // Get current page snapshot for context
   const snapshot = await mcp__playwright__browser_snapshot();
   
   // Get console messages
   const consoleMessages = await mcp__playwright__browser_console_messages();
   
   // Get network requests
   const networkRequests = await mcp__playwright__browser_network_requests();
   ```

3. **Multi-Viewport Testing**:
   ```javascript
   const viewports = [
     { name: "Desktop HD", width: 1920, height: 1080 },
     { name: "Desktop", width: 1366, height: 768 },
     { name: "Tablet Landscape", width: 1024, height: 768 },
     { name: "Tablet Portrait", width: 768, height: 1024 },
     { name: "Mobile", width: 375, height: 667 },
     { name: "Mobile Small", width: 320, height: 568 }
   ];
   
   const screenshots = [];
   
   for (const viewport of viewports) {
     // Resize browser
     await mcp__playwright__browser_resize({
       width: viewport.width,
       height: viewport.height
     });
     
     // Wait for responsive adjustments
     await mcp__playwright__browser_wait_for({ time: 1 });
     
     // Capture screenshot
     await mcp__playwright__browser_take_screenshot({
       filename: `baseline-${viewport.name.replace(' ', '-')}.png`,
       fullPage: true
     });
     
     screenshots.push({
       viewport: viewport,
       filename: `baseline-${viewport.name.replace(' ', '-')}.png`
     });
   }
   ```

4. **Component Isolation Testing**:
   ```javascript
   // Find all major components
   const components = [
     { name: "header", selector: "header, [role='banner']" },
     { name: "navigation", selector: "nav, [role='navigation']" },
     { name: "main-content", selector: "main, [role='main']" },
     { name: "sidebar", selector: "aside, [role='complementary']" },
     { name: "footer", selector: "footer, [role='contentinfo']" },
     { name: "modals", selector: "[role='dialog']" },
     { name: "forms", selector: "form" }
   ];
   
   for (const component of components) {
     // Check if component exists
     const exists = await mcp__playwright__browser_evaluate({
       function: `(selector) => !!document.querySelector('${component.selector}')`,
       element: component.name
     });
     
     if (exists) {
       // Capture component screenshot
       await mcp__playwright__browser_take_screenshot({
         element: component.selector,
         ref: component.selector,
         filename: `component-${component.name}.png`
       });
     }
   }
   ```

5. **Interactive State Testing**:
   ```javascript
   // Test hover states
   const hoverElements = await mcp__playwright__browser_evaluate({
     function: `() => {
       const elements = [];
       document.querySelectorAll('a, button, [role="button"]').forEach(el => {
         const rect = el.getBoundingClientRect();
         if (rect.width > 0 && rect.height > 0) {
           elements.push({
             selector: el.tagName.toLowerCase() + (el.id ? '#' + el.id : ''),
             text: el.textContent.trim().substring(0, 50)
           });
         }
       });
       return elements.slice(0, 5); // Test first 5
     }`
   });
   
   for (const element of hoverElements) {
     // Hover over element
     await mcp__playwright__browser_hover({
       element: element.text,
       ref: element.selector
     });
     
     // Capture hover state
     await mcp__playwright__browser_take_screenshot({
       filename: `hover-${element.text.replace(/[^a-z0-9]/gi, '-')}.png`
     });
   }
   
   // Test focus states
   await mcp__playwright__browser_press_key({ key: "Tab" });
   await mcp__playwright__browser_take_screenshot({
     filename: "focus-state-1.png"
   });
   ```

6. **Form Interaction Testing**:
   ```javascript
   // Find forms
   const forms = await mcp__playwright__browser_evaluate({
     function: `() => {
       return Array.from(document.querySelectorAll('form')).map(form => ({
         id: form.id,
         action: form.action,
         inputs: Array.from(form.querySelectorAll('input, select, textarea')).length
       }));
     }`
   });
   
   for (const form of forms) {
     // Fill form with test data
     await mcp__playwright__browser_type({
       element: "First input field",
       ref: "input[type='text']",
       text: "Test User"
     });
     
     await mcp__playwright__browser_type({
       element: "Email field",
       ref: "input[type='email']",
       text: "test@example.com"
     });
     
     // Capture filled form
     await mcp__playwright__browser_take_screenshot({
       filename: `form-filled-${form.id || 'unnamed'}.png`
     });
     
     // Trigger validation
     await mcp__playwright__browser_click({
       element: "Submit button",
       ref: "button[type='submit']"
     });
     
     // Capture validation state
     await mcp__playwright__browser_take_screenshot({
       filename: `form-validation-${form.id || 'unnamed'}.png`
     });
   }
   ```

7. **Animation and Transition Testing**:
   ```javascript
   // Test page transitions
   const links = await mcp__playwright__browser_evaluate({
     function: `() => {
       return Array.from(document.querySelectorAll('a[href^="/"]')).map(a => ({
         href: a.href,
         text: a.textContent.trim()
       })).slice(0, 3);
     }`
   });
   
   for (const link of links) {
     // Click link
     await mcp__playwright__browser_click({
       element: link.text,
       ref: `a[href="${link.href}"]`
     });
     
     // Capture mid-transition
     await mcp__playwright__browser_wait_for({ time: 0.5 });
     await mcp__playwright__browser_take_screenshot({
       filename: `transition-${link.text.replace(/[^a-z0-9]/gi, '-')}.png`
     });
     
     // Wait for transition complete
     await mcp__playwright__browser_wait_for({ time: 2 });
     await mcp__playwright__browser_take_screenshot({
       filename: `transitioned-${link.text.replace(/[^a-z0-9]/gi, '-')}.png`
     });
     
     // Go back
     await mcp__playwright__browser_navigate_back();
   }
   ```

8. **Chain to React Testing Agent**:
   - Invoke react-tanstack-tester agent:
     ```
     Task: "Create visual regression tests for React components:
           
           Components found:
           ${JSON.stringify(components, null, 2)}
           
           Screenshots captured:
           ${screenshots.map(s => s.filename).join('\n')}
           
           Generate:
           1. Playwright test suite for visual regression
           2. Component-specific visual tests
           3. Interaction visual tests
           4. Cross-browser test matrix"
     ```

9. **Chain to Performance Analysis**:
   - Invoke performance-optimizer agent:
     ```
     Task: "Analyze visual performance metrics:
           
           Network requests: ${networkRequests.length}
           Image requests: ${networkRequests.filter(r => r.url.match(/\.(png|jpg|jpeg|gif|webp)/)).length}
           
           Optimize:
           1. Image loading strategies
           2. Critical CSS extraction
           3. Font loading optimization
           4. Animation performance"
     ```

10. **Generate Visual Test Suite**:
    ```typescript
    // visual-regression.spec.ts
    import { test, expect } from '@playwright/test';
    
    // Viewports to test
    const viewports = ${JSON.stringify(viewports, null, 2)};
    
    test.describe('Visual Regression Tests: $ARGUMENTS', () => {
      // Test each viewport
      viewports.forEach(viewport => {
        test(\`Visual consistency at \${viewport.name}\`, async ({ page }) => {
          // Set viewport
          await page.setViewportSize({
            width: viewport.width,
            height: viewport.height
          });
          
          // Navigate
          await page.goto('$ARGUMENTS');
          
          // Wait for content
          await page.waitForLoadState('networkidle');
          
          // Visual assertion
          await expect(page).toHaveScreenshot(\`\${viewport.name}.png\`, {
            fullPage: true,
            threshold: 0.2,
            maxDiffPixels: 100
          });
        });
      });
      
      // Component isolation tests
      test.describe('Component Visual Tests', () => {
        ${components.map(c => `
        test('${c.name} component visual', async ({ page }) => {
          await page.goto('$ARGUMENTS');
          const component = page.locator('${c.selector}');
          await expect(component).toHaveScreenshot('${c.name}.png');
        });`).join('\n')}
      });
      
      // Interaction visual tests
      test.describe('Interaction States', () => {
        test('Hover states', async ({ page }) => {
          await page.goto('$ARGUMENTS');
          
          const button = page.locator('button').first();
          await button.hover();
          await expect(button).toHaveScreenshot('button-hover.png');
        });
        
        test('Focus states', async ({ page }) => {
          await page.goto('$ARGUMENTS');
          
          await page.keyboard.press('Tab');
          await expect(page).toHaveScreenshot('focus-state.png');
        });
        
        test('Form validation states', async ({ page }) => {
          await page.goto('$ARGUMENTS');
          
          // Submit empty form
          await page.locator('form').first().locator('button[type="submit"]').click();
          await expect(page.locator('form').first()).toHaveScreenshot('form-errors.png');
        });
      });
      
      // Cross-browser tests
      ['chromium', 'firefox', 'webkit'].forEach(browserName => {
        test(\`Cross-browser visual - \${browserName}\`, async ({ page }) => {
          await page.goto('$ARGUMENTS');
          await expect(page).toHaveScreenshot(\`cross-browser-\${browserName}.png\`);
        });
      });
    });
    ```

11. **Generate Visual Diff Analysis**:
    ```javascript
    // visual-diff-analyzer.js
    const pixelmatch = require('pixelmatch');
    const fs = require('fs');
    const PNG = require('pngjs').PNG;
    
    function compareScreenshots(baseline, current) {
      const img1 = PNG.sync.read(fs.readFileSync(baseline));
      const img2 = PNG.sync.read(fs.readFileSync(current));
      const {width, height} = img1;
      const diff = new PNG({width, height});
      
      const numDiffPixels = pixelmatch(
        img1.data, img2.data, diff.data, width, height,
        {threshold: 0.1}
      );
      
      return {
        diffPixels: numDiffPixels,
        diffPercentage: (numDiffPixels / (width * height)) * 100,
        diffImage: diff
      };
    }
    
    // Analyze all screenshots
    const results = screenshots.map(s => {
      const baseline = \`baseline-\${s.filename}\`;
      const current = \`current-\${s.filename}\`;
      
      if (fs.existsSync(baseline) && fs.existsSync(current)) {
        return {
          name: s.filename,
          ...compareScreenshots(baseline, current)
        };
      }
      return null;
    }).filter(Boolean);
    ```

12. **Generate Visual Testing Report**:
    ```markdown
    # Visual Regression Test Report: $ARGUMENTS
    
    ## Test Coverage
    - Viewports Tested: ${viewports.length}
    - Components Tested: ${components.length}
    - Interaction States: ${hoverElements.length + forms.length}
    - Cross-browser: Chrome, Firefox, Safari
    
    ## Visual Consistency Results
    ### Desktop (1920x1080)
    - Baseline: [OK] Captured
    - Difference: ${results.find(r => r.name.includes('Desktop'))?.diffPercentage || 0}%
    - Status: ${results.find(r => r.name.includes('Desktop'))?.diffPercentage < 1 ? '[OK] PASS' : '[X] FAIL'}
    
    ### Tablet (768x1024)
    - Baseline: [OK] Captured
    - Difference: ${results.find(r => r.name.includes('Tablet'))?.diffPercentage || 0}%
    - Status: ${results.find(r => r.name.includes('Tablet'))?.diffPercentage < 1 ? '[OK] PASS' : '[X] FAIL'}
    
    ### Mobile (375x667)
    - Baseline: [OK] Captured
    - Difference: ${results.find(r => r.name.includes('Mobile'))?.diffPercentage || 0}%
    - Status: ${results.find(r => r.name.includes('Mobile'))?.diffPercentage < 1 ? '[OK] PASS' : '[X] FAIL'}
    
    ## Component Visual Tests
    ${components.map(c => `
    ### ${c.name}
    - Screenshot: [OK] Captured
    - Visual Consistency: [OK] PASS
    - Accessibility: ${c.accessible ? '[OK]' : '⚠️'} 
    `).join('\n')}
    
    ## Interaction States
    - Hover Effects: [OK] Tested
    - Focus States: [OK] Tested
    - Active States: [OK] Tested
    - Form Validation: [OK] Tested
    
    ## Performance Metrics
    - Total Image Requests: ${networkRequests.filter(r => r.url.match(/\.(png|jpg|jpeg|gif|webp)/)).length}
    - Image Load Time: ${imageLoadTime}ms
    - First Contentful Paint: ${fcp}ms
    - Layout Shifts: ${cls}
    
    ## Accessibility Issues
    ${accessibilityIssues.map(issue => `- ${issue}`).join('\n') || '- None found'}
    
    ## Recommendations
    1. ${recommendations[0] || 'Optimize image sizes for different viewports'}
    2. ${recommendations[1] || 'Implement lazy loading for below-fold images'}
    3. ${recommendations[2] || 'Add ARIA labels to interactive elements'}
    
    ## Test Files Generated
    - visual-regression.spec.ts
    - component-visual.spec.ts
    - interaction-visual.spec.ts
    - cross-browser.spec.ts
    
    ## CI/CD Integration
    \`\`\`yaml
    # .github/workflows/visual-tests.yml
    - name: Run Visual Tests
      run: npx playwright test --project=chromium
    - name: Upload Screenshots
      uses: actions/upload-artifact@v3
      with:
        name: screenshots
        path: test-results/
    \`\`\`
    ```
</actions>

The assistant should use Playwright's powerful visual testing capabilities to create comprehensive regression tests, then chain specialized agents to analyze results and optimize visual performance.