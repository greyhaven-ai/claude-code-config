# Plugin Migration Tool for Claude Code

A Python tool for validating, generating, and analyzing Claude Code plugin structures, built using strict Test-Driven Development (TDD) methodology.

## Features

- **Manifest Validation**: Validate `marketplace.json` and `plugin.json` manifests
- **Structure Generation**: Create proper plugin marketplace directory structures
- **Directory Analysis**: Analyze existing `.claude/` directories for commands, agents, and hooks
- **High Test Coverage**: 99% test coverage using pytest

## Installation

1. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install pytest pytest-cov
```

## Usage

### Command Line Interface

```bash
# Analyze .claude directory structure
python main.py analyze [path]

# Validate marketplace.json
python main.py validate-marketplace <file>

# Validate plugin.json
python main.py validate-plugin <file>

# Generate plugin marketplace structure
python main.py generate <path> <name>
```

### Examples

1. **Analyze current directory**:
```bash
python main.py analyze .
```

2. **Generate a new marketplace**:
```bash
python main.py generate ./my-marketplace "My Plugin Collection"
```

3. **Validate manifests**:
```bash
python main.py validate-marketplace ./marketplace/.claude-plugin/marketplace.json
python main.py validate-plugin ./plugins/my-plugin/plugin.json
```

## Project Structure

```
tools/
├── plugin_generator/
│   ├── __init__.py         # Package initialization
│   ├── validators.py       # Manifest validators
│   ├── generator.py        # Structure generator
│   └── analyzer.py         # .claude/ analyzer
├── tests/
│   ├── __init__.py
│   ├── test_validators.py  # Validator tests
│   ├── test_generator.py   # Generator tests
│   └── test_analyzer.py    # Analyzer tests
├── main.py                 # CLI entry point
└── README.md              # This file
```

## Validation Rules

### marketplace.json

Required fields:
- `name`: Marketplace name
- `owner`: Object with `name` field
- `plugins`: Array of plugin objects

Each plugin must have:
- `name`: Plugin identifier
- `source`: Path to plugin
- `description`: Plugin description

### plugin.json

Required fields:
- `name`: Plugin name
- `description`: Plugin description
- `version`: Semantic version (e.g., "1.0.0")
- `author`: Object with `name` field

Optional fields:
- `keywords`: Array of strings
- `license`: License string

## Generated Structure

```
marketplace/
├── .claude-plugin/
│   └── marketplace.json    # Marketplace manifest
└── plugins/
    └── sample-plugin/
        └── plugin.json     # Plugin manifest
```

## Development

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=plugin_generator --cov-report=term-missing

# Generate HTML coverage report
pytest tests/ --cov=plugin_generator --cov-report=html
```

### TDD Workflow

This project was built using strict TDD principles:

1. **Red Phase**: Write failing tests first
2. **Green Phase**: Write minimal code to pass tests
3. **Refactor Phase**: Improve code while keeping tests green

### Test Coverage

Current coverage: **99%**

The only uncovered lines are edge cases in the analyzer for empty category handling.

## Type Hints

All functions include Python 3.13+ type hints for better IDE support and code clarity.

## License

MIT License - Copyright (c) 2025 Grey Haven Studio