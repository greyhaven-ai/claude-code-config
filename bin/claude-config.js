#!/usr/bin/env node

/**
 * Claude Config CLI Wrapper
 * This Node.js wrapper executes the Python CLI with proper environment setup
 */

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');
const os = require('os');

// Determine the installation directory
const installDir = path.join(__dirname, '..');
const claudeConfigScript = path.join(installDir, 'claude-config');

// Check if Python is available
function checkPython() {
  const pythonCommands = ['python3', 'python'];
  
  for (const cmd of pythonCommands) {
    try {
      const result = require('child_process').execSync(`${cmd} --version`, { 
        stdio: 'pipe' 
      }).toString();
      
      if (result.includes('Python 3')) {
        return cmd;
      }
    } catch (e) {
      // Continue to next command
    }
  }
  
  console.error('Error: Python 3 is required but not found.');
  console.error('Please install Python 3: https://www.python.org/downloads/');
  process.exit(1);
}

// Check if the Python script exists
if (!fs.existsSync(claudeConfigScript)) {
  console.error(`Error: Claude Config script not found at ${claudeConfigScript}`);
  console.error('The installation may be corrupted. Please reinstall:');
  console.error('  npm uninstall -g @grey-haven/claude-config');
  console.error('  npm install -g @grey-haven/claude-config');
  process.exit(1);
}

// Find Python executable
const pythonCmd = checkPython();

// Set up environment variables
const env = Object.assign({}, process.env, {
  CLAUDE_CONFIG_GLOBAL: '1',
  CLAUDE_CONFIG_HOME: installDir,
  // Preserve color output
  FORCE_COLOR: '1'
});

// Get command line arguments (skip first two: node and script path)
const args = process.argv.slice(2);

// Special handling for update command
if (args[0] === 'self-update') {
  console.log('Updating claude-config from npm...');
  const npm = spawn('npm', ['update', '-g', '@greyhaven/claude-code-config'], {
    stdio: 'inherit',
    shell: true
  });
  
  npm.on('exit', (code) => {
    if (code === 0) {
      console.log('Successfully updated claude-config!');
    } else {
      console.error('Update failed. Please try manually:');
      console.error('  npm update -g @greyhaven/claude-code-config');
    }
    process.exit(code);
  });
  return;
}

// Execute the Python script with all arguments
const child = spawn(pythonCmd, [claudeConfigScript, ...args], {
  env: env,
  stdio: 'inherit',
  shell: false
});

// Handle errors
child.on('error', (err) => {
  console.error('Failed to execute claude-config:', err.message);
  process.exit(1);
});

// Pass through the exit code
child.on('exit', (code) => {
  process.exit(code || 0);
});