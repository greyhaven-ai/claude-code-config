#!/usr/bin/env node

/**
 * Coverage Gap Finder Hook for JavaScript/TypeScript
 * ===================================================
 * Type: Stop
 * Description: Shows uncovered code paths and suggests test cases
 *
 * Works with: Jest, Vitest, NYC, C8 coverage reports
 */

const fs = require('fs');
const path = require('path');
// const { execSync } = require('child_process'); // Not currently used

// Read hook data from stdin
let inputData = '';
process.stdin.on('data', chunk => inputData += chunk);
process.stdin.on('end', () => {
    try {
        const data = JSON.parse(inputData);
        analyzeCoverage(data);
    } catch {
        // Don't block on error
        process.exit(0);
    }
});

function analyzeCoverage(data) {
    const changedFiles = data.changed_files || [];
    const projectDir = data.project_dir || process.cwd();

    if (changedFiles.length === 0) {
        process.exit(0);
    }

    // Look for coverage reports
    const coverageFiles = findCoverageFiles(projectDir);

    console.log('=' + '='.repeat(59));
    console.log('📊 Coverage Gap Analysis (JavaScript/TypeScript)');
    console.log('=' + '='.repeat(59));

    if (coverageFiles.length > 0) {
        console.log('\n📁 Found coverage data:');
        coverageFiles.slice(0, 3).forEach(file => {
            console.log(`   • ${path.relative(projectDir, file)}`);
        });
    }

    // Try to generate fresh coverage for changed files
    const jsFiles = changedFiles.filter(f =>
        (f.endsWith('.js') || f.endsWith('.jsx') ||
         f.endsWith('.ts') || f.endsWith('.tsx')) &&
        !f.includes('.test.') && !f.includes('.spec.')
    );

    if (jsFiles.length === 0) {
        process.exit(0);
    }

    // Analyze coverage for each file
    const coverageData = analyzeCoverageData(projectDir, jsFiles);

    if (coverageData.length > 0) {
        console.log('\n📄 Coverage Analysis:');

        for (const fileData of coverageData) {
            const emoji = getCoverageEmoji(fileData.percentage);
            console.log(`\n${emoji} ${path.basename(fileData.file)}: ${fileData.percentage}% coverage`);

            if (fileData.uncoveredLines.length > 0) {
                console.log('   ⚠️  Uncovered lines:');
                fileData.uncoveredLines.slice(0, 5).forEach(line => {
                    console.log(`      Line ${line}`);
                });

                if (fileData.uncoveredLines.length > 5) {
                    console.log(`      ... and ${fileData.uncoveredLines.length - 5} more`);
                }
            }

            if (fileData.suggestions.length > 0) {
                console.log('   💡 Test suggestions:');
                fileData.suggestions.forEach(suggestion => {
                    console.log(`      • ${suggestion}`);
                });
            }
        }
    }

    // Generate test stub example
    if (jsFiles.length > 0) {
        const testStub = generateTestStub(jsFiles[0], projectDir);

        console.log('\n' + '='.repeat(60));
        console.log('🧪 Example Test Stub:');
        console.log('='.repeat(60));
        console.log(testStub);
    }

    console.log('\n💡 Coverage Improvement Tips:');
    console.log('   • Focus on error handling paths (often missed)');
    console.log('   • Test edge cases and boundary conditions');
    console.log('   • Add tests for new functions before committing');
    console.log('   • Aim for 80% coverage minimum');

    console.log('\n📚 Commands to check coverage:');
    console.log('   Jest: npm test -- --coverage');
    console.log('   Vitest: vitest run --coverage');
    console.log('   NYC: nyc npm test');

    console.log('=' + '='.repeat(59));
    process.exit(0);
}

function findCoverageFiles(projectDir) {
    const coveragePatterns = [
        'coverage/lcov.info',
        'coverage/coverage-final.json',
        'coverage/clover.xml',
        '.nyc_output/processinfo/index.json',
        'coverage-report/index.html'
    ];

    const found = [];
    for (const pattern of coveragePatterns) {
        const fullPath = path.join(projectDir, pattern);
        if (fs.existsSync(fullPath)) {
            found.push(fullPath);
        }
    }

    return found;
}

