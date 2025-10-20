#!/usr/bin/env node

/**
 * Smart Test Runner Hook for JavaScript/TypeScript
 * =================================================
 * Type: PostToolUse (Edit/Write)
 * Description: Runs only affected tests based on changed files
 *
 * Supports: Jest, Vitest, Mocha, Jasmine
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
        runAffectedTests(data);
    } catch {
        // Don't block on error
        process.exit(0);
    }
});

function runAffectedTests(data) {
    const changedFiles = data.changed_files || [];
    const projectDir = data.project_dir || process.cwd();

    if (changedFiles.length === 0) {
        process.exit(0);
    }

    // Detect test runner
    const packageJsonPath = path.join(projectDir, 'package.json');
    let testRunner = null;
    let testCommand = null;

    if (fs.existsSync(packageJsonPath)) {
        const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
        const scripts = packageJson.scripts || {};
        const deps = { ...packageJson.dependencies, ...packageJson.devDependencies };

        // Detect test runner from dependencies
        if (deps['vitest']) {
            testRunner = 'vitest';
            testCommand = 'vitest run';
        } else if (deps['jest']) {
            testRunner = 'jest';
            testCommand = 'jest';
        } else if (deps['mocha']) {
            testRunner = 'mocha';
            testCommand = 'mocha';
        } else if (deps['jasmine']) {
            testRunner = 'jasmine';
            testCommand = 'jasmine';
        }

        // Check for test script
        if (scripts.test) {
            testCommand = 'npm test';
        }
    }

    if (!testCommand) {
        process.exit(0);
    }

    // Find related test files
    const testFiles = [];

    for (const file of changedFiles) {
        if (file.includes('.test.') || file.includes('.spec.')) {
            testFiles.push(file);
        } else {
            // Find corresponding test file
            const basename = path.basename(file, path.extname(file));
            const dirname = path.dirname(file);

            const possibleTests = [
                path.join(dirname, `${basename}.test.js`),
                path.join(dirname, `${basename}.test.ts`),
                path.join(dirname, `${basename}.spec.js`),
                path.join(dirname, `${basename}.spec.ts`),
                path.join(dirname, '__tests__', `${basename}.test.js`),
                path.join(dirname, '__tests__', `${basename}.test.ts`),
            ];

            for (const testPath of possibleTests) {
                if (fs.existsSync(testPath)) {
                    testFiles.push(testPath);
                }
            }
        }
    }

    if (testFiles.length === 0) {
        process.exit(0);
    }

    // Output
    console.log('=' + '='.repeat(59));
    console.log('🧪 Smart Test Runner (JavaScript)');
    console.log('=' + '='.repeat(59));
    console.log(`\nTest Runner: ${testRunner}`);
    console.log(`Changed files: ${changedFiles.length}`);
    console.log(`Test files to run: ${testFiles.length}`);

    // Run tests based on runner
    try {
        let command;

        if (testRunner === 'jest') {
            command = `jest ${testFiles.join(' ')} --passWithNoTests`;
        } else if (testRunner === 'vitest') {
            command = `vitest run ${testFiles.join(' ')}`;
        } else if (testRunner === 'mocha') {
            command = `mocha ${testFiles.join(' ')}`;
        } else {
            command = testCommand;
        }

        console.log(`\nRunning: ${command}\n`);

        execSync(command, {
            cwd: projectDir,
            stdio: 'inherit'
        });

        console.log('\n✅ Tests passed!');
    } catch {
        console.log('\n❌ Tests failed!');
        console.log('Please fix the failing tests.');
    }

    console.log('=' + '='.repeat(59));
    process.exit(0);
}