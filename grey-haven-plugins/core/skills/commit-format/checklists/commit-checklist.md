# Commit Message Checklist

**Use before creating any git commit.**

## Format Validation

- [ ] Type is one of: feat, fix, docs, style, refactor, test, chore, perf, ci, build, revert
- [ ] Type is lowercase
- [ ] Scope is meaningful and lowercase (if included)
- [ ] Subject uses imperative mood ("add" not "added")
- [ ] Subject is lowercase (NO capitals anywhere)
- [ ] Full header (type + scope + subject) is under 100 characters
- [ ] Subject doesn't end with a period

## Body (if included)

- [ ] Blank line after subject
- [ ] Explains **why** the change was made
- [ ] Wraps at 90 characters per line
- [ ] Uses bullet points for lists
- [ ] Written in present tense

## Footer (if included)

- [ ] Blank line before footer
- [ ] Breaking changes start with "BREAKING CHANGE:"
- [ ] Linear issues referenced as GREY-123
- [ ] GitHub issues referenced as #123

## Content Quality

- [ ] Commit message is descriptive and specific
- [ ] Change is atomic (single logical change)
- [ ] No sensitive information (passwords, keys, tokens)
- [ ] Multi-tenant changes mention tenant_id (if applicable)

## Python Projects

- [ ] Virtual environment activated (source .venv/bin/activate)
- [ ] Pre-commit hooks will run (Ruff, mypy, pytest)

## Before Pushing

- [ ] Commits follow squash-merge strategy (if merging to main)
- [ ] Breaking changes are clearly documented
- [ ] Linear issues are referenced
