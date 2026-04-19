---
description: Verify every skill, agent, and plugin cross-reference in the plugin suite resolves to an existing target
allowed-tools:
  - Bash(python3 *)
  - Read
  - Grep
argument-hint: [--strict] [--format=github]
---

Run the cross-reference linter on every `SKILL.md`, agent, workflow, and reference doc under `grey-haven-plugins/`, verifying that every skill/agent reference resolves to something that actually exists.

<context>
The linter script lives at `grey-haven-plugins/plugin-auditor/scripts/cross_ref_lint.py` and uses only the Python standard library. It surfaces:

- `frontmatter-skill-missing` — a `skills:` auto-load entry (on a skill or an agent) that points to a skill that doesn't exist. These are silent failures at runtime.
- `related-agent-missing` — a "Related Agents" entry in a `SKILL.md` that names an agent file that doesn't exist.
- `legacy-ref-info` — a `grey-haven-X` reference that should be updated after the v2.0.0 rename. Known-legitimate cases (directory/repo names, markdown link targets, `not ...` counter-examples) are filtered.

Exit code 0 = clean. Exit code 1 = hard errors present.
</context>

<requirements>
Run the linter:

```bash
python3 grey-haven-plugins/plugin-auditor/scripts/cross_ref_lint.py $ARGUMENTS
```

Then:

1. Report the summary (inventory size, findings by category) back to the user.
2. For each hard error (`frontmatter-skill-missing`, `related-agent-missing`), propose one of three fixes:
   - Remove the broken reference (if the target is genuinely phantom)
   - Create the missing target (if it should exist)
   - Rename the reference (if the target exists under a different name)
3. For `legacy-ref-info` findings, check whether each is actually a rename that was missed or a legitimate external/phantom reference.
4. Do **not** apply fixes automatically — present the findings and let the user direct the cleanup.

Re-run the linter after fixes to confirm a clean baseline (`No cross-reference issues found.`).

Use `--strict` to elevate `legacy-ref-info` to hard errors for pre-release gates.
Use `--format=github` for CI annotations.
</requirements>
