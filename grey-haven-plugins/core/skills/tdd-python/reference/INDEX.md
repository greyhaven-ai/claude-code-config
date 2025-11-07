# TDD Python Reference

Comprehensive reference materials for Python Test-Driven Development - pytest, unittest, mocking, coverage, and Python-specific testing patterns.

## Available References

### [pytest-guide.md](pytest-guide.md)
Complete pytest reference - fixtures, parametrize, marks, plugins, and configuration.

**When to use**: Modern Python projects, learning pytest patterns
**Covers**: Fixtures, parametrize, marks, plugins, conftest.py, pytest.ini
**Key Topics**: Dependency injection, test discovery, assertion introspection

---

### [unittest-guide.md](unittest-guide.md)
Comprehensive unittest reference - TestCase classes, assertions, setUp/tearDown, test discovery.

**When to use**: Legacy projects, corporate environments, no external dependencies
**Covers**: TestCase structure, assertion methods, test organization, discovery
**Key Topics**: Class-based testing, setUp/tearDown, unittest.main()

---

### [mocking-reference.md](mocking-reference.md)
Complete mocking guide - Mock, MagicMock, patch, side_effect, assert patterns.

**When to use**: Testing external dependencies, isolating units, verifying interactions
**Covers**: unittest.mock, pytest-mock, mocking strategies, anti-patterns
**Key Topics**: Mock vs stub vs spy, patching strategies, assertion methods

---

### [coverage-guide.md](coverage-guide.md)
Coverage analysis and interpretation - tools, metrics, thresholds, CI integration.

**When to use**: Measuring test effectiveness, finding gaps, enforcing quality gates
**Covers**: coverage.py, pytest-cov, branch coverage, HTML reports, exclusions
**Key Topics**: 80% line coverage target, critical path coverage, differential coverage

---

### [python-specific-testing.md](python-specific-testing.md)
Python-specific testing patterns - async/await, decorators, generators, context managers, type hints.

**When to use**: Testing Python-specific features
**Covers**: pytest-asyncio, testing decorators, generator testing, mypy integration
**Key Topics**: Async testing, decorator verification, StopIteration, type checking

---

## Quick Reference

### pytest vs unittest

| Feature | pytest | unittest |
|---------|--------|----------|
| **Style** | Functional | Class-based |
| **Assertions** | Plain `assert` | `self.assertEqual()` |
| **Setup** | Fixtures | `setUp()/tearDown()` |
| **Discovery** | Automatic | `unittest.main()` |
| **Dependencies** | pip install pytest | Standard library |

### Test Organization

```
project/
├── app/
│   └── module.py
└── tests/
    ├── conftest.py          # Shared fixtures
    ├── test_module.py       # Mirror source structure
    └── integration/
        └── test_api.py
```

### Coverage Goals

| Metric | Minimum | Target | Critical Path |
|--------|---------|--------|---------------|
| Line Coverage | 80% | 90%+ | 100% |
| Branch Coverage | 75% | 85%+ | 100% |
| Function Coverage | 85% | 90%+ | 100% |

### Mocking Decision Matrix

| Dependency Type | Strategy | Tool |
|----------------|----------|------|
| HTTP API | Stub responses | aioresponses, responses |
| Database | Test database | pytest fixtures |
| File I/O | Mock or tmp_path | unittest.mock, pytest |
| Time/Random | Patch | patch('time.time') |
| External Service | Mock | unittest.mock.Mock |

---

Return to [tdd-python-implementer agent](../tdd-python.md) | [examples/](../examples/INDEX.md) | [templates/](../templates/INDEX.md) | [checklists/](../checklists/INDEX.md)
