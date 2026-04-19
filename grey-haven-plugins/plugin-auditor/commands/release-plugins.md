---
description: Release the Grey Haven plugin suite — bump all plugin.json versions in lockstep, prepend a CHANGELOG entry, run pre-flight lint, and create the release commit
allowed-tools:
  - Bash(python3 *)
  - Bash(git *)
  - Bash(date *)
  - Read
  - Edit
  - Write
  - TodoWrite
argument-hint: patch | minor | major | X.Y.Z
---

Coordinate a release of the `grey-haven-plugins` suite. All plugins in this repo ship together and are versioned in lockstep.

<context>
Helper scripts:
- `grey-haven-plugins/plugin-auditor/scripts/cross_ref_lint.py` — verifies every skill/agent cross-reference resolves
- `grey-haven-plugins/plugin-auditor/scripts/bump_plugin_versions.py` — bumps every plugin.json in lockstep

A release is a single commit that:
1. Bumps every `plugin.json` `version` field to the same new version
2. Prepends a new entry to `CHANGELOG.md` dated today
3. Uses a conventional commit message: `chore(plugins): release X.Y.Z — <one-line summary>`

Argument `$ARGUMENTS`:
- `patch`, `minor`, `major` → semver bump from current lockstep version
- `X.Y.Z` → explicit version (use when resetting after a version drift)
- empty → ask the user what kind of release this is
</context>

<pre-flight>
Run these checks **before any mutating action** and abort on failure:

1. **Cross-reference linter must pass.** Stale `skills:` entries or missing agent files in a release tag are a sharp edge for users.
   ```bash
   python3 grey-haven-plugins/plugin-auditor/scripts/cross_ref_lint.py
   ```
   If it exits non-zero, surface the findings and stop. Do not proceed to the bump.

2. **Current versions in lockstep.**
   ```bash
   python3 grey-haven-plugins/plugin-auditor/scripts/bump_plugin_versions.py --check
   ```
   If out of lockstep, report the drift and require `$ARGUMENTS` to be an explicit `X.Y.Z` — do not accept `patch`/`minor`/`major`.

3. **Working tree clean.** Run `git status --short`. If there are unstaged or untracked files beyond what the release should touch, stop and ask the user whether to commit them separately, stash them, or include them in the release.
</pre-flight>

<steps>
1. **Determine target version.**
   - If `$ARGUMENTS` is `patch`/`minor`/`major`: semver bump from the current lockstep version.
   - If `$ARGUMENTS` matches `^\d+\.\d+\.\d+$`: use it directly.
   - If `$ARGUMENTS` is empty: ask the user which kind of release, then proceed.

2. **Apply the version bump.**
   ```bash
   python3 grey-haven-plugins/plugin-auditor/scripts/bump_plugin_versions.py --bump <type>
   # or
   python3 grey-haven-plugins/plugin-auditor/scripts/bump_plugin_versions.py --version X.Y.Z
   ```

3. **Gather material for the CHANGELOG entry.**
   - Find the previous release tag: `git describe --tags --abbrev=0 --match 'v*' 2>/dev/null || echo ""`
   - If a tag exists: `git log <tag>..HEAD --oneline --no-merges`
   - Otherwise: `git log -n 30 --oneline --no-merges`
   - Today's date: `date +%Y-%m-%d`

4. **Draft the CHANGELOG entry.** Read `CHANGELOG.md` to match its existing format. Group commits into:
   - **Breaking Changes** (anything renamed, removed, or requiring user action)
   - **Fixed** (bug fixes, corrupted-file reconstructions, dead-ref cleanups)
   - **Added** (new plugins, skills, commands, capabilities)
   - **Changed** (version bumps, model changes, non-breaking edits)

   Keep each bullet concise and factual — the commit message already has the long form. Write the *user-facing* summary of what changed.

5. **Prepend the entry to `CHANGELOG.md`.** Insert just below the header block (before the previous most-recent entry). The header format in this repo is `## [Plugins X.Y.Z] - YYYY-MM-DD`.

6. **Preview for the user.** Show:
   - `git diff --stat grey-haven-plugins/ CHANGELOG.md`
   - The new CHANGELOG section (full text)
   - The proposed commit message
   Ask for confirmation before committing. Do not proceed without explicit approval.

7. **Commit.**
   ```bash
   git add grey-haven-plugins/ CHANGELOG.md
   git commit -m "chore(plugins): release X.Y.Z — <one-line summary>"
   ```

8. **Report next steps** to the user:
   - `git push origin main` to publish
   - `git tag -a vX.Y.Z -m "Release X.Y.Z"` if they want a release tag
   - `git push origin vX.Y.Z` to push the tag

Do not push or tag automatically — the user may want to amend or review first.
</steps>

<safeguards>
- Never force-push, skip hooks, or amend a published commit.
- If the cross-reference linter fails, stop — the release is blocked until the dangling refs are fixed (run `/audit-refs` or fix manually).
- If the working tree contains changes unrelated to the release, do not bundle them into the release commit. Offer to commit them separately first.
- If the user hasn't confirmed the preview, do not commit.
- Never bump a version without also adding a CHANGELOG entry for that version — leaving silent version bumps makes user-facing release notes useless.
</safeguards>