function analyzeCoverageData(projectDir, files) {
    const results = [];

    // Try to read coverage-final.json (Jest/NYC format)
    const coverageJsonPath = path.join(projectDir, 'coverage', 'coverage-final.json');

    if (fs.existsSync(coverageJsonPath)) {
        try {
            const coverage = JSON.parse(fs.readFileSync(coverageJsonPath, 'utf8'));

            for (const file of files) {
                const absolutePath = path.resolve(projectDir, file);
                const coverageData = coverage[absolutePath];

                if (coverageData) {
                    const statements = coverageData.s || {};
                    const branches = coverageData.b || {};
                    const functions = coverageData.f || {};

                    // Calculate coverage percentage
                    const stmtTotal = Object.keys(statements).length;
                    const stmtCovered = Object.values(statements).filter(v => v > 0).length;
                    const percentage = stmtTotal > 0 ? Math.round((stmtCovered / stmtTotal) * 100) : 0;

                    // Find uncovered lines
                    const uncoveredLines = [];
                    const statementMap = coverageData.statementMap || {};

                    for (const [key, count] of Object.entries(statements)) {
                        if (count === 0 && statementMap[key]) {
                            uncoveredLines.push(statementMap[key].start.line);
                        }
                    }

                    // Generate suggestions
                    const suggestions = generateTestSuggestions(file, {
                        uncoveredStatements: stmtTotal - stmtCovered,
                        uncoveredBranches: Object.values(branches).filter(b => b[0] === 0 || b[1] === 0).length,
                        uncoveredFunctions: Object.values(functions).filter(v => v === 0).length
                    });

                    results.push({
                        file,
                        percentage,
                        uncoveredLines: uncoveredLines.slice(0, 10),
                        suggestions
                    });
                }
            }
        } catch {
            // Coverage file might be malformed
        }
    }

    // If no coverage data, provide generic analysis
    if (results.length === 0) {
        for (const file of files.slice(0, 3)) {
            results.push({
                file,
                percentage: 0,
                uncoveredLines: [],
                suggestions: [
                    'Run coverage analysis to identify gaps',
                    'Add unit tests for exported functions',
                    'Test error handling scenarios'
                ]
            });
        }
    }

    return results;
}

function generateTestSuggestions(file, coverage) {
    const suggestions = [];

    if (coverage.uncoveredFunctions > 0) {
        suggestions.push(`Test ${coverage.uncoveredFunctions} untested function(s)`);
    }

    if (coverage.uncoveredBranches > 0) {
        suggestions.push(`Cover ${coverage.uncoveredBranches} untested branch(es) (if/else, switch)`);
    }

    if (coverage.uncoveredStatements > 5) {
        suggestions.push('Add tests for error handling paths');
    }

    // File-specific suggestions
    if (file.includes('api') || file.includes('service')) {
        suggestions.push('Test API error responses');
        suggestions.push('Mock external dependencies');
    }

    if (file.includes('component')) {
        suggestions.push('Test component edge cases');
        suggestions.push('Test user interactions');
    }

    if (file.includes('util') || file.includes('helper')) {
        suggestions.push('Test with various input types');
        suggestions.push('Test boundary conditions');
    }

    return suggestions.slice(0, 3);
}

function generateTestStub(file) {
    const basename = path.basename(file, path.extname(file));
    const isTypeScript = file.endsWith('.ts') || file.endsWith('.tsx');
    const testExt = isTypeScript ? '.test.ts' : '.test.js';

    const stub = `// ${basename}${testExt}

${isTypeScript ? "import { describe, it, expect, beforeEach, vi } from 'vitest';" : "const { describe, it, expect, beforeEach } = require('@jest/globals');"}
import { ${basename} } from './${basename}';

describe('${basename}', () => {
  beforeEach(() => {
    // Setup test environment
    ${isTypeScript ? 'vi.clearAllMocks();' : 'jest.clearAllMocks();'}
  });

  describe('Happy Path', () => {
    it('should handle valid input correctly', () => {
      // TODO: Implement test
      expect(true).toBe(true);
    });
  });

  describe('Edge Cases', () => {
    it('should handle null/undefined gracefully', () => {
      // TODO: Test with null and undefined
      expect(true).toBe(true);
    });

    it('should handle empty input', () => {
      // TODO: Test with empty arrays, strings, objects
      expect(true).toBe(true);
    });
  });

  describe('Error Scenarios', () => {
    it('should throw error for invalid input', () => {
      // TODO: Test error conditions
      expect(() => {
        // Invalid operation
      }).toThrow();
    });
  });
});`;

    return stub;
}

function getCoverageEmoji(percentage) {
    if (percentage >= 80) return '🟢';
    if (percentage >= 60) return '🟡';
    return '🔴';
}