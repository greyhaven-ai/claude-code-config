#!/usr/bin/env node

/**
 * Post-installation script for claude-config
 * Sets up necessary permissions and displays installation message
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

// Colors for console output
const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\xariable[34m',
  cyan: '\x1b[36m'
};

console.log(`
${colors.cyan}${colors.bright}═══════════════════════════════════════════════════════════${colors.reset}
${colors.cyan}${colors.bright}     Claude Config - Installation Complete! 🎉              ${colors.reset}
${colors.cyan}${colors.bright}═══════════════════════════════════════════════════════════${colors.reset}

${colors.green}Successfully installed claude-config!${colors.reset}

${colors.yellow}Quick Start:${colors.reset}
  ${colors.bright}claude-config --help${colors.reset}              Show all commands
  ${colors.bright}claude-config init${colors.reset}                Initialize in current directory
  ${colors.bright}claude-config list-presets${colors.reset}        Show 23 available presets
  ${colors.bright}claude-config preset recommended${colors.reset}  Apply recommended preset

${colors.yellow}Available Resources:${colors.reset}
  • 23 preset configurations
  • 22 slash commands  
  • 19 specialized agents
  • 20 statusline options

${colors.yellow}Documentation:${colors.reset}
  https://github.com/grey-haven/grey-haven-claude-config

${colors.yellow}Updates:${colors.reset}
  ${colors.bright}claude-config self-update${colors.reset}         Update to latest version
  ${colors.bright}npm update -g @grey-haven/claude-config${colors.reset}

${colors.cyan}═══════════════════════════════════════════════════════════${colors.reset}
`);

// Make the Python script executable
try {
  const scriptPath = path.join(__dirname, '..', 'claude-config');
  if (fs.existsSync(scriptPath)) {
    fs.chmodSync(scriptPath, '755');
  }
  
  const binPath = path.join(__dirname, '..', 'bin', 'claude-config.js');
  if (fs.existsSync(binPath)) {
    fs.chmodSync(binPath, '755');
  }
} catch (err) {
  // Ignore permission errors on Windows
  if (process.platform !== 'win32') {
    console.warn('Warning: Could not set execute permissions:', err.message);
  }
}