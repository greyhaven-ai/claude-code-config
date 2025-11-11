#!/usr/bin/env node

/**
 * Subagent Context Preparer Hook for JavaScript/TypeScript
 * =========================================================
 * Type: PreToolUse (Task)
 * Description: Prepares optimal context for subagent tasks
 *
 * This hook analyzes the task description and injects relevant context
 * to help subagents complete their work independently and correctly.
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

class SubagentContextPreparer {
    constructor(projectDir, taskDescription) {
        this.projectDir = projectDir;
        this.task = taskDescription.toLowerCase();
        this.contextItems = [];
    }

    detectTaskType() {
        return {
            research: /research|find|search|analyze|investigate/.test(this.task),
            implementation: /implement|create|build|add|write/.test(this.task),
            refactoring: /refactor|optimize|improve|clean|reorganize/.test(this.task),
            testing: /test|spec|coverage|unit test|integration/.test(this.task),
            debugging: /debug|fix|bug|error|issue/.test(this.task),
            documentation: /document|docs|readme|comment|explain/.test(this.task),
            review: /review|check|validate|verify|audit/.test(this.task),
            component: /component|react|vue|angular|svelte/.test(this.task),
            api: /api|endpoint|route|controller|middleware/.test(this.task),
            styling: /style|css|sass|tailwind|styled-components/.test(this.task),
        };
    }

    getProjectStructureContext() {
        const context = ['=== Project Structure Overview ==='];
        
        // Get main directories
        const importantDirs = [
            'src', 'app', 'pages', 'components', 'lib', 'utils',
            'api', 'server', 'client', 'public', 'tests', 'docs'
        ];
        
        const existingDirs = importantDirs.filter(dir => 
            fs.existsSync(path.join(this.projectDir, dir))
        );
        
        if (existingDirs.length) {
            context.push(`Key directories: ${existingDirs.join(', ')}`);
        }
        
        // Detect project type from package.json
        const packageJsonPath = path.join(this.projectDir, 'package.json');
        if (fs.existsSync(packageJsonPath)) {
            try {
                const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
                const deps = { ...packageJson.dependencies, ...packageJson.devDependencies };
                
                const frameworks = [];
                if (deps['next']) frameworks.push('Next.js');
                if (deps['react']) frameworks.push('React');
                if (deps['vue']) frameworks.push('Vue');
                if (deps['@angular/core']) frameworks.push('Angular');
                if (deps['svelte']) frameworks.push('Svelte');
                if (deps['express']) frameworks.push('Express');
                if (deps['fastify']) frameworks.push('Fastify');
                if (deps['@nestjs/core']) frameworks.push('NestJS');
                if (deps['remix']) frameworks.push('Remix');
                if (deps['nuxt']) frameworks.push('Nuxt');
                
                if (frameworks.length) {
                    context.push(`Frameworks: ${frameworks.join(', ')}`);
                }
                
                // Detect TypeScript
                if (deps['typescript']) {
                    context.push('TypeScript: Enabled');
                }
                
                // File counts
                try {
                    const jsCount = execSync(`find "${this.projectDir}" -name "*.js" -o -name "*.jsx" 2>/dev/null | wc -l`, { encoding: 'utf8' }).trim();
                    const tsCount = execSync(`find "${this.projectDir}" -name "*.ts" -o -name "*.tsx" 2>/dev/null | wc -l`, { encoding: 'utf8' }).trim();
                    
                    context.push('File distribution:');
                    if (parseInt(jsCount) > 0) context.push(`  JavaScript: ${jsCount} files`);
                    if (parseInt(tsCount) > 0) context.push(`  TypeScript: ${tsCount} files`);
                } catch {}
            } catch {}
        }
        
        return context.length > 1 ? context.join('\n') : null;
    }

    getCodingStandards() {
        const context = ['=== Coding Standards ==='];
        let foundStandards = false;
        
        // Check for linter configs
        const linterConfigs = {
            'eslint.config.js': 'ESLint',
            '.eslintrc.js': 'ESLint',
            '.eslintrc.json': 'ESLint',
            'biome.json': 'Biome',
            '.prettierrc': 'Prettier',
            'prettier.config.js': 'Prettier',
        };
        
        for (const [file, tool] of Object.entries(linterConfigs)) {
            if (fs.existsSync(path.join(this.projectDir, file))) {
                context.push(`${tool}: Using ${file}`);
                foundStandards = true;
                
                // Extract key settings for ESLint
                if (tool === 'ESLint' && file.endsWith('.js')) {
                    try {
                        const configPath = path.join(this.projectDir, file);
                        const content = fs.readFileSync(configPath, 'utf8');
                        
                        if (content.includes('airbnb')) {
                            context.push('  - Style: Airbnb');
                        } else if (content.includes('standard')) {
                            context.push('  - Style: Standard');
                        }
                    } catch {}
                }
            }
        }
        
        // Check for TypeScript config
        if (fs.existsSync(path.join(this.projectDir, 'tsconfig.json'))) {
            context.push('TypeScript: Using tsconfig.json');
            try {
                const tsconfig = JSON.parse(fs.readFileSync(path.join(this.projectDir, 'tsconfig.json'), 'utf8'));
                if (tsconfig.compilerOptions?.strict) {
                    context.push('  - Strict mode enabled');
                }
            } catch {}
            foundStandards = true;
        }
        
        // Check for editor config
        if (fs.existsSync(path.join(this.projectDir, '.editorconfig'))) {
            context.push('Editor: Using .editorconfig');
            foundStandards = true;
        }
        
        return foundStandards ? context.join('\n') : null;
    }

    getSimilarImplementations() {
        const context = ['=== Similar Implementations ==='];
        
        // Extract key terms from task
        const keyTerms = this.task.match(/\b[a-z]{4,}\b/g) || [];
        const relevantTerms = keyTerms.filter(term => 
            !['that', 'this', 'with', 'from', 'into', 'have', 'been', 'will', 'should', 'could'].includes(term)
        );
        
        if (!relevantTerms.length) return null;
        
        // Search for files containing these terms
        const similarFiles = new Set();
        
        for (const term of relevantTerms.slice(0, 3)) {
            try {
                const result = execSync(
                    `grep -l -r -i "${term}" "${this.projectDir}" --include="*.js" --include="*.jsx" --include="*.ts" --include="*.tsx" 2>/dev/null | head -5`,
                    { encoding: 'utf8', timeout: 2000 }
                ).trim();
                
                if (result) {
                    result.split('\n').forEach(file => similarFiles.add(file));
                }
            } catch {}
        }
        
        if (similarFiles.size > 0) {
            context.push('Files with potentially similar logic:');
            for (const file of Array.from(similarFiles).slice(0, 5)) {
                const relativePath = path.relative(this.projectDir, file);
                context.push(`  - ${relativePath}`);
            }
            return context.join('\n');
        }
        
        return null;
    }

    getTestExamples() {
        const context = ['=== Test Examples ==='];
        
        // Find test files
        const testPatterns = ['**/*.test.*', '**/*.spec.*', '**/__tests__/**'];
        const testFiles = [];
        
        try {
            const result = execSync(
                `find "${this.projectDir}" -name "*.test.js" -o -name "*.test.ts" -o -name "*.spec.js" -o -name "*.spec.ts" 2>/dev/null | head -5`,
                { encoding: 'utf8' }
            ).trim();
            
            if (result) {
                testFiles.push(...result.split('\n'));
            }
        } catch {}
        
        if (testFiles.length === 0) return null;
        
        // Get sample test structure
        const sampleTest = testFiles[0];
        context.push(`Example test structure from ${path.basename(sampleTest)}:`);
        
        try {
            const content = fs.readFileSync(sampleTest, 'utf8');
            const lines = content.split('\n').slice(0, 30);
            
            for (const line of lines) {
                if (/describe\(|it\(|test\(|expect\(|beforeEach\(|afterEach\(/.test(line)) {
                    const trimmed = line.trim();
                    if (trimmed.length <= 60) {
                        context.push(`  ${trimmed}`);
                    } else {
                        context.push(`  ${trimmed.substring(0, 57)}...`);
                    }
                }
            }
        } catch {}
        
        return context.length > 1 ? context.join('\n') : null;
    }

    getComponentPatterns() {
        const context = ['=== Component Patterns ==='];
        
        // Look for React/Vue/Svelte components
        const componentDirs = ['components', 'src/components', 'app/components'];
        
        for (const dir of componentDirs) {
            const dirPath = path.join(this.projectDir, dir);
            if (fs.existsSync(dirPath)) {
                try {
                    const files = fs.readdirSync(dirPath).slice(0, 5);
                    
                    // Analyze a sample component
                    for (const file of files) {
                        if (/\.(jsx?|tsx?)$/.test(file)) {
                            const filePath = path.join(dirPath, file);
                            const content = fs.readFileSync(filePath, 'utf8');
                            
                            // Detect patterns
                            const patterns = [];
                            if (/useState|useEffect|useContext/.test(content)) {
                                patterns.push('React Hooks');
                            }
                            if (/export default function/.test(content)) {
                                patterns.push('Functional Components');
                            }
                            if (/class\s+\w+\s+extends\s+(React\.)?Component/.test(content)) {
                                patterns.push('Class Components');
                            }
                            if (/styled\.|css`/.test(content)) {
                                patterns.push('CSS-in-JS');
                            }
                            if (/\.module\.css|\.module\.scss/.test(content)) {
                                patterns.push('CSS Modules');
                            }
                            
                            if (patterns.length) {
                                context.push(`Component patterns found:`);
                                patterns.forEach(p => context.push(`  - ${p}`));
                                break;
                            }
                        }
                    }
                } catch {}
                break;
            }
        }
        
        return context.length > 1 ? context.join('\n') : null;
    }

    getPerformanceGuidelines() {
        const taskType = this.detectTaskType();
        
        if (!(taskType.implementation || taskType.refactoring)) {
            return null;
        }
        
        const context = ['=== Performance Guidelines ==='];
        
        const packageJsonPath = path.join(this.projectDir, 'package.json');
        if (fs.existsSync(packageJsonPath)) {
            try {
                const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
                const deps = { ...packageJson.dependencies, ...packageJson.devDependencies };
                
                if (deps['react']) {
                    context.push('React:');
                    context.push('  - Use React.memo for expensive components');
                    context.push('  - Implement useMemo/useCallback for expensive computations');
                    context.push('  - Consider virtualization for long lists');
                    context.push('  - Lazy load components with React.lazy');
                }
                
                if (deps['next']) {
                    context.push('Next.js:');
                    context.push('  - Use static generation when possible');
                    context.push('  - Implement ISR for dynamic content');
                    context.push('  - Optimize images with next/image');
                    context.push('  - Use dynamic imports for code splitting');
                }
                
                context.push('General JavaScript:');
                context.push('  - Prefer async/await over callbacks');
                context.push('  - Use Web Workers for heavy computations');
                context.push('  - Implement debounce/throttle for frequent events');
                context.push('  - Consider bundle size impact');
            } catch {}
        }
        
        return context.length > 1 ? context.join('\n') : null;
    }

    prepareContext() {
        const taskType = this.detectTaskType();
        const contexts = [];
        
        // Always provide project structure
        const projectContext = this.getProjectStructureContext();
        if (projectContext) contexts.push(projectContext);
        
        // Always provide coding standards
        const standards = this.getCodingStandards();
        if (standards) contexts.push(standards);
        
        // Task-specific context
        if (taskType.implementation || taskType.refactoring) {
            const similar = this.getSimilarImplementations();
            if (similar) contexts.push(similar);
            
            const perf = this.getPerformanceGuidelines();
            if (perf) contexts.push(perf);
        }
        
        if (taskType.testing) {
            const testExamples = this.getTestExamples();
            if (testExamples) contexts.push(testExamples);
        }
        
        if (taskType.component) {
            const componentPatterns = this.getComponentPatterns();
            if (componentPatterns) contexts.push(componentPatterns);
        }
        
        // Add task-specific tips
        contexts.push('=== Task Guidelines ===');
        if (taskType.research) {
            contexts.push('Research task: Be thorough and provide sources');
        }
        if (taskType.implementation) {
            contexts.push('Implementation task: Follow existing patterns and test your code');
        }
        if (taskType.testing) {
            contexts.push('Testing task: Cover edge cases and maintain consistency with existing tests');
        }
        if (taskType.debugging) {
            contexts.push('Debugging task: Identify root cause, not just symptoms');
        }
        if (taskType.documentation) {
            contexts.push('Documentation task: Be clear, include examples, use JSDoc where appropriate');
        }
        
        return contexts.join('\n\n');
    }
}

// Main execution
let inputData = '';
process.stdin.on('data', chunk => inputData += chunk);
process.stdin.on('end', () => {
    try {
        const data = JSON.parse(inputData);
        const toolName = data.tool_name || '';
        
        // Only process Task tool calls
        if (toolName !== 'Task') {
            process.exit(0);
        }
        
        const toolInput = data.tool_input || {};
        const taskDescription = toolInput.prompt || '';
        const projectDir = data.cwd || process.cwd();
        
        if (!taskDescription) {
            process.exit(0);
        }
        
        const preparer = new SubagentContextPreparer(projectDir, taskDescription);
        const context = preparer.prepareContext();
        
        // Inject context into task description
        const enhancedPrompt = `[Subagent Context]
${context}

[Original Task]
${taskDescription}

Remember to:
1. Follow the project's coding standards
2. Use similar implementations as reference
3. Test your changes if implementing code
4. Update documentation if needed
5. Consider performance implications`;
        
        // Modify tool input
        toolInput.prompt = enhancedPrompt;
        
        // Auto-approve with enhanced context
        const output = {
            hookSpecificOutput: {
                hookEventName: 'PreToolUse',
                permissionDecision: 'allow',
                permissionDecisionReason: 'Task enhanced with project context'
            },
            suppressOutput: true
        };
        
        console.log(JSON.stringify(output));
        process.exit(0);
    } catch (error) {
        // Don't block on errors
        process.exit(0);
    }
});