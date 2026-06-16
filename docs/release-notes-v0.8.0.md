# v0.8.0 Release Notes Draft

## Summary

This release turns Question to Prompt Pack from a local skill into a more shareable and verifiable Codex workflow package.

## Highlights

- Added CI-friendly quality checks.
- Added benchmark validation for 50 realistic user-style requests.
- Added promotion copy, adoption guidance, and contribution workflow.
- Added release management guidance for future versions.
- Clarified the safety model: local skills first, cache second, GitHub metadata-only discovery after approval.

## Validation

```text
Rule check passed.
Unified benchmark validation passed for 50 cases.
Quality checks passed.
```

## Safety

- Discovery reads only `SKILL.md` metadata.
- Remote skills are not auto-installed.
- Remote code is not executed automatically.
- User profile data remains local and non-sensitive.

## Suggested Release Title

```text
v0.8.0 - Promotion and maintenance workflow
```

## Suggested GitHub Release Body

```markdown
Question to Prompt Pack now includes the materials needed for public adoption: a clearer README, benchmark validation, promotion copy, contribution templates, release-management guidance, and CI checks.

The core rule remains the same:

> Use the smallest frame that prevents misunderstanding.

Validation:

- `Rule check passed.`
- `Unified benchmark validation passed for 50 cases.`
- `Quality checks passed.`

Safety:

- GitHub discovery is metadata-only.
- No remote skill is auto-installed.
- No remote code is executed automatically.
```
