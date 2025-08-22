#!/usr/bin/env node

/**
 * Work Completion Assistant Hook for JavaScript/TypeScript
 * =========================================================
 * Type: Stop
 * Description: Ensures work is complete before allowing Claude to stop
 *
 * This hook validates that all work has been properly completed, including:
 * - Tests are passing
 * - No unresolved TODOs
 * - Code is formatted
 * - Documentation is updated
 * - Changes are committed (optionally)
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

class WorkCompletionValidator {
    constructor(projectDir) {
        this.projectDir = projectDir;
        this.issues = [];
        this.warnings = [];
    }

    checkUncommittedChanges() {
        try {
            const status = execSync('git status --porcelain', {
                encoding: 'utf8',
                cwd: this.projectDir
            }).trim();

            if (status) {
                const changedFiles = status.split('\n').length;
                this.warnings.push(`You have ${changedFiles} uncommitted changes`);
                return false;
            }
            return true;
        } catch {
            return true; // Not a git repo, skip
        }
    }

    checkTodosInChangedFiles() {
        try {
            // Get changed files
            const diffFiles = execSync('git diff --name-only HEAD', {
                encoding: 'utf8',
                cwd: this.projectDir
            }).trim().split('\n').filter(Boolean);

            const stagedFiles = execSync('git diff --cached --name-only', {
                encoding: 'utf8',
                cwd: this.projectDir
            }).trim().split('\n').filter(Boolean);

            const allFiles = [...new Set([...diffFiles, ...stagedFiles])];
            const filesWithTodos = [];

            for (const file of allFiles) {
                const filePath = path.join(this.projectDir, file);
                if (fs.existsSync(filePath)) {
                    try {
                        const content = fs.readFileSync(filePath, 'utf8');
                        if (/TODO|FIXME|XXX|HACK/.test(content)) {
                            filesWithTodos.push(file);
                        }
                    } catch {}
                }
            }

            if (filesWithTodos.length) {
                this.issues.push(`Unresolved TODOs in: ${filesWithTodos.slice(0, 3).join(', ')}`);
                return false;
            }
            return true;
        } catch {
            return true;
        }
    }

    checkTests() {
        const packageJsonPath = path.join(this.projectDir, 'package.json');
        
        if (!fs.existsSync(packageJsonPath)) {
            return true; // No package.json, skip
        }

        try {
            const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
            const scripts = packageJson.scripts || {};
            
            // Check for test scripts
            const testCommands = [];
            if (scripts.test) {
                testCommands.push('test');
            }
            if (scripts['test:unit']) {
                testCommands.push('test:unit');
            }
            
            if (testCommands.length) {
                // Check if using bun or npm
                const runner = fs.existsSync(path.join(this.projectDir, 'bun.lockb')) ? 'bun' : 'npm';
                this.warnings.push(`Remember to run tests: ${runner} run ${testCommands[0]}`);
            }
            
            // Check for test configuration files
            const testConfigs = [
                'jest.config.js',
                'jest.config.ts',
                'vitest.config.js',
                'vitest.config.ts',
                '.mocharc.json',
                'playwright.config.js',
                'cypress.config.js'
            ];
            
            for (const config of testConfigs) {
                if (fs.existsSync(path.join(this.projectDir, config))) {
                    const testRunner = config.split('.')[0].split('rc')[0];
                    this.warnings.push(`${testRunner} configuration found - ensure tests pass`);
                    break;
                }
            }
            
            return true; // Don't block on tests
        } catch {
            return true;
        }
    }

    checkLinting() {
        // Check for linting configs
        const lintConfigs = [
            'eslint.config.js',
            '.eslintrc.js',
            '.eslintrc.json',
            'biome.json',
            '.prettierrc',
            'prettier.config.js'
        ];

        for (const config of lintConfigs) {
            if (fs.existsSync(path.join(this.projectDir, config))) {
                const linter = config.includes('eslint') ? 'ESLint' : 
                              config.includes('prettier') ? 'Prettier' : 
                              config.includes('biome') ? 'Biome' : 'Linter';
                this.warnings.push(`Remember to run ${linter}`);
                break;
            }
        }

        return true; // Don't block on linting
    }

    checkDocumentation() {
        try {
            // Check if code files were changed
            const changedFiles = execSync('git diff --name-only HEAD', {
                encoding: 'utf8',
                cwd: this.projectDir
            }).trim().split('\n').filter(Boolean);

            const codeFilesChanged = changedFiles.some(f => 
                /\.(js|jsx|ts|tsx|mjs|cjs)$/.test(f)
            );

            const docsChanged = changedFiles.some(f => 
                /\.(md|mdx)$/.test(f) || f.includes('docs/')
            );

            if (codeFilesChanged && !docsChanged) {
                this.warnings.push('Code changed but documentation not updated');
            }

            // Check for JSDoc in TypeScript/JavaScript files
            if (codeFilesChanged) {
                const undocumentedExports = [];
                
                for (const file of changedFiles.filter(f => /\.(js|ts|jsx|tsx)$/.test(f)).slice(0, 3)) {
                    const filePath = path.join(this.projectDir, file);
                    if (fs.existsSync(filePath)) {
                        try {
                            const content = fs.readFileSync(filePath, 'utf8');
                            
                            // Check for exported functions without JSDoc
                            const exportPattern = /export\s+(async\s+)?function\s+(\w+)/g;
                            let match;
                            while ((match = exportPattern.exec(content)) !== null) {
                                const funcName = match[2];
                                const beforeFunc = content.substring(Math.max(0, match.index - 200), match.index);
                                if (!beforeFunc.includes('/**')) {
                                    undocumentedExports.push(`${file}:${funcName}`);
                                }
                            }
                        } catch {}
                    }
                }
                
                if (undocumentedExports.length) {
                    this.warnings.push(`Undocumented exports: ${undocumentedExports.slice(0, 3).join(', ')}`);
                }
            }

            return true; // Don't block on documentation
        } catch {
            return true;
        }
    }

    checkBranches() {
        try {
            const branch = execSync('git branch --show-current', {
                encoding: 'utf8',
                cwd: this.projectDir
            }).trim();

            if (['main', 'master', 'production'].includes(branch)) {
                this.warnings.push(`Working directly on ${branch} branch`);
            }

            return true; // Don't block on branch
        } catch {
            return true;
        }
    }

    checkTypeScript() {
        // Check for TypeScript errors
        const tsconfigPath = path.join(this.projectDir, 'tsconfig.json');
        
        if (fs.existsSync(tsconfigPath)) {
            this.warnings.push('Remember to check TypeScript compilation: npx tsc --noEmit');
            
            // Check for any .ts files with @ts-ignore or @ts-expect-error
            try {
                const tsFiles = execSync('find . -name "*.ts" -o -name "*.tsx" 2>/dev/null | head -20', {
                    encoding: 'utf8',
                    cwd: this.projectDir
                }).trim().split('\n').filter(Boolean);
                
                let ignoreCount = 0;
                for (const file of tsFiles) {
                    const filePath = path.join(this.projectDir, file);
                    if (fs.existsSync(filePath)) {
                        try {
                            const content = fs.readFileSync(filePath, 'utf8');
                            const matches = content.match(/@ts-ignore|@ts-expect-error/g);
                            if (matches) {
                                ignoreCount += matches.length;
                            }
                        } catch {}
                    }
                }
                
                if (ignoreCount > 0) {
                    this.warnings.push(`Found ${ignoreCount} TypeScript ignore comments`);
                }
            } catch {}
        }
        
        return true;
    }

    validate() {
        // Run all checks
        this.checkUncommittedChanges();
        this.checkTodosInChangedFiles();
        this.checkTests();
        this.checkLinting();
        this.checkDocumentation();
        this.checkBranches();
        this.checkTypeScript();

        // Determine if we should block
        const shouldBlock = this.issues.length > 0;

        if (shouldBlock) {
            let reason = 'Work incomplete:\n';
            reason += this.issues.map(issue => `❌ ${issue}`).join('\n');
            
            if (this.warnings.length) {
                reason += '\n\nWarnings:\n';
                reason += this.warnings.map(warning => `⚠️  ${warning}`).join('\n');
            }

            return {
                decision: 'block',
                reason: reason + '\n\nPlease address these items before stopping.'
            };
        } else if (this.warnings.length) {
            // Just show warnings, don't block
            const summary = 'Work appears complete. Reminders:\n' +
                          this.warnings.map(warning => `⚠️  ${warning}`).join('\n');
            
            console.error(summary); // Use stderr for output
            return {};
        } else {
            console.error('✅ All checks passed - work appears complete!');
            return {};
        }
    }
}

// Main execution
let inputData = '';
process.stdin.on('data', chunk => inputData += chunk);
process.stdin.on('end', () => {
    try {
        const data = JSON.parse(inputData);
        
        // Check if we're already in a stop hook loop
        if (data.stop_hook_active) {
            process.exit(0); // Don't create infinite loops
        }
        
        const projectDir = data.cwd || process.cwd();
        
        const validator = new WorkCompletionValidator(projectDir);
        const result = validator.validate();
        
        if (result.decision) {
            console.log(JSON.stringify(result));
        }
        
        process.exit(0);
    } catch (error) {
        // Don't block on errors
        process.exit(0);
    }
});