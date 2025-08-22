#!/usr/bin/env node

/**
 * Prompt Enhancer Hook for JavaScript/TypeScript
 * ===============================================
 * Type: UserPromptSubmit
 * Description: Intelligently enhances user prompts with relevant context
 *
 * This hook analyzes user prompts and automatically injects relevant context
 * like documentation, test coverage, dependency graphs, and recent changes.
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

class PromptEnhancer {
    constructor(projectDir) {
        this.projectDir = projectDir;
        this.contextAdditions = [];
    }

    detectIntent(prompt) {
        const promptLower = prompt.toLowerCase();
        
        return {
            testing: /test|spec|coverage|jest|vitest|mocha/.test(promptLower),
            debugging: /bug|fix|error|issue|debug/.test(promptLower),
            feature: /implement|add|create|feature|build/.test(promptLower),
            refactor: /refactor|optimize|improve|clean/.test(promptLower),
            documentation: /document|docs|readme|comment/.test(promptLower),
            api: /api|endpoint|route|request|response/.test(promptLower),
            database: /database|query|sql|migration|schema|prisma|typeorm/.test(promptLower),
            security: /security|auth|permission|vulnerability|cors/.test(promptLower),
            performance: /performance|speed|optimize|slow|bundle/.test(promptLower),
            component: /component|react|vue|svelte|angular/.test(promptLower),
            styling: /css|style|sass|tailwind|styled/.test(promptLower),
        };
    }

    extractFileReferences(prompt) {
        const files = [];
        
        // Common file patterns
        const patterns = [
            /[./\w-]+\.\w+/g,  // Files with extensions
            /`([^`]+)`/g,       // Backtick references
            /"([^"]+)"/g,       // Quoted references
        ];
        
        for (const pattern of patterns) {
            const matches = prompt.matchAll(pattern);
            for (const match of matches) {
                const filename = match[1] || match[0];
                if (filename.includes('.') && !filename.startsWith('http')) {
                    // Try to find the file
                    try {
                        const findResult = execSync(
                            `find "${this.projectDir}" -name "${filename}" 2>/dev/null | head -5`,
                            { encoding: 'utf8' }
                        ).trim();
                        
                        if (findResult) {
                            files.push(...findResult.split('\n'));
                        }
                    } catch {}
                }
            }
        }
        
        return [...new Set(files)];
    }

    getTestCoverageContext(files) {
        if (!files.length) return null;
        
        const context = [];
        
        for (const file of files.slice(0, 3)) {
            const basename = path.basename(file, path.extname(file));
            const dirname = path.dirname(file);
            
            // Check for test files
            const testPatterns = [
                `${basename}.test.js`,
                `${basename}.test.ts`,
                `${basename}.spec.js`,
                `${basename}.spec.ts`,
                `${basename}.test.jsx`,
                `${basename}.test.tsx`,
            ];
            
            let hasTest = false;
            for (const pattern of testPatterns) {
                const testPath = path.join(dirname, pattern);
                const testInTestsDir = path.join(dirname, '__tests__', pattern);
                
                if (fs.existsSync(testPath) || fs.existsSync(testInTestsDir)) {
                    hasTest = true;
                    context.push(`Test file exists for: ${path.relative(this.projectDir, file)}`);
                    break;
                }
            }
            
            if (!hasTest) {
                context.push(`No test file found for: ${path.relative(this.projectDir, file)}`);
            }
        }
        
        return context.length ? context.join('\n') : null;
    }

    getPackageContext() {
        const packagePath = path.join(this.projectDir, 'package.json');
        if (!fs.existsSync(packagePath)) return null;
        
        try {
            const packageJson = JSON.parse(fs.readFileSync(packagePath, 'utf8'));
            const context = [];
            
            // Detect frameworks
            const deps = { ...packageJson.dependencies, ...packageJson.devDependencies };
            
            const frameworks = [];
            if (deps['react']) frameworks.push('React');
            if (deps['vue']) frameworks.push('Vue');
            if (deps['@angular/core']) frameworks.push('Angular');
            if (deps['svelte']) frameworks.push('Svelte');
            if (deps['next']) frameworks.push('Next.js');
            if (deps['nuxt']) frameworks.push('Nuxt');
            if (deps['express']) frameworks.push('Express');
            if (deps['fastify']) frameworks.push('Fastify');
            if (deps['@nestjs/core']) frameworks.push('NestJS');
            
            if (frameworks.length) {
                context.push(`Frameworks: ${frameworks.join(', ')}`);
            }
            
            // Detect test runners
            const testRunners = [];
            if (deps['jest']) testRunners.push('Jest');
            if (deps['vitest']) testRunners.push('Vitest');
            if (deps['mocha']) testRunners.push('Mocha');
            if (deps['@playwright/test']) testRunners.push('Playwright');
            if (deps['cypress']) testRunners.push('Cypress');
            
            if (testRunners.length) {
                context.push(`Test runners: ${testRunners.join(', ')}`);
            }
            
            // Check for build tools
            const buildTools = [];
            if (deps['webpack']) buildTools.push('Webpack');
            if (deps['vite']) buildTools.push('Vite');
            if (deps['esbuild']) buildTools.push('esbuild');
            if (deps['rollup']) buildTools.push('Rollup');
            if (deps['parcel']) buildTools.push('Parcel');
            
            if (buildTools.length) {
                context.push(`Build tools: ${buildTools.join(', ')}`);
            }
            
            // Check scripts
            if (packageJson.scripts) {
                const scripts = Object.keys(packageJson.scripts);
                const relevantScripts = scripts.filter(s => 
                    /test|lint|build|dev|start|format/.test(s)
                );
                if (relevantScripts.length) {
                    context.push(`Available scripts: ${relevantScripts.join(', ')}`);
                }
            }
            
            return context.length ? context.join('\n') : null;
        } catch {
            return null;
        }
    }

    getRecentChangesContext(files) {
        if (!files.length) return null;
        
        const context = [];
        
        for (const file of files.slice(0, 3)) {
            try {
                const gitLog = execSync(
                    `git log --oneline -3 -- "${file}" 2>/dev/null`,
                    { encoding: 'utf8', cwd: this.projectDir }
                ).trim();
                
                if (gitLog) {
                    const relativePath = path.relative(this.projectDir, file);
                    context.push(`Recent changes to ${relativePath}:`);
                    context.push(gitLog);
                }
            } catch {}
        }
        
        return context.length ? context.join('\n') : null;
    }

    getDependencyContext(files) {
        if (!files.length) return null;
        
        const context = [];
        
        for (const file of files.slice(0, 2)) {
            if (/\.(js|jsx|ts|tsx|mjs|cjs)$/.test(file)) {
                try {
                    const content = fs.readFileSync(file, 'utf8');
                    const lines = content.split('\n').slice(0, 50);
                    
                    const imports = [];
                    for (const line of lines) {
                        // ES6 imports
                        if (/^import\s/.test(line.trim())) {
                            imports.push(line.trim());
                        }
                        // CommonJS requires
                        if (/require\(['"']/.test(line)) {
                            imports.push(line.trim());
                        }
                    }
                    
                    if (imports.length) {
                        const relativePath = path.relative(this.projectDir, file);
                        context.push(`Dependencies in ${relativePath}:`);
                        context.push(...imports.slice(0, 5));
                    }
                } catch {}
            }
        }
        
        return context.length ? context.join('\n') : null;
    }

    getComponentContext() {
        const context = [];
        
        // Look for component directories
        const componentDirs = ['components', 'src/components', 'app/components', 'views'];
        
        for (const dir of componentDirs) {
            const dirPath = path.join(this.projectDir, dir);
            if (fs.existsSync(dirPath) && fs.statSync(dirPath).isDirectory()) {
                try {
                    const files = fs.readdirSync(dirPath).slice(0, 10);
                    if (files.length) {
                        context.push(`Component directory found: ${dir}`);
                        context.push(`Components: ${files.join(', ')}`);
                        break;
                    }
                } catch {}
            }
        }
        
        return context.length ? context.join('\n') : null;
    }

    getAPIContext() {
        const context = [];
        
        // Look for API route directories (Next.js, Nuxt, etc.)
        const apiDirs = [
            'pages/api',
            'app/api',
            'src/api',
            'server/api',
            'routes',
            'src/routes'
        ];
        
        for (const dir of apiDirs) {
            const dirPath = path.join(this.projectDir, dir);
            if (fs.existsSync(dirPath)) {
                context.push(`API directory found: ${dir}`);
                
                try {
                    const files = fs.readdirSync(dirPath).slice(0, 5);
                    if (files.length) {
                        context.push(`API files: ${files.join(', ')}`);
                    }
                } catch {}
                break;
            }
        }
        
        // Check for OpenAPI/Swagger
        const specFiles = ['openapi.json', 'openapi.yaml', 'swagger.json', 'swagger.yaml'];
        for (const spec of specFiles) {
            if (fs.existsSync(path.join(this.projectDir, spec))) {
                context.push(`API specification found: ${spec}`);
                break;
            }
        }
        
        return context.length ? context.join('\n') : null;
    }

    enhancePrompt(prompt) {
        const intent = this.detectIntent(prompt);
        const files = this.extractFileReferences(prompt);
        
        const contexts = [];
        
        // Add package.json context
        const packageContext = this.getPackageContext();
        if (packageContext) {
            contexts.push('=== Project Setup ===');
            contexts.push(packageContext);
        }
        
        // Add file-specific contexts
        if (files.length) {
            contexts.push(`Referenced files: ${files.map(f => path.basename(f)).slice(0, 5).join(', ')}`);
            
            if (intent.testing) {
                const coverage = this.getTestCoverageContext(files);
                if (coverage) {
                    contexts.push('=== Test Coverage ===');
                    contexts.push(coverage);
                }
            }
            
            if (intent.debugging) {
                const changes = this.getRecentChangesContext(files);
                if (changes) {
                    contexts.push('=== Recent Changes ===');
                    contexts.push(changes);
                }
            }
            
            const deps = this.getDependencyContext(files);
            if (deps) {
                contexts.push('=== Dependencies ===');
                contexts.push(deps);
            }
        }
        
        // Add intent-specific contexts
        if (intent.component) {
            const componentContext = this.getComponentContext();
            if (componentContext) {
                contexts.push('=== Components ===');
                contexts.push(componentContext);
            }
        }
        
        if (intent.api) {
            const apiContext = this.getAPIContext();
            if (apiContext) {
                contexts.push('=== API Context ===');
                contexts.push(apiContext);
            }
        }
        
        // Add branch context
        try {
            const branch = execSync(
                'git branch --show-current',
                { encoding: 'utf8', cwd: this.projectDir }
            ).trim();
            
            if (branch && branch !== 'main' && branch !== 'master') {
                contexts.push(`Current branch: ${branch}`);
            }
        } catch {}
        
        return contexts.length ? contexts.join('\n\n') : null;
    }
}

// Main execution
let inputData = '';
process.stdin.on('data', chunk => inputData += chunk);
process.stdin.on('end', () => {
    try {
        const data = JSON.parse(inputData);
        const prompt = data.prompt || '';
        const projectDir = data.cwd || process.cwd();
        
        const enhancer = new PromptEnhancer(projectDir);
        const additionalContext = enhancer.enhancePrompt(prompt);
        
        if (additionalContext) {
            const output = {
                hookSpecificOutput: {
                    hookEventName: 'UserPromptSubmit',
                    additionalContext: `[Automated Context]\n${additionalContext}`
                }
            };
            console.log(JSON.stringify(output));
        }
    } catch (error) {
        // Don't block on errors
        process.exit(0);
    }
});