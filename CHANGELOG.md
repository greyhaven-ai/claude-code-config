# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.0] - 2025-10-20

### Added
- **Claude Skills support**: Added three production-ready Skills for automatic code assistance
  - `grey-haven-code-style`: Apply Grey Haven coding standards (TypeScript, React, Python)
  - `grey-haven-commit-format`: Format commit messages using Conventional Commits
  - `grey-haven-pr-template`: Generate comprehensive pull request descriptions
- **Skills plugin package**: New `grey-haven-skills` plugin in marketplace
- **CLI Skills management**:
  - `claude-config install-skills`: Install Skills to `~/.claude/skills/`
  - `claude-config list-skills`: Show available Skills
- **Doctor diagnostic**: Added Skills installation check to `claude-config doctor`
- **Documentation**:
  - [SKILLS_ANALYSIS_AND_INTEGRATION.md](.claude/research/SKILLS_ANALYSIS_AND_INTEGRATION.md) - Comprehensive Skills research and integration strategy
  - [grey-haven-plugins/grey-haven-skills/README.md](grey-haven-plugins/grey-haven-skills/README.md) - Skills package documentation
  - [.claude/skills/README.md](.claude/skills/README.md) - Skills directory guide

### Changed
- Updated CLI version to 2.1.0
- Updated CLI description to include Skills
- Enhanced help text with Skills examples
- Updated package.json keywords to include "skills" and "code-quality"
- Updated README.md with Skills information (pending)

### Package
- Package size: ~104 KB (includes Skills)
- New files included:
  - `.claude/skills/` directory
  - `grey-haven-plugins/grey-haven-skills/` plugin package

## [2.0.0] - 2025-10-20

### Breaking Changes
- **npm/Homebrew scope reduction**: No longer distributes agents and commands
- **Plugin-first architecture**: Agents and commands now distributed via Git + plugin marketplace
- Package size reduced 75%: from ~2 MB to 104.6 KB

### Added
- **Hooks and configuration focus**: npm package now focuses on hooks and setup
- **CLI commands**:
  - `claude-config install-hooks`: Install hooks to `~/.claude/hooks/`
  - `claude-config list-hooks`: Show available hooks
  - `claude-config init`: Initialize `.claude/` directory
  - `claude-config backup-settings`: Backup user settings
  - `claude-config restore-settings`: Restore settings from backup
  - `claude-config doctor`: Diagnose installation and configuration
  - `claude-config self-update`: Update to latest version via npm
- **Documentation**:
  - [V2_ARCHITECTURE_PLAN.md](.claude/V2_ARCHITECTURE_PLAN.md) - Complete v2.0.0 architecture
  - [MIGRATION_V2.md](MIGRATION_V2.md) - Migration guide from v1.x to v2.0.0

### Removed
- Agents (now in `grey-haven-plugins/` packages)
- Commands (now in `grey-haven-plugins/` packages)
- Presets
- Agent/command management from CLI

### Changed
- **Python CLI refactored**: Reduced from 1,483 to 520 lines (-65%)
- **Package structure**: Only hooks and configuration in npm package
- **Distribution model**:
  - Hooks/config via npm/Homebrew
  - Plugins via Git + marketplace
  - Skills via plugins (v2.1.0+)

### Documentation
- Updated README.md for v2.0.0 architecture
- Updated CLAUDE.md with development guidelines
- Organized archive/ and research/ directories
- Cleaned up root directory documentation

## [1.2.8] - 2025-10-XX

### Fixed
- Hook JSON validation fixes
- Python type hinting and output formatting

## [1.2.7] - 2025-10-XX

### Fixed
- Corrected decision field values in hooks to use 'approve' instead of 'allow'

---

## Release Notes

### v2.1.0 - Skills Support

This release adds comprehensive Skills support, enabling Claude to automatically apply Grey Haven coding standards, format commit messages, and generate PR descriptions.

**Key Features**:
- 3 production-ready Skills
- Plugin marketplace integration
- CLI management commands
- Automatic invocation (no manual triggers needed)

**Installation**:
```bash
npm install -g @greyhaven/claude-code-config@2.1.0
claude-config install-skills
```

Or via plugin marketplace:
```
/plugin install grey-haven-skills@grey-haven-plugins
```

### v2.0.0 - Hooks and Configuration Focus

Major architectural redesign focused on hooks and configuration management. Agents and commands moved to plugin marketplace for better distribution and flexibility.

**Installation**:
```bash
npm install -g @greyhaven/claude-code-config@2.0.0
claude-config install-hooks
```

**Migration**: See [MIGRATION_V2.md](MIGRATION_V2.md) for complete upgrade guide.

---

[2.1.0]: https://github.com/greyhaven-ai/grey-haven-claude-code-config/compare/v2.0.0...v2.1.0
[2.0.0]: https://github.com/greyhaven-ai/grey-haven-claude-code-config/compare/v1.2.8...v2.0.0
[1.2.8]: https://github.com/greyhaven-ai/grey-haven-claude-code-config/compare/v1.2.7...v1.2.8
[1.2.7]: https://github.com/greyhaven-ai/grey-haven-claude-code-config/releases/tag/v1.2.7
