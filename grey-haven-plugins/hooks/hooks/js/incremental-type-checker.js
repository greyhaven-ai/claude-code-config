#!/usr/bin/env node

/**
 * Incremental Type Checker Hook for JavaScript/TypeScript
 * ========================================================
 * Type: PostToolUse (Edit/Write)
 * Description: Type checks only changed TypeScript files
 *
 * Supports: TypeScript (tsc), Flow
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Read hook data from stdin
let inputData = '';
process.stdin.on('data', chunk => inputData += chunk);
process.stdin.on('end', () => {
    try {
        const data = JSON.parse(inputData);
        runTypeCheck(data);
    } catch {
        // Don't block on error
        process.exit(0);
    }
});

function runTypeCheck(data) {
    const changedFiles = data.changed_files || [];
    const projectDir = data.project_dir || process.cwd();

    // Filter for TypeScript files
    const tsFiles = changedFiles.filter(f =>
        f.endsWith('.ts') || f.endsWith('.tsx') ||
        f.endsWith('.mts') || f.endsWith('.cts')
    );

    if (tsFiles.length === 0) {
        process.exit(0);
    }

    // Check for TypeScript configuration
    const tsconfigPath = path.join(projectDir, 'tsconfig.json');
    const hasTypeScript = fs.existsSync(tsconfigPath);

    // Check for Flow
    const flowConfigPath = path.join(projectDir, '.flowconfig');
    const hasFlow = fs.existsSync(flowConfigPath);

    if (!hasTypeScript && !hasFlow) {
        process.exit(0);
    }

    console.log('=' + '='.repeat(59));
    console.log('🔍 Incremental Type Checker (JavaScript/TypeScript)');
    console.log('=' + '='.repeat(59));

    let hasErrors = false;

    // TypeScript checking
    if (hasTypeScript) {
        console.log('\n📘 TypeScript Check');
        console.log(`Checking ${tsFiles.length} file(s)...`);

        try {
            // Use tsc with noEmit for type checking only
            const command = `npx tsc --noEmit --incremental ${tsFiles.join(' ')}`;

            execSync(command, {
                cwd: projectDir,
                encoding: 'utf8'
            });

            console.log('✅ No TypeScript errors found');
        } catch (error) {
            hasErrors = true;
            console.log('❌ TypeScript errors found:');

            // Parse and display errors
            const errorOutput = error.stdout || error.message;
            const lines = errorOutput.split('\n');

            for (const line of lines.slice(0, 10)) { // Limit output
                if (line.includes('error TS')) {
                    console.log(`  ${line}`);
                }
            }

            if (lines.length > 10) {
                console.log(`  ... and ${lines.length - 10} more errors`);
            }
        }
    }

    // Flow checking
    if (hasFlow) {
        const flowFiles = changedFiles.filter(f =>
            f.endsWith('.js') || f.endsWith('.jsx')
        );

        if (flowFiles.length > 0) {
            console.log('\n🌊 Flow Check');
            console.log(`Checking ${flowFiles.length} file(s)...`);

            try {
                const command = `npx flow check ${flowFiles.join(' ')}`;

                execSync(command, {
                    cwd: projectDir,
                    encoding: 'utf8'
                });

                console.log('✅ No Flow errors found');
            } catch (error) {
                hasErrors = true;
                console.log('❌ Flow errors found');
                console.log(error.stdout || error.message);
            }
        }
    }

    // Suggestions
    if (hasErrors) {
        console.log('\n💡 Tips:');
        console.log('  • Fix type errors before committing');
        console.log('  • Use strict mode for better type safety');
        console.log('  • Consider adding type annotations to untyped code');
        console.log('  • Run full type check: npm run type-check');
    }

    console.log('=' + '='.repeat(59));
    process.exit(0);
}