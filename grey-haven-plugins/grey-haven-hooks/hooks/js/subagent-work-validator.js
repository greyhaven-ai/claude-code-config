#!/usr/bin/env node

/**
 * Subagent Work Validator Hook for JavaScript/TypeScript
 * ========================================================
 * Type: SubagentStop, PostToolUse(Task)
 * Description: Validates that subagent completed its assigned task properly
 *
 * This hook ensures subagents have completed their work according to standards:
 * - Code compiles/runs
 * - Tests were added if code was written
 * - Documentation was updated
 * - No obvious issues introduced
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

class SubagentWorkValidator {
    constructor(projectDir, transcriptPath = null) {
        this.projectDir = projectDir;
        this.transcriptPath = transcriptPath;
        this.issues = [];
        this.suggestions = [];
    }

    analyzeTranscript() {
        if (!this.transcriptPath || !fs.existsSync(this.transcriptPath)) {
            return {};
        }

        try {
            const content = fs.readFileSync(this.transcriptPath, 'utf8');
            
            // Look for indicators of incomplete work
            const indicators = {
                errors: (content.match(/error|Error|ERROR/g) || []).length,
                warnings: (content.match(/warning|Warning|WARNING/g) || []).length,
                todos: (content.match(/TODO|FIXME|XXX|HACK/g) || []).length,
                skipped: (content.match(/skip|Skip|SKIP|defer|Defer|DEFER/g) || []).length,
                failedTests: (content.match(/test.*fail|fail.*test|FAIL/gi) || []).length,
            };
            
            return indicators;
        } catch {
            return {};
        }
    }

    checkSyntaxErrors() {
        try {
            // Get recently modified files (within last 5 minutes)
            const recentFiles = execSync(
                `find "${this.projectDir}" -type f -mmin -5 2>/dev/null`,
                { encoding: 'utf8' }
            ).trim().split('\n').filter(Boolean);

            const filesWithErrors = [];

            for (const file of recentFiles) {
                // JavaScript/TypeScript syntax check
                if (file.endsWith('.js') || file.endsWith('.jsx')) {
                    try {
                        execSync(`node --check "${file}" 2>/dev/null`);
                    } catch {
                        filesWithErrors.push(path.basename(file));
                    }
                }
                
                // TypeScript check
                if (file.endsWith('.ts') || file.endsWith('.tsx')) {
                    // Check if TypeScript is available
                    try {
                        execSync('which tsc', { stdio: 'ignore' });
                        execSync(`tsc --noEmit "${file}" 2>/dev/null`);
                    } catch {
                        // Only report if tsc is available
                        if (fs.existsSync(path.join(this.projectDir, 'node_modules/typescript'))) {
                            filesWithErrors.push(path.basename(file));
                        }
                    }
                }
                
                // JSON syntax check
                if (file.endsWith('.json')) {
                    try {
                        JSON.parse(fs.readFileSync(file, 'utf8'));
                    } catch {
                        filesWithErrors.push(path.basename(file));
                    }
                }
            }

            if (filesWithErrors.length) {
                this.issues.push(`Syntax errors in: ${filesWithErrors.slice(0, 3).join(', ')}`);
                return false;
            }

            return true;
        } catch {
            return true; // Don't block if we can't check
        }
    }

    checkTestCoverage() {
        try {
            // Get files modified in last 5 minutes
            const modifiedFiles = execSync(
                `find "${this.projectDir}" -type f \\( -name "*.js" -o -name "*.jsx" -o -name "*.ts" -o -name "*.tsx" \\) -mmin -5 2>/dev/null`,
                { encoding: 'utf8' }
            ).trim().split('\n').filter(Boolean);

            if (!modifiedFiles.length) {
                return true;
            }

            const modifiedCodeFiles = [];
            const modifiedTestFiles = [];

            for (const file of modifiedFiles) {
                if (/\.test\.|\.spec\.|__tests__|test_/.test(file)) {
                    modifiedTestFiles.push(file);
                } else {
                    modifiedCodeFiles.push(file);
                }
            }

            // If code was modified but no tests, suggest adding tests
            if (modifiedCodeFiles.length && !modifiedTestFiles.length) {
                // Check if any of the modified files are significant (not just config)
                const significantFiles = modifiedCodeFiles.filter(f => 
                    !f.includes('config') && 
                    !f.includes('.d.ts') &&
                    !f.endsWith('package.json')
                );
                
                if (significantFiles.length) {
                    this.suggestions.push('Consider adding tests for the new code');
                }
            }

            return true; // Don't block, just suggest
        } catch {
            return true;
        }
    }

    checkDocumentation() {
        try {
            // Check if any significant code files were changed
            const codeFiles = execSync(
                `find "${this.projectDir}" -type f \\( -name "*.js" -o -name "*.jsx" -o -name "*.ts" -o -name "*.tsx" \\) -mmin -5 2>/dev/null`,
                { encoding: 'utf8' }
            ).trim().split('\n').filter(Boolean);

            const codeModified = codeFiles.length > 0;

            // Check if any docs were modified
            const docFiles = execSync(
                `find "${this.projectDir}" -type f \\( -name "*.md" -o -name "*.mdx" -o -path "*/docs/*" \\) -mmin -5 2>/dev/null`,
                { encoding: 'utf8' }
            ).trim().split('\n').filter(Boolean);

            const docsModified = docFiles.length > 0;

            if (codeModified && !docsModified) {
                // Check if the changes were significant
                try {
                    const diffStat = execSync('git diff --stat', {
                        encoding: 'utf8',
                        cwd: this.projectDir
                    });
                    
                    const insertions = diffStat.match(/(\d+) insertion/);
                    const totalInsertions = insertions ? parseInt(insertions[1]) : 0;
                    
                    if (totalInsertions > 20) {
                        this.suggestions.push('Documentation may need updating for these changes');
                    }
                } catch {}
            }

            // Check for missing JSDoc in new functions
            for (const file of codeFiles.slice(0, 3)) {
                try {
                    const content = fs.readFileSync(file, 'utf8');
                    
                    // Check for exported functions without JSDoc
                    const exportedFunctions = content.match(/export\s+(async\s+)?function\s+\w+/g) || [];
                    const jsdocComments = content.match(/\/\*\*[\s\S]*?\*\//g) || [];
                    
                    if (exportedFunctions.length > jsdocComments.length) {
                        this.suggestions.push(`Some exported functions lack JSDoc in ${path.basename(file)}`);
                        break;
                    }
                } catch {}
            }

            return true; // Don't block on documentation
        } catch {
            return true;
        }
    }

    checkImports() {
        try {
            // Check JavaScript/TypeScript files
            const jsFiles = execSync(
                `find "${this.projectDir}" -type f \\( -name "*.js" -o -name "*.jsx" -o -name "*.ts" -o -name "*.tsx" \\) -mmin -5 2>/dev/null`,
                { encoding: 'utf8' }
            ).trim().split('\n').filter(Boolean);

            for (const file of jsFiles) {
                if (!fs.existsSync(file)) continue;
                
                try {
                    const content = fs.readFileSync(file, 'utf8');
                    
                    // Check for missing imports (using undefined variables)
                    // This is a simple heuristic check
                    const imports = new Set();
                    const importMatches = content.matchAll(/import\s+(?:{[^}]+}|\w+|\*\s+as\s+\w+)\s+from/g);
                    for (const match of importMatches) {
                        const importText = match[0];
                        // Extract imported names
                        const names = importText.match(/\w+/g);
                        if (names) {
                            names.forEach(name => imports.add(name));
                        }
                    }
                    
                    // Check for duplicate imports
                    const importLines = content.match(/^import\s+.*$/gm) || [];
                    const importSources = importLines.map(line => {
                        const match = line.match(/from\s+['"](.*)['"]/);
                        return match ? match[1] : null;
                    }).filter(Boolean);
                    
                    const duplicates = importSources.filter((item, index) => 
                        importSources.indexOf(item) !== index
                    );
                    
                    if (duplicates.length) {
                        this.suggestions.push(`Duplicate imports in ${path.basename(file)}`);
                    }
                    
                    // Check for unused imports (basic check)
                    const unusedImports = [];
                    for (const imp of imports) {
                        if (imp === 'import' || imp === 'from' || imp === 'as') continue;
                        // Check if the import is used in the file (excluding the import line)
                        const regex = new RegExp(`\\b${imp}\\b`, 'g');
                        const matches = content.match(regex) || [];
                        if (matches.length <= 1) { // Only appears in import statement
                            unusedImports.push(imp);
                        }
                    }
                    
                    if (unusedImports.length > 3) {
                        this.suggestions.push(`Multiple unused imports in ${path.basename(file)}`);
                    }
                } catch {}
            }

            return true; // Don't block on import issues
        } catch {
            return true;
        }
    }

    checkPackageJson() {
        // Check if package.json was modified
        const packageJsonPath = path.join(this.projectDir, 'package.json');
        
        try {
            const stats = fs.statSync(packageJsonPath);
            const modifiedRecently = (Date.now() - stats.mtimeMs) < 5 * 60 * 1000; // 5 minutes
            
            if (modifiedRecently) {
                // Validate package.json
                try {
                    const content = fs.readFileSync(packageJsonPath, 'utf8');
                    JSON.parse(content); // Will throw if invalid
                    
                    // Check for lock file update
                    const hasNpmLock = fs.existsSync(path.join(this.projectDir, 'package-lock.json'));
                    const hasYarnLock = fs.existsSync(path.join(this.projectDir, 'yarn.lock'));
                    const hasPnpmLock = fs.existsSync(path.join(this.projectDir, 'pnpm-lock.yaml'));
                    const hasBunLock = fs.existsSync(path.join(this.projectDir, 'bun.lockb'));
                    
                    if (!hasNpmLock && !hasYarnLock && !hasPnpmLock && !hasBunLock) {
                        this.suggestions.push('package.json modified but no lock file found');
                    } else {
                        // Check if lock file is older than package.json
                        const lockFiles = [];
                        if (hasNpmLock) lockFiles.push('package-lock.json');
                        if (hasYarnLock) lockFiles.push('yarn.lock');
                        if (hasPnpmLock) lockFiles.push('pnpm-lock.yaml');
                        if (hasBunLock) lockFiles.push('bun.lockb');
                        
                        for (const lockFile of lockFiles) {
                            const lockPath = path.join(this.projectDir, lockFile);
                            const lockStats = fs.statSync(lockPath);
                            if (lockStats.mtimeMs < stats.mtimeMs) {
                                this.suggestions.push(`${lockFile} may need updating after package.json changes`);
                                break;
                            }
                        }
                    }
                } catch (error) {
                    this.issues.push('package.json is invalid JSON');
                }
            }
        } catch {}
        
        return true;
    }

    validate() {
        // Analyze transcript if available
        const transcriptIndicators = this.analyzeTranscript();
        
        // Check for serious issues
        this.checkSyntaxErrors();
        
        // Check for quality issues
        this.checkTestCoverage();
        this.checkDocumentation();
        this.checkImports();
        this.checkPackageJson();
        
        // Analyze transcript indicators
        if (transcriptIndicators.errors && transcriptIndicators.errors > 5) {
            this.issues.push('Multiple errors detected in subagent work');
        }
        if (transcriptIndicators.failedTests && transcriptIndicators.failedTests > 0) {
            this.issues.push('Tests appear to be failing');
        }
        if (transcriptIndicators.todos && transcriptIndicators.todos > 3) {
            this.suggestions.push('Several TODOs were left in the code');
        }
        
        // Determine if we should block
        if (this.issues.length > 0) {
            let reason = 'Subagent work validation failed:\n';
            reason += this.issues.map(issue => `❌ ${issue}`).join('\n');
            
            if (this.suggestions.length) {
                reason += '\n\nSuggestions:\n';
                reason += this.suggestions.map(suggestion => `💡 ${suggestion}`).join('\n');
            }
            
            return {
                decision: 'block',
                reason: reason + '\n\nPlease address these issues.'
            };
        } else if (this.suggestions.length) {
            // Just provide suggestions, don't block
            const feedback = 'Subagent work complete. Suggestions:\n' +
                           this.suggestions.map(suggestion => `💡 ${suggestion}`).join('\n');
            
            console.error(feedback);
            return {};
        } else {
            console.error('✅ Subagent work validated successfully!');
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
        
        // Handle both SubagentStop and PostToolUse(Task)
        const hookEvent = data.hook_event_name || '';
        
        if (hookEvent === 'PostToolUse') {
            const toolName = data.tool_name || '';
            if (toolName !== 'Task') {
                process.exit(0);
            }
        }
        
        const projectDir = data.cwd || process.cwd();
        const transcriptPath = data.transcript_path;
        
        const validator = new SubagentWorkValidator(projectDir, transcriptPath);
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