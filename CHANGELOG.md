# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Plugins 2.1.0] - 2026-04-19

### Added
- **DDD + DRY discipline layering** across the TDD and code-review chain. Two lenses applied at specific phases — Domain-Driven Design at Red (model before you test), principled DRY at Refactor (deduplicate only same-concept repetition at ≥3 sites). Never displaces red-green-refactor; sharpens it at plan-review boundaries.
  - `core:tdd-python-implementer` and `core:tdd-typescript-implementer` (agents + skills): new "Domain-First Design" section, ubiquitous-language test-name enforcement, branded-type examples in TypeScript, primitive-obsession detection, DRY-with-discipline refactor rule. Skills bumped to 1.1.
  - `core:tdd-orchestrator`: new **Layer 0 "Domain Model Plan"** gate that blocks all Red tasks until a short plan naming entities/value objects/aggregates, classifying them, auditing primitive obsession, and drawing the domain/infrastructure boundary is approved. Plan-review criteria strengthened at Red/Green/Refactor. Task board grew from 6 to 7 layers. Skill bumped to 2.1.
  - `core:code-quality-analyzer` (agent + skill): two new workflow passes (Domain Lens, Duplication Lens) before cross-file analysis. Flags mechanical naming, primitive obsession, domain rules leaking into infrastructure, and premature DRY extractions. Skill bumped to 1.2.
- **`/audit-refs` command** and `plugin-auditor/scripts/cross_ref_lint.py` — a stdlib-only linter that scans every `SKILL.md`, agent, workflow, and reference doc for broken `skills:` auto-loads, missing "Related Agents" entries, and legacy `grey-haven-<name>` references. Filters directory names, repo names, markdown link targets, and deliberate counter-examples to keep the signal clean. Exit 1 on errors for CI gating.
- **`/release-plugins` command** and `plugin-auditor/scripts/bump_plugin_versions.py` — coordinates plugin releases: pre-flight cross-ref lint (blocks on dangling refs), lockstep version check, bumps all 8 `plugin.json` files, drafts a CHANGELOG entry from `git log`, previews before committing. Never auto-pushes.

### Fixed
- **Dangling cross-references eliminated.** The cross-ref linter surfaced 15 genuine issues on first run, all resolved:
  - 6 broken `skills:` auto-loads referencing phantom skills `security-practices`, `linear-workflow`, `observability-monitoring` (across `api-design-standards`, `pr-template`, `onboarding-coordination`, `code-quality-analysis`, `performance-optimization`, `incident-response`).
  - 3 "Related Agents" pointing at nonexistent agents (`security-analyzer`, `memory-profiler`, `observability-engineer`).
  - 6 phantom plugin-integration blocks in `incident-response/workflows/incident-response.md` and `data-quality/agents/data-validator.md` promising integrations with plugins that don't exist. Repo now lint-clean.

### Changed
- All plugin `version` fields bumped from `2.0.0` to `2.1.0` uniformly.

## [Plugins 2.0.0] - 2026-04-17

### Breaking Changes
- **Skill names no longer carry the `grey-haven-` prefix.** Invoke skills as `tdd-python` instead of `grey-haven-tdd-python`; the plugin already provides the namespace (`core:tdd-python`, etc.). All 32 `SKILL.md` files and their `skills:` cross-references were updated. Any external documentation or `CLAUDE.md` that invokes skills by full name must be updated.

### Fixed
- **`research:tech-docs-orchestrator`**: reconstructed from a corrupted concatenation that had two agents' content (and `name: tdd-python-implementer`) spliced together since the initial hooks commit. Now has correct frontmatter (`name: tech-docs-orchestrator`, `model: sonnet`, declared `tools`) and clean body.
- Stale cross-references to old `grey-haven-<name>` skills in `skill-creator/SKILL.md`, `skill-creator/scripts/init_skill.py` (was generating the deprecated template), `ontological-documentation/SKILL.md` (also removed nonexistent `authentication-patterns` ref), `suite-audit/SKILL.md`, `llm-project-development/references/INDEX.md`, `plugin-audit/examples/audit-report-example.md`, and top-level `README.md`.

### Added
- `maxTurns: 40` on `tdd-orchestrator`, `multi-agent-synthesis-orchestrator`, and `tech-docs-orchestrator` (v2.1.76 frontmatter field) — prevents runaway orchestration loops.
- `grey-haven-plugins/docs/DOCUMENTATION_STANDARDS.md` relocated from the plugins root.

### Changed
- All plugin `version` fields bumped to `2.0.0` uniformly (previously mixed: `1.0.0`, `1.1.0`, `1.7.0`).

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
